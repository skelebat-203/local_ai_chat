import os
from pathlib import Path

class SubjectRetriever:
    def __init__(self, basepath="."):
        self.basepath = Path(basepath)
        self.personas_path = self.basepath / "personas"
        self.subjects_path = self.basepath / "subjects"
    
    def load_persona(self, persona_name):
        """Load persona instructions from personas folder"""
        persona_file = self.personas_path / f"{persona_name.lower()}.md"
        if persona_file.exists():
            with open(persona_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"Persona '{persona_name}' not found at {persona_file}")
    
    def load_subject_instructions(self, subject_name):
        """Load instructions.md from specific subject folder"""
        instructions_file = self.subjects_path / subject_name / "instructions.md"
        if instructions_file.exists():
            with open(instructions_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"Instructions for subject '{subject_name}' not found at {instructions_file}")
    
    def load_chat_logs(self, subject_name):
        """Load all chat logs from subject folder"""
        subject_folder = self.subjects_path / subject_name
        chat_logs = []
        
        if subject_folder.exists():
            # Load chatlog.md if it exists
            chatlog_file = subject_folder / "chatlog.md"
            if chatlog_file.exists():
                with open(chatlog_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():  # Only add if not empty
                        chat_logs.append(content)
            
            # Load any other chat log files (chat_*.md pattern)
            for file in sorted(subject_folder.glob("chat_*.md")):
                if file.name != "chatlog.md":  # Avoid duplicate
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            chat_logs.append(content)
        
        return "\n---\n".join(chat_logs) if chat_logs else ""
    
    def build_system_prompt(self, persona_name, subject_name):
        """Build complete system prompt with persona and subject"""
        persona = self.load_persona(persona_name)
        instructions = self.load_subject_instructions(subject_name)
        chat_history = self.load_chat_logs(subject_name)
        
        system_prompt = f"""# Persona
{persona}

# Subject Instructions
{instructions}"""
        
        if chat_history:
            system_prompt += f"""

# Previous Chat History
{chat_history}"""
        
        return system_prompt
    
    def parse_subject_command(self, user_input):
        """Parse commands like 'Persona: writer, Subject: Fantasy story, prompt'
        Returns (persona, subject, remaining_prompt)"""
        if "persona" in user_input.lower() and "subject" in user_input.lower():
            persona = None
            subject = None
            prompt_parts = []
            
            # Split by comma but handle the prompt part carefully
            parts = user_input.split(',')
            for i, part in enumerate(parts):
                part_lower = part.strip().lower()
                if part_lower.startswith("persona"):
                    persona = part.split(':', 1)[1].strip()
                elif part_lower.startswith("subject"):
                    subject = part.split(':', 1)[1].strip()
                else:
                    # Everything after persona/subject is the prompt
                    prompt_parts.append(part.strip())
            
            prompt = ', '.join(prompt_parts).strip()
            return persona, subject, prompt
        
        return None, None, user_input
    
    def list_personas(self):
        """List all available personas"""
        if self.personas_path.exists():
            return [f.stem for f in self.personas_path.glob("*.md")]
        return []
    
    def list_subjects(self):
        """List all available subjects"""
        if self.subjects_path.exists():
            return [d.name for d in self.subjects_path.iterdir() if d.is_dir()]
        return []
