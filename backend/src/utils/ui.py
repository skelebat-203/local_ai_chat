"""UI utilities for the terminal interface.

This module contains helper functions for:
    - Printing formatted messages and section headers
    - Rendering welcome and commands help text
    - Collecting user input with prompt_toolkit
    - Displaying previous chat history in a readable format
"""

from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from core import __version__

COMMANDS_TEXT = f'''
{"=" * 60}
Commands:
Keyboard Navigation 
• UP, DOWN, LEFT, and Right arrow keys - navigate throught the prompt
• ALT + ENTER - Submit a prompt or Save and exit
• ESC + ENTER - Submit a prompt or Save and exit

General
• /status - Show current meta data for chat
• /clear - Clear conversation history
• /swap - Change AI model 
• /pref_streaming - Toggle text streaming on/off

Create new
• /s_new [subject_name]- Create a new subject by entering the command followed by the subject name
• /p_new [persona_name] - Create a new persona by entering the command followed by the persona name

View / Update
• /help - List all commands
• /p - List available personas
• /s - List available subjects
• /p_inst - view and optionally update persona instructions
• /s_inst - view and optionally update subject instructions
• /c_history - List all chats across subjects
• /c_history_[subject] - List chats for specific subject
• /c_move - Move a chat to a different subject

Delete
• /p_delete [persona_name] - Delete [persona]
• /s_delete [subject_name] - Delete [subject]
• /c_delete [chat_name] - Delete [chat]
{"=" * 60}
'''

WELCOME_TEXT = f'''
{"=" * 60}
Terminal Chat (Ollama + Llama3)
Version: {__version__}
{"=" * 60}
Format:
Persona: <name>, Subject: <name>, <prompt>
\t- Load persona and subject, then send prompt
Note: You can chat immediately without setting persona/subject.
• ALT + ENTER - Submit a prompt or Save and exit
• /help - List all commands
'''


def print_welcome():
    """Print the initial welcome banner for the application."""
    print(WELCOME_TEXT)


def print_commands():
    """Print the list of available slash commands and keyboard shortcuts."""
    print(COMMANDS_TEXT)


def print_section_header(title: str):
    """Print a formatted section header with a title.

    Args:
        title: Text to show as the section title.
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_success(message: str):
    """Print a success message with a checkmark prefix.

    Args:
        message: Message text to display.
    """
    print(f"✓ {message}")


def print_error(message: str):
    """Print an error message with a cross prefix.

    Args:
        message: Message text to display.
    """
    print(f"✗ {message}")


def print_warning(message: str):
    """Print a warning message with a warning icon prefix.

    Args:
        message: Message text to display.
    """
    print(f"⚠ {message}")


def get_user_input(prompt_text: str = "\nUser:\n") -> str:
    """Get multi‑line user input with basic arrow-key navigation.

    Shows a small hint about how to submit, then uses prompt_toolkit
    to collect a (possibly multi‑line) string.

    Args:
        prompt_text: Prompt label shown above the input area.

    Returns:
        The trimmed user input. Returns an empty string on Ctrl+C,
        or the literal string "exit" on EOF (Ctrl+D).
    """
    print("(Press Alt+Enter to submit)")
    try:
        user_input = prompt(prompt_text, multiline=True)
        return user_input.strip()
    except KeyboardInterrupt:
        return ""
    except EOFError:
        return "exit"


def get_confirmation(message: str) -> bool:
    """Prompt the user for a yes/no confirmation.

    Args:
        message: Question to display.

    Returns:
        True if the user answers 'y', False otherwise.
    """
    response = input(f"{message} (y/n): ").lower().strip()
    return response == "y"


def display_chat_history(history):
    """Display formatted chat history in the terminal.

    Args:
        history: Iterable of message dicts with 'role' and 'content' keys.
    """
    print_section_header("Previous Chat:")
    for msg in history:
        role = msg["role"].capitalize()
        content = msg["content"]
        print(f"\n{role}: {content}")
    print("\n" + "=" * 60)
