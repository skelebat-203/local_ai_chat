"""Main entry point for the chat application."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.retriever import SubjectRetriever
from core.chat import ChatSession
from core.logger import ChatLogger
from commands.command_handler import CommandHandler
from utils.ui import print_welcome, get_user_input, print_warning


def initialize_components():
    """Initialize all application components."""
    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"

    retriever = SubjectRetriever(basepath=str(data_path))
    chat = ChatSession(model="llama3")
    logger = ChatLogger(basepath=str(data_path))

    return retriever, chat, logger, data_path


def load_defaults(retriever, chat):
    """Load default persona and subject."""
    try:
        default_system_prompt = retriever.build_system_prompt()
        chat.set_system_prompt(default_system_prompt)
        chat.set_subject_info(retriever.default_persona, retriever.default_subject)
    except Exception as e:
        print_warning(f"Could not load defaults: {e}")


def process_message(chat, user_input, text_streaming):
    """Process and send user message to chat."""
    print()
    
    if text_streaming:
        for chunk in chat.send_message_stream(user_input):
            print(chunk, end='', flush=True)
        print()
    else:
        response = chat.send_message(user_input)
        print(response)


def main():
    """Main application loop."""
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
