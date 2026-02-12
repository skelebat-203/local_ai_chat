"""
Chat Logger
Saves conversation logs to appropriate context folders
"""
from pathlib import Path
from datetime import datetime

class ChatLogger:
    def __init__(self, base_path="Chat_App"):
        self.base_path = Path(base_path)
        self.contexts_path = self.base_path / "contexts"

    def save_chat(self, context_name, conversation_history, append=False):
        """
        Save chat log to the specified context folder

        Args:
            context_name: Name of the context folder
            conversation_history: List of message dictionaries
            append: If True, append to existing chat_log.md, else create new file
        """
        context_folder = self.contexts_path / context_name

        # Ensure context folder exists
        if not context_folder.exists():
            raise FileNotFoundError(f"Context folder '{context_name}' does not exist")

        # Determine log file
        if append:
            log_file = context_folder / "chat_log.md"
        else:
            # Create timestamped log file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = context_folder / f"chat_{timestamp}.md"

        # Format the conversation
        log_content = self._format_conversation(conversation_history)

        # Write to file
        mode = 'a' if append and log_file.exists() else 'w'
        with open(log_file, mode, encoding='utf-8') as f:
            if mode == 'a':
                f.write("\n\n---\n\n")  # Separator for appended sessions
            f.write(f"## Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(log_content)

        return log_file

    def _format_conversation(self, conversation_history):
        """Format conversation history as markdown"""
        formatted = []
        for msg in conversation_history:
            role = msg["role"].capitalize()
            content = msg["content"]
            formatted.append(f"**{role}:** {content}\n")
        return "\n".join(formatted)

    def create_context_folder(self, context_name):
        """Create a new context folder with instructions.md template"""
        context_folder = self.contexts_path / context_name
        context_folder.mkdir(parents=True, exist_ok=True)

        # Create instructions.md if it doesn't exist
        instructions_file = context_folder / "instructions.md"
        if not instructions_file.exists():
            with open(instructions_file, 'w', encoding='utf-8') as f:
                f.write(f"# Instructions for {context_name}\n\n")
                f.write("Add your context-specific instructions here.\n")

        return context_folder
