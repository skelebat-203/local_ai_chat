"""UI utilities for terminal interface."""

COMMANDS_TEXT = f'''
{"=" * 60}
Commands:
• /help - List all commands
• /personas - List available personas
• /subjects - List available subjects
• /status - Show current persona and subject
• /clear - Clear conversation history
• /chat_history - List all chats across subjects
• /chat_history_[subject] - List chats for specific subject
• /new_subject [subject_name]- Create a new subject by entering the command followed by the subject name
• /new_persona [persona_name] - Create a new persona by entering the command followed by the persona name
• /pref_streaming - Toggle text streaming on/off
• /exit - Save and exit
{"=" * 60}
'''

WELCOME_TEXT = f'''
{"=" * 60}
Subject-Aware Chat Application (Ollama + Llama3)
{"=" * 60}
Format:
Persona: <name>, Subject: <name>, <prompt>
\t- Load persona and subject, then send prompt
Note: You can chat immediately without setting persona/subject.
• /help - List all commands
• /exit - Save and exit
'''


def print_welcome():
    """Print welcome message."""
    print(WELCOME_TEXT)


def print_commands():
    """Print available commands."""
    print(COMMANDS_TEXT)


def print_section_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_success(message):
    """Print success message."""
    print(f"✓ {message}")


def print_error(message):
    """Print error message."""
    print(f"✗ {message}")


def print_warning(message):
    """Print warning message."""
    print(f"⚠ {message}")


def get_user_input(prompt="\n> "):
    """Get user input with default prompt."""
    return input(prompt).strip()


def get_confirmation(message):
    """Get yes/no confirmation from user."""
    response = input(f"{message} (y/n): ").lower().strip()
    return response == 'y'


def display_chat_history(history):
    """Display formatted chat history."""
    print_section_header("Previous Chat:")
    for msg in history:
        role = msg['role'].capitalize()
        content = msg['content']
        print(f"\n{role}: {content}")
    print("\n" + "=" * 60)
