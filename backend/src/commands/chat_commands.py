"""Chat-related command handlers."""

from pathlib import Path
from utils.ui import (
    print_section_header, print_success, print_error,
    get_user_input, display_chat_history
)


def handle_chat_history(retriever, chat):
    """Handle /chat_history command - view all chats."""
    all_chats = retriever.list_all_chats()
    if not all_chats:
        print("No chat history found.")
        return None

    print_section_header("All Chat History")
    for idx, chat_info in enumerate(all_chats, 1):
        subject, filename, file_path = chat_info
        print(f"{idx}. [{subject}] {filename}")
    print("=" * 60)

    try:
        selection = get_user_input("\nEnter number to open chat (or press Enter to cancel): ")
        if not selection:
            return None

        chat_idx = int(selection) - 1
        if 0 <= chat_idx < len(all_chats):
            subject, filename, file_path = all_chats[chat_idx]
            return _load_chat_file(retriever, chat, file_path, subject, filename)
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
        return None


def handle_chat_history_by_subject(retriever, chat, subject_name):
    """Handle /chat_history_[subject] command - view chats for specific subject."""
    if not subject_name:
        print("Please specify a subject: /chat_history_[subject]")
        return None

    chats = retriever.list_chats_by_subject(subject_name)
    if not chats:
        print(f"No chat history found for subject '{subject_name}'.")
        return None

    print_section_header(f"Chat History for: {subject_name}")
    for idx, chat_info in enumerate(chats, 1):
        filename, file_path = chat_info
        print(f"{idx}. {filename}")
    print("=" * 60)

    try:
        selection = get_user_input("\nEnter number to open chat (or press Enter to cancel): ")
        if not selection:
            return None

        chat_idx = int(selection) - 1
        if 0 <= chat_idx < len(chats):
            filename, file_path = chats[chat_idx]
            return _load_chat_file(retriever, chat, file_path, subject_name, filename)
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
        return None


def _load_chat_file(retriever, chat, file_path, subject_name, filename):
    """Helper function to load a chat file."""
    loaded_history = retriever.load_chat_file(file_path)
    chat.load_history(loaded_history)

    system_prompt = retriever.build_system_prompt(retriever.default_persona, subject_name)
    chat.set_system_prompt(system_prompt)
    chat.set_subject_info(retriever.default_persona, subject_name)

    print_success(f"Loaded chat from {filename}")
    print_success(f"Subject: {subject_name}")
    print_success("You can now continue this conversation")

    display_chat_history(loaded_history)

    chat.original_chat_file = file_path
    return True


def handle_clear_history(chat):
    """Handle /clear command."""
    chat.clear_history()
    print_success("Conversation history cleared")


def handle_status(chat, text_streaming):
    """Handle /status command."""
    persona = chat.current_persona or "None"
    subject = chat.current_subject or "None"
    streaming_status = "on" if text_streaming else "off"
    print(f"Persona: {persona}")
    print(f"Current Subject: {subject}")
    print(f"Model: {chat.model}")
    print(f"Text Streaming: {streaming_status}")


def handle_streaming_toggle(text_streaming):
    """Handle /pref_streaming command."""
    current_state = "on" if text_streaming else "off"
    target_state = "off" if text_streaming else "on"

    response = get_user_input(f"Turn text streaming {target_state}? 'y' / 'n'? ").lower()

    if response == 'y':
        text_streaming = not text_streaming
        new_state = "on" if text_streaming else "off"
        print(f"Text streaming is now {new_state}. What would you like to discuss?")
    elif response == 'n':
        print("No change. What would you like to discuss?")
    else:
        print("Invalid response. No change made.")

    return text_streaming


def handle_exit(chat, logger):
    """Handle /exit command."""
    if chat.current_subject and chat.conversation_history:
        from utils.ui import get_confirmation, print_success
        
        if get_confirmation(f"Save chat to '{chat.current_subject}'?"):
            log_file = logger.save_chat(chat.current_subject, chat.conversation_history)
            print_success(f"Chat saved to {log_file}")

            if hasattr(chat, 'original_chat_file') and chat.original_chat_file.exists():
                chat.original_chat_file.unlink()
                print_success(f"Removed old chat file: {chat.original_chat_file.name}")
    
    print("Goodbye!")
    return True
