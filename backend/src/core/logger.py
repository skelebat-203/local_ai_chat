import os
from datetime import datetime
from pathlib import Path


class ChatLogger:
    """Persist chat conversations to markdown files on disk.

    Chat logs are organized under a base 'subjects' directory. Each
    subject has its own folder with an instructions.md template and
    one or more chat_*.md files, plus an optional rolling chatlog.md.
    """

    def __init__(self, basepath: str = "."):
        """Create a new ChatLogger rooted at the given base path.

        Args:
            basepath: Directory that contains the 'subjects' folder.
        """
        self.basepath = Path(basepath)
        self.subjects_path = self.basepath / "subjects"

    def save_chat(self, subject_name: str, conversation_history, append: bool = False) -> Path:
        """Save a chat log to the specified subject folder.

        Args:
            subject_name: Name of the subject folder.
            conversation_history: List of message dicts produced by ChatSession.
            append: If True, append to chatlog.md; otherwise create a new
                timestamped chat_*.md file.

        Returns:
            Path to the log file that was written.

        Raises:
            FileNotFoundError: If the subject folder does not exist.
        """
        subject_folder = self.subjects_path / subject_name

        if not subject_folder.exists():
            raise FileNotFoundError(f"Subject folder '{subject_name}' does not exist")

        if append:
            log_file = subject_folder / "chatlog.md"
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
            log_file = subject_folder / f"chat_{timestamp}.md"

        log_content = self.format_conversation(conversation_history)

        mode = "a" if (append and log_file.exists()) else "w"
        with open(log_file, mode, encoding="utf-8") as f:
            if mode == "a":
                f.write("\n---\n")
                f.write(f"# Session {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(log_content)

        return log_file

    def format_conversation(self, conversation_history) -> str:
        """Format conversation history as markdown.

        Args:
            conversation_history: List of message dicts with 'role' and 'content'.

        Returns:
            A markdown-formatted string representation of the conversation.
        """
        formatted = []
        for msg in conversation_history:
            role = msg["role"].capitalize()
            content = msg["content"]
            formatted.append(f"**{role}:**\n{content}\n")
        return "\n".join(formatted)

    def create_subject_folder(self, subject_name: str) -> Path:
        """Create a new subject folder with a default instructions template.

        If the folder already exists it is reused, and an instructions.md
        file is created only if missing.

        Args:
            subject_name: Name of the subject to create.

        Returns:
            Path to the subject folder.
        """
        subject_folder = self.subjects_path / subject_name
        subject_folder.mkdir(parents=True, exist_ok=True)

        instructions_file = subject_folder / "instructions.md"
        if not instructions_file.exists():
            with open(instructions_file, "w", encoding="utf-8") as f:
                f.write(f"# Instructions for {subject_name}\n\n")
                f.write("Add your subject-specific instructions here.\n")

        return subject_folder
