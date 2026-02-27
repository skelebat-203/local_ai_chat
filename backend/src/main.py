"""Main entry point for the subject-aware local chat application.

This module wires together the SubjectRetriever, ChatSession, ChatLogger,
and CommandHandler, then runs an interactive REPL in the terminal.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.retriever import SubjectRetriever
from core.chat import ChatSession
from core.logger import ChatLogger
from commands.command_handler import CommandHandler
from utils.ui import print_welcome, get_user_input, print_warning


def initialize_components():
    """Create and configure retriever, chat session, logger, and data path.

    Returns:
        (retriever, chat, logger, data_path) tuple where:
            retriever: SubjectRetriever instance
            chat: ChatSession instance
            logger: ChatLogger instance
            data_path: Path to the data directory containing personas/subjects
    """
    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"

    retriever = SubjectRetriever(basepath=str(data_path))
    chat = ChatSession(model="llama3")  # default model
    logger = ChatLogger(str(data_path))

    return retriever, chat, logger, data_path


def load_defaults(retriever, chat):
    """Load and apply the default persona and subject to the chat session.

    Any errors are surfaced as a warning, but the app can still run
    without defaults if necessary.
    """
    try:
        default_system_prompt = retriever.build_system_prompt()
        chat.set_system_prompt(default_system_prompt)
        chat.set_subject_info(retriever.default_persona, retriever.default_subject)
    except Exception as e:
        print_warning(f"Could not load defaults: {e}")


def process_message(chat, user_input: str, text_streaming: bool):
    """Send a user message to the model and print the assistant response.

    Args:
        chat: ChatSession used to talk to the model.
        user_input: User prompt to send.
        text_streaming: Whether to stream the response chunk‑by‑chunk.
    """
    print()

    if text_streaming:
        print("Assistant:")
        for chunk in chat.send_message_stream(user_input):
            print(chunk, end="", flush=True)
        print()
    else:
        response = chat.send_message(user_input)
        print("Assistant:\n" + response)


def main():
    """Run the interactive chat loop until the user chooses to exit."""
    retriever, chat, logger, data_path = initialize_components()
    load_defaults(retriever, chat)

    command_handler = CommandHandler(retriever, chat, logger)

    print_welcome()

    while True:
        try:
            user_input = get_user_input()
            if not user_input:
                continue

            should_exit, modified_input = command_handler.handle_command(user_input)

            if should_exit:
                break

            if modified_input:
                process_message(chat, modified_input, command_handler.text_streaming)

        except KeyboardInterrupt:
            print("\n⚠ Use /exit to save and quit.")
        except Exception as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
