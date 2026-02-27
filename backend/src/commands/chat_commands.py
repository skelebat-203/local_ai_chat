"""Chat history and status command handlers.

This module contains helpers for commands that operate on the current
chat session and its stored conversations, including:

    - /status        : Show current persona, subject, and model info
    - /clear         : Clear in-memory conversation history
    - /c_history     : List and preview chats across all subjects
    - /c_history_<s> : List and preview chats for a specific subject
    - /c_delete      : Delete a chat by index
    - /c_move        : Move a chat between subjects
    - /pref_streaming: Toggle streaming preference
    - /exit          : Exit the application cleanly

These functions are invoked by CommandHandler and interact with
SubjectRetriever, ChatSession, and ChatLogger via their public APIs.
"""

from pathlib import Path

from utils.ui import (
    print_success,
    print_error,
    print_warning,
    print_section_header,
    get_confirmation,
    display_chat_history,
)


def handle_status(chat, text_streaming: bool) -> None:
    """Show current chat metadata such as persona, subject, model, and streaming.

    Args:
        chat: ChatSession instance with current state.
        text_streaming: Flag indicating whether streaming is enabled.
    """
    print_section_header("Status")
    persona = getattr(chat, "current_persona", None) or "None"
    subject = getattr(chat, "current_subject", None) or "None"
    model = getattr(chat, "model", "unknown")

    print(f"Persona: {persona}")
    print(f"Subject: {subject}")
    print(f"Model:   {model}")
    print(f"Streaming: {'on' if text_streaming else 'off'}")


def handle_clear_history(chat) -> None:
    """Clear the in-memory conversation history for the current chat session.

    Args:
        chat: ChatSession instance to clear.
    """
    chat.clear_history()
    print_success("Conversation history cleared.")


def _select_chat_from_list(chats):
    """Helper to let the user pick a chat from a list by index.

    Args:
        chats: List of tuples describing chats. For /c_history this is:
               (subject_name, chat_filename, file_path)
               For /c_history_<subject> this is:
               (chat_filename, file_path)

    Returns:
        The selected tuple from `chats`, or None if selection was cancelled
        or invalid.
    """
    if not chats:
        print_warning("No chats found.")
        return None

    for idx, entry in enumerate(chats, start=1):
        if len(entry) == 3:
            subject_name, chat_filename, _ = entry
            print(f"{idx}. [{subject_name}] {chat_filename}")
        else:
            chat_filename, _ = entry
            print(f"{idx}. {chat_filename}")

    choice = input("\nEnter number to view (or press Enter to cancel): ").strip()
    if not choice:
        print_warning("Selection cancelled.")
        return None

    if not choice.isdigit():
        print_error("Invalid selection.")
        return None

    index = int(choice)
    if not (1 <= index <= len(chats)):
        print_error("Selection out of range.")
        return None

    return chats[index - 1]


def handle_chat_history(retriever, chat) -> None:
    """Handle /c_history: list and preview chats across all subjects.

    Shows a numbered list of all chat files returned by
    SubjectRetriever.list_all_chats, then lets the user choose one
    to load and preview its contents in the terminal.

    Args:
        retriever: SubjectRetriever used to discover chat files.
        chat: ChatSession instance (used only for display context).
    """
    print_section_header("All Chats")
    chats = retriever.list_all_chats()
    selected = _select_chat_from_list(chats)
    if not selected:
        return

    subject_name, chat_filename, file_path = selected
    print_success(f"Loading chat '{chat_filename}' from subject '{subject_name}'")

    history = retriever.load_chat_file(file_path)
    if not history:
        print_warning("Chat file is empty or could not be parsed.")
        return

    display_chat_history(history)


def handle_chat_history_by_subject(retriever, chat, subject_name: str) -> None:
    """Handle /c_history_<subject>: list and preview chats for one subject.

    Args:
        retriever: SubjectRetriever used to discover chat files.
        chat: ChatSession instance (used only for display context).
        subject_name: Name of the subject whose chats should be listed.
    """
    if not subject_name:
        print_error("Usage: /c_history_[subject]")
        return

    print_section_header(f"Chats for subject: {subject_name}")
    chats = retriever.list_chats_by_subject(subject_name)
    selected = _select_chat_from_list(chats)
    if not selected:
        return

    chat_filename, file_path = selected
    print_success(f"Loading chat '{chat_filename}'")

    history = retriever.load_chat_file(file_path)
    if not history:
        print_warning("Chat file is empty or could not be parsed.")
        return

    display_chat_history(history)


def handle_delete_chat(retriever, chat, idx: str) -> None:
    """Handle /c_delete: delete a chat by its index from the global list.

    This presents the same list as /c_history, but deletes the chosen
    chat file instead of viewing it.

    Args:
        retriever: SubjectRetriever used to list and delete chat files.
        chat: ChatSession instance (unused but kept for symmetry).
        idx: Optional index argument provided after the command. If empty,
             the user will be prompted interactively.
    """
    chats = retriever.list_all_chats()
    if not chats:
        print_warning("No chats found.")
        return

    if idx and idx.isdigit():
        index = int(idx)
        if not (1 <= index <= len(chats)):
            print_error("Index out of range.")
            return
        selected = chats[index - 1]
    else:
        print_section_header("Delete Chat")
        selected = _select_chat_from_list(chats)
        if not selected:
            return

    subject_name, chat_filename, file_path = selected

    if not get_confirmation(
        f"Are you sure you want to delete '{chat_filename}' from subject '{subject_name}'?"
    ):
        print_warning("Delete chat cancelled.")
        return

    success = retriever.delete_chat_file(subject_name, chat_filename)
    if success:
        print_success(f"Deleted chat '{chat_filename}'.")
    else:
        print_error(f"Failed to delete chat '{chat_filename}'.")


def handle_chat_move(retriever, chat, _unused) -> None:
    """Handle /c_move: move a chat file from one subject to another.

    The user is first shown a list of all chats across subjects, selects
    one, and is then prompted for a target subject name. A new subject
    folder is created if needed.

    Args:
        retriever: SubjectRetriever used to list and move chat files.
        chat: ChatSession instance (unused but kept for symmetry).
        _unused: Placeholder arg (CommandHandler currently passes None).
    """
    chats = retriever.list_all_chats()
    if not chats:
        print_warning("No chats found.")
        return

    print_section_header("Move Chat")
    selected = _select_chat_from_list(chats)
    if not selected:
        return

    source_subject, chat_filename, file_path = selected
    target_subject = input("Enter target subject name: ").strip()

    if not target_subject:
        print_error("Target subject name cannot be empty.")
        return

    if not get_confirmation(
        f"Move '{chat_filename}' from '{source_subject}' to '{target_subject}'?"
    ):
        print_warning("Move chat cancelled.")
        return

    success = retriever.move_chat_to_subject(source_subject, chat_filename, target_subject)
    if success:
        print_success(f"Moved '{chat_filename}' to subject '{target_subject}'.")
    else:
        print_error(f"Failed to move chat '{chat_filename}'.")


def handle_streaming_toggle(current_value: bool) -> bool:
    """Toggle the streaming preference and report the new state.

    Args:
        current_value: Current boolean value of the streaming flag.

    Returns:
        The toggled boolean value.
    """
    new_value = not current_value
    state = "enabled" if new_value else "disabled"
    print_success(f"Text streaming {state}.")
    return new_value


def handle_exit(chat, logger) -> bool:
    """Handle /exit: perform any final actions and signal the app to quit.

    Currently this just prints a message and returns True so that the
    main loop can terminate. It is a placeholder to hook in any future
    "save on exit" logic using the logger if needed.

    Args:
        chat: ChatSession instance (currently unused).
        logger: ChatLogger instance (currently unused).

    Returns:
        True, indicating the caller should exit the application.
    """
    print_success("Exiting chat. Goodbye!")
    return True
