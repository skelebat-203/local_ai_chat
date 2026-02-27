"""Central command handler and router.

This module defines CommandHandler, which inspects user input lines,
routes slash commands to the appropriate handlers, and decides whether
a given line should be sent to the model as a prompt or treated as
a meta-command.
"""

from commands.chat_commands import (
    handle_chat_history,
    handle_chat_history_by_subject,
    handle_clear_history,
    handle_status,
    handle_streaming_toggle,
    handle_exit,
    handle_delete_chat,
    handle_chat_move,
)
from commands.subject_commands import (
    handle_list_personas,
    handle_list_subjects,
    handle_new_subject,
    handle_new_persona,
    handle_persona_subject_switch,
    handle_view_subject,
    handle_view_persona,
    handle_delete_persona,
    handle_delete_subject,
)
from utils.ui import print_commands


class CommandHandler:
    """Route and execute user commands within the chat loop."""

    def __init__(self, retriever, chat, logger):
        """Create a new command handler.

        Args:
            retriever: SubjectRetriever instance used for metadata and logs.
            chat: ChatSession used for sending messages and tracking state.
            logger: ChatLogger used by some commands for persistence.
        """
        self.retriever = retriever
        self.chat = chat
        self.logger = logger
        self.text_streaming = True

    def handle_command(self, user_input: str) -> tuple[bool, str | None]:
        """Process a single user input line.

        Determines whether the line is:
            - a slash command (e.g. /help, /s_new, /swap)
            - a persona/subject switch line
            - a normal chat prompt to send to the model

        Args:
            user_input: Raw line typed by the user.

        Returns:
            (should_exit, modified_input) where:
                should_exit: True if the main loop should stop.
                modified_input: None if no prompt should be sent to the model
                    for this line, or a possibly-modified prompt string to
                    forward to ChatSession.
        """
        cmd = user_input.lower()

        if cmd == "/exit":
            return handle_exit(self.chat, self.logger), None

        if cmd == "/help":
            print_commands()
            return False, None

        if cmd == "/pref_streaming":
            self.text_streaming = handle_streaming_toggle(self.text_streaming)
            return False, None

        if cmd == "/p":
            handle_list_personas(self.retriever)
            return False, None

        if cmd == "/s":
            handle_list_subjects(self.retriever)
            return False, None

        if cmd == "/s_inst":
            handle_view_subject(self.retriever, self.chat)
            return False, None

        if cmd == "/p_inst":
            handle_view_persona(self.retriever, self.chat)
            return False, None

        if cmd == "/status":
            handle_status(self.chat, self.text_streaming)
            return False, None

        if cmd == "/clear":
            handle_clear_history(self.chat)
            return False, None

        if cmd == "/c_history":
            handle_chat_history(self.retriever, self.chat)
            return False, None

        if cmd.startswith("/c_history_"):
            subject_name = user_input[14:].strip()
            handle_chat_history_by_subject(self.retriever, self.chat, subject_name)
            return False, None

        if cmd.startswith("/s_new"):
            parts = user_input.split(maxsplit=1)
            subject_name = parts[1].strip() if len(parts) > 1 else ""
            handle_new_subject(self.retriever, self.chat, subject_name)
            return False, None

        if cmd.startswith("/p_new"):
            parts = user_input.split(maxsplit=1)
            persona_name = parts[1].strip() if len(parts) > 1 else ""
            handle_new_persona(self.retriever, self.chat, persona_name)
            return False, None

        # Persona/subject inline switch; may also return a prompt
        prompt = handle_persona_subject_switch(self.retriever, self.chat, user_input)
        if prompt is not None:
            return False, prompt if prompt else None

        if cmd.startswith("/p_delete"):
            parts = user_input.split(maxsplit=1)
            persona_name = parts[1].strip() if len(parts) > 1 else ""
            handle_delete_persona(self.retriever, self.chat, persona_name)
            return False, None

        if cmd.startswith("/s_delete"):
            parts = user_input.split(maxsplit=1)
            subject_name = parts[1].strip() if len(parts) > 1 else ""
            handle_delete_subject(self.retriever, self.chat, subject_name)
            return False, None

        if cmd.startswith("/c_delete"):
            parts = user_input.split(maxsplit=1)
            idx = parts[1].strip() if len(parts) > 1 else ""
            handle_delete_chat(self.retriever, self.chat, idx)
            return False, None

        if cmd.startswith("/c_move"):
            handle_chat_move(self.retriever, self.chat, None)
            return False, None

        if cmd.startswith("/swap"):
            # formats:
            #   /swap           -> toggle llama3 <-> qwen2.5-coder
            #   /swap llama3    -> set explicitly
            #   /swap qwen      -> set explicitly (short alias)
            parts = user_input.split(maxsplit=1)
            if len(parts) == 1:
                current = self.chat.model
                if current == "llama3":
                    new_model = "qwen2.5-coder:32b"
                else:
                    new_model = "llama3"
            else:
                target = parts[1].strip().lower()
                if target in ("llama3", "llama"):
                    new_model = "llama3"
                elif target in ("qwen2.5-coder", "qwen"):
                    new_model = "qwen2.5-coder"
                else:
                    print("Unknown model. Use: llama3 or qwen2.5-coder.")
                    return False, None

            self.chat.set_model(new_model)
            return False, None

        # Not a recognized command – treat as a normal prompt
        return False, user_input
