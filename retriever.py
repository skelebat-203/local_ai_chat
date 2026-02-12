"""
Context and Persona Retrieval System
Loads persona files, context instructions, and chat logs
"""
import os
from pathlib import Path


class ContextRetriever:
    def __init__(self, base_path="Chat_App"):
        self.base_path = Path(base_path)
        self.personas_path = self.base_path / "personas"
        self.contexts_path = self.base_path / "contexts"

    def load_persona(self, persona_name):
        """Load persona instructions from personas folder"""
        persona_file = self.personas_path / f"{persona_name.lower()}.md"
        if persona_file.exists():
            with open(persona_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"Persona '{persona_name}' not found at {persona_file}")

    def load_context_instructions(self, context_name):
        """Load instructions.md from specific context folder"""
        instructions_file = self.contexts_path / context_name / "instructions.md"
        if instructions_file.exists():
            with open(instructions_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"Instructions for context '{context_name}' not found at {instructions_file}")

    def load_chat_logs(self, context_name):
        """Load all chat logs from context folder"""
        context_folder = self.contexts_path / context_name
        chat_logs = []

        if context_folder.exists():
            # Load chat_log.md if it exists
            chat_log_file = context_folder / "chat_log.md"
            if chat_log_file.exists():
                with open(chat_log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():  # Only add if not empty
                        chat_logs.append(content)

            # Load any other chat log files (chat_*.md pattern)
            for file in sorted(context_folder.glob("chat_*.md")):
                if file.name != "chat_log.md":  # Avoid duplicate
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            chat_logs.append(content)

        return "\n\n---\n\n".join(chat_logs) if chat_logs else ""

    def build_system_prompt(self, persona_name, context_name):
        """Build complete system prompt with persona + context"""
        persona = self.load_persona(persona_name)
        instructions = self.load_context_instructions(context_name)
        chat_history = self.load_chat_logs(context_name)

        system_prompt = f"""# Persona
{persona}

# Context Instructions
{instructions}
"""

        # Only add chat history section if there are logs
        if chat_history:
            system_prompt += f"""
# Previous Chat History
{chat_history}
"""

        return system_prompt

    def parse_context_command(self, user_input):
        """
        Parse commands like 'Persona = writer, Context = Fantasy story, [prompt]'
        Returns: (persona, context, remaining_prompt)
        """
        if "persona" in user_input.lower() and "context" in user_input.lower():
            # Split by comma but handle the prompt part carefully
            persona = None
            context = None
            prompt_parts = []

            # Find persona and context assignments
            parts = user_input.split(",")
            for i, part in enumerate(parts):
                part_lower = part.strip().lower()
                if part_lower.startswith("persona"):
                    persona = part.split("=")[1].strip()
                elif part_lower.startswith("context"):
                    context = part.split("=")[1].strip()
                else:
                    # Everything after persona/context is the prompt
                    prompt_parts.append(part.strip())

            prompt = ", ".join(prompt_parts).strip()
            return persona, context, prompt

        return None, None, user_input

    def list_personas(self):
        """List all available personas"""
        if self.personas_path.exists():
            return [f.stem for f in self.personas_path.glob("*.md")]
        return []

    def list_contexts(self):
        """List all available contexts"""
        if self.contexts_path.exists():
            return [d.name for d in self.contexts_path.iterdir() if d.is_dir()]
        return []
