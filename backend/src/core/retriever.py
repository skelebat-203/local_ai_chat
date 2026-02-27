import os
from pathlib import Path


class SubjectRetriever:
    """Manage personas, subjects, and chat files on disk.

    This class knows how to:
        - Load and update persona instruction files
        - Load and update subject instructions
        - Build system prompts from persona, subject, and chat history
        - Parse inline persona/subject commands from user input
        - List, load, delete, and move chat markdown files
    """

    def __init__(self, basepath: str = "."):
        """Initialize a new SubjectRetriever.

        Args:
            basepath: Base directory that contains 'personas' and 'subjects'
                subdirectories used to store configuration and chat logs.
        """
        self.basepath = Path(basepath)
        self.personas_path = self.basepath / "personas"
        self.subjects_path = self.basepath / "subjects"
        self.default_persona = "default"
        self.default_subject = "no_subject"

    def load_persona(self, persona_name: str | None = None) -> str:
        """Load persona instructions from the personas folder.

        If persona_name is None, the default persona file is loaded.
        When a non-default persona is missing, this method falls back
        to the default persona if present, otherwise it raises.

        Args:
            persona_name: Optional persona name (without .md extension).

        Returns:
            The contents of the persona markdown file as a string.

        Raises:
            FileNotFoundError: If neither the requested nor default persona
                file can be found.
        """
        if persona_name is None:
            persona_name = self.default_persona

        persona_file = self.personas_path / f"{persona_name.lower()}.md"
        if persona_file.exists():
            with open(persona_file, "r", encoding="utf-8") as f:
                return f.read()

        if persona_name != self.default_persona:
            default_file = self.personas_path / f"{self.default_persona}.md"
            if default_file.exists():
                print(f"⚠ Persona '{persona_name}' not found, using default")
                with open(default_file, "r", encoding="utf-8") as f:
                    return f.read()

        raise FileNotFoundError(f"Persona '{persona_name}' not found at {persona_file}")

    def load_subject_instructions(self, subject_name: str | None = None) -> str:
        """Load instructions.md for a subject, defaulting to no_subject.

        If subject_name is None, the default subject is used. When a
        subject is missing, this method falls back to the default subject
        instructions if available, otherwise it raises.

        Args:
            subject_name: Optional subject folder name.

        Returns:
            The contents of the subject's instructions.md file.

        Raises:
            FileNotFoundError: If neither the requested nor default subject
                instructions can be found.
        """
        if subject_name is None:
            subject_name = self.default_subject

        instructions_file = self.subjects_path / subject_name / "instructions.md"
        if instructions_file.exists():
            with open(instructions_file, "r", encoding="utf-8") as f:
                return f.read()

        if subject_name != self.default_subject:
            default_file = self.subjects_path / self.default_subject / "instructions.md"
            if default_file.exists():
                print(f"⚠ Subject '{subject_name}' not found, using default")
                with open(default_file, "r", encoding="utf-8") as f:
                    return f.read()

        raise FileNotFoundError(
            f"Instructions for subject '{subject_name}' not found at {instructions_file}"
        )

    def update_persona_instructions(self, persona_name: str, new_instructions: str) -> bool:
        """Overwrite instructions for an existing persona file.

        Args:
            persona_name: Name of the persona to update.
            new_instructions: New markdown/text content to store.

        Returns:
            True if the file was updated successfully, False otherwise.
        """
        persona_file = self.personas_path / f"{persona_name.lower()}.md"

        if not persona_file.exists():
            return False

        try:
            with open(persona_file, "w", encoding="utf-8") as f:
                f.write(new_instructions)
            return True
        except Exception as e:
            print(f"Error updating persona: {e}")
            return False

    def update_subject_instructions(self, subject_name: str, new_instructions: str) -> bool:
        """Overwrite instructions for an existing subject.

        Args:
            subject_name: Name of the subject to update.
            new_instructions: New markdown/text content to store.

        Returns:
            True if the file was updated successfully, False otherwise.
        """
        instructions_file = self.subjects_path / subject_name / "instructions.md"

        if not instructions_file.exists():
            return False

        try:
            with open(instructions_file, "w", encoding="utf-8") as f:
                f.write(new_instructions)
            return True
        except Exception as e:
            print(f"Error updating subject instructions: {e}")
            return False

    def load_chat_logs(self, subject_name: str) -> str:
        """Load all chat logs for a subject as a single combined string.

        This will merge the rolling chatlog.md (if present) with all
        timestamped chat_*.md files, separated by '---' markers.

        Args:
            subject_name: Name of the subject folder.

        Returns:
            Combined markdown text of all chat logs, or an empty string
            if no logs exist.
        """
        subject_folder = self.subjects_path / subject_name
        chat_logs = []

        if subject_folder.exists():
            chatlog_file = subject_folder / "chatlog.md"
            if chatlog_file.exists():
                with open(chatlog_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content.strip():
                        chat_logs.append(content)

            for file in sorted(subject_folder.glob("chat_*.md")):
                if file.name != "chatlog.md":
                    with open(file, "r", encoding="utf-8") as f:
                        content = f.read()
                        if content.strip():
                            chat_logs.append(content)

        return "\n---\n".join(chat_logs) if chat_logs else ""

    def build_system_prompt(self, persona_name: str | None = None, subject_name: str | None = None) -> str:
        """Build the full system prompt combining persona, subject, and history.

        Args:
            persona_name: Optional persona name; defaults to the retriever's
                default persona if not specified.
            subject_name: Optional subject name; defaults to the default
                subject if not specified.

        Returns:
            A multiline system prompt string.
        """
        persona = self.load_persona(persona_name)
        instructions = self.load_subject_instructions(subject_name)

        chat_history = ""
        if subject_name and subject_name != self.default_subject:
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

    def parse_subject_command(self, user_input: str):
        """Parse inline Persona/Subject declarations from a user input string.

        Supports flexible formats, for example:
            - "Persona: writer"
            - "Subject: Fantasy story"
            - "Persona: writer, Subject: Fantasy story"
            - "Persona: writer, Subject: Fantasy story, prompt"
            - "Subject: Fantasy story, Persona: writer, prompt"

        Args:
            user_input: Raw user text to inspect.

        Returns:
            tuple (persona, subject, prompt, is_meta_only) where:
                persona: extracted persona name or None
                subject: extracted subject name or None
                prompt: remaining text after declarations (may be "")
                is_meta_only: True if only persona/subject was set and
                    there is no prompt text.
        """
        text = user_input.strip()
        lower_text = text.lower()

        if "persona" not in lower_text and "subject" not in lower_text:
            return None, None, text, False

        persona = None
        subject = None
        prompt_parts = []

        parts = text.split(",")

        for part in parts:
            raw = part.strip()
            lower = raw.lower()

            if lower.startswith("persona"):
                if ":" in raw:
                    persona_value = raw.split(":", 1)[1].strip()
                    if persona_value:
                        persona = persona_value
            elif lower.startswith("subject"):
                if ":" in raw:
                    subject_value = raw.split(":", 1)[1].strip()
                    if subject_value:
                        subject = subject_value
            else:
                if raw:
                    prompt_parts.append(raw)

        prompt = ", ".join(prompt_parts).strip()
        is_meta_only = (persona is not None or subject is not None) and (prompt == "")

        return persona, subject, prompt, is_meta_only

    def list_personas(self):
        """List all available personas by stem name (without .md)."""
        if self.personas_path.exists():
            return [f.stem for f in self.personas_path.glob("*.md")]
        return []

    def list_subjects(self):
        """List all available subject folder names."""
        if self.subjects_path.exists():
            return [d.name for d in self.subjects_path.iterdir() if d.is_dir()]
        return []

    def list_all_chats(self):
        """List all chat files across all subjects.

        Returns:
            List of tuples (subject_name, chat_filename, file_path),
            sorted by filename (timestamp).
        """
        all_chats = []
        if self.subjects_path.exists():
            for subject_dir in self.subjects_path.iterdir():
                if subject_dir.is_dir():
                    for chat_file in sorted(subject_dir.glob("chat_*.md")):
                        all_chats.append((subject_dir.name, chat_file.name, chat_file))
        all_chats.sort(key=lambda x: x[1])
        return all_chats

    def list_chats_by_subject(self, subject_name: str):
        """List all chat files in a specific subject folder.

        Args:
            subject_name: Subject folder name.

        Returns:
            List of tuples (chat_filename, file_path), sorted by filename.
        """
        chats = []
        subject_folder = self.subjects_path / subject_name
        if subject_folder.exists():
            for chat_file in sorted(subject_folder.glob("chat_*.md")):
                chats.append((chat_file.name, chat_file))
        chats.sort(key=lambda x: x[0])
        return chats

    def load_chat_file(self, chat_file_path: Path | str):
        """Load a chat markdown file and parse it into conversation history.

        Args:
            chat_file_path: Path to a chat_*.md or chatlog.md file.

        Returns:
            List of message dicts with 'role' and 'content' keys. Returns an
            empty list if parsing fails.
        """
        conversation_history = []

        try:
            with open(chat_file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading chat file: {e}")
            return []

        lines = content.split("\n")
        current_role = None
        current_content = []

        for line in lines:
            if line.strip().lower().startswith("**user:**"):
                if current_role and current_content:
                    conversation_history.append(
                        {"role": current_role, "content": "\n".join(current_content).strip()}
                    )
                current_role = "user"
                current_content = []
            elif line.strip().lower().startswith("**assistant:**"):
                if current_role and current_content:
                    conversation_history.append(
                        {"role": current_role, "content": "\n".join(current_content).strip()}
                    )
                current_role = "assistant"
                current_content = []
            elif current_role is not None:
                current_content.append(line)

        if current_role and current_content:
            conversation_history.append(
                {"role": current_role, "content": "\n".join(current_content).strip()}
            )

        print(f"Loaded {len(conversation_history)} messages from chat file")
        return conversation_history if conversation_history else []

    def create_subject_folder(self, subject_name: str) -> bool:
        """Create a new subject folder if it does not already exist.

        Args:
            subject_name: Name of the subject folder to create.

        Returns:
            True if the folder was created, False if it already existed.
        """
        subject_path = self.subjects_path / subject_name

        if subject_path.exists():
            return False

        subject_path.mkdir(parents=True, exist_ok=True)
        return True

    def save_subject_instructions(self, subject_name: str, instructions: str) -> Path:
        """Create or overwrite instructions for a subject.

        Ensures the subject folder exists before writing.

        Args:
            subject_name: Subject folder name.
            instructions: Instructions text to save.

        Returns:
            Path to the newly written instructions.md file.
        """
        subject_path = self.subjects_path / subject_name

        if not subject_path.exists():
            subject_path.mkdir(parents=True, exist_ok=True)

        instructions_file = subject_path / "instructions.md"
        with open(instructions_file, "w", encoding="utf-8") as f:
            f.write(f"# {subject_name} Instructions\n\n")
            f.write(instructions)

        return instructions_file

    def delete_persona(self, persona_name: str) -> bool:
        """Delete a persona .md file (cannot delete the default persona).

        Args:
            persona_name: Name of the persona to delete.

        Returns:
            True if the file was deleted, False otherwise.
        """
        persona_name = persona_name.lower()
        if persona_name == self.default_persona.lower():
            print("Default persona cannot be deleted.")
            return False

        persona_file = self.personas_path / f"{persona_name}.md"
        if not persona_file.exists():
            print(f"Persona '{persona_name}' not found.")
            return False

        try:
            persona_file.unlink()
            return True
        except Exception as e:
            print(f"Error deleting persona: {e}")
            return False

    def delete_subject(self, subject_name: str) -> bool:
        """Delete an entire subject folder and all of its contents.

        Args:
            subject_name: Name of the subject folder to delete.

        Returns:
            True if deletion was successful, False otherwise.
        """
        if subject_name == self.default_subject:
            print("Default subject cannot be deleted.")
            return False

        subject_path = self.subjects_path / subject_name
        if not subject_path.exists():
            print(f"Subject '{subject_name}' not found.")
            return False

        try:
            for root, dirs, files in os.walk(subject_path, topdown=False):
                root_path = Path(root)
                for f in files:
                    (root_path / f).unlink()
                for d in dirs:
                    (root_path / d).rmdir()
            subject_path.rmdir()
            return True
        except Exception as e:
            print(f"Error deleting subject: {e}")
            return False

    def delete_chat_file(self, subject_name: str, chat_filename: str) -> bool:
        """Delete a specific chat markdown file in a subject folder.

        Args:
            subject_name: Subject folder name.
            chat_filename: File name of the chat to delete.

        Returns:
            True if the file was deleted, False otherwise.
        """
        subject_folder = self.subjects_path / subject_name
        chat_path = subject_folder / chat_filename

        if not chat_path.exists():
            print(f"Chat '{chat_filename}' not found in subject '{subject_name}'.")
            return False

        try:
            chat_path.unlink()
            return True
        except Exception as e:
            print(f"Error deleting chat file: {e}")
            return False

    def move_chat_to_subject(self, source_subject: str, chat_filename: str, target_subject: str) -> bool:
        """Move a chat file from one subject folder to another.

        Args:
            source_subject: Name of the source subject folder.
            chat_filename: Chat file name to move.
            target_subject: Name of the target subject folder.

        Returns:
            True if the file was moved successfully, False otherwise.
        """
        source_folder = self.subjects_path / source_subject
        target_folder = self.subjects_path / target_subject

        source_path = source_folder / chat_filename
        if not source_path.exists():
            print(f"Chat {chat_filename} not found in subject {source_subject}.")
            return False

        try:
            target_folder.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Error creating target subject folder {target_subject}: {e}")
            return False

        target_path = target_folder / chat_filename

        try:
            target_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
            source_path.unlink()
            return True
        except Exception as e:
            print(f"Error moving chat from {source_subject} to {target_subject}: {e}")
            return False
