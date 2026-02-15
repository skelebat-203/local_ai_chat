import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.retriever import SubjectRetriever
from core.chat import ChatSession
from core.logger import ChatLogger

commands = f'''
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

welcome = f'''
{"=" * 60}
Subject-Aware Chat Application (Ollama + Llama3)
{"=" * 60}
Format:
Persona: <name>, Subject: <name>, <prompt>
\t- Load persona and subject, then send prompt
Note: You can chat immediately without setting persona/subject.
{commands}
'''

def print_welcome():
    print(welcome)

def main():
    # Get the base path (project root: backend/)
    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"
    
    # Initialize components with new data path
    retriever = SubjectRetriever(basepath=str(data_path))
    chat = ChatSession(model="llama3")
    logger = ChatLogger(basepath=str(data_path))

    # Initialize text streaming preference (default: on)
    text_streaming = True

    # Initialize with defaults immediately
    try:
        default_system_prompt = retriever.build_system_prompt()
        chat.set_system_prompt(default_system_prompt)
        chat.set_subject_info(retriever.default_persona, retriever.default_subject)
    except Exception as e:
        print(f"⚠ Warning: Could not load defaults: {e}")

    print_welcome()

    # Main interaction loop
    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue

            # Handle commands
            if user_input.lower() == "/exit":
                if chat.current_subject and chat.conversation_history:
                    save = input(f"Save chat to '{chat.current_subject}'? (y/n): ").lower()
                    if save == 'y':
                        log_file = logger.save_chat(chat.current_subject, chat.conversation_history)
                        print(f"✓ Chat saved to {log_file}")

                        if hasattr(chat, 'original_chat_file') and chat.original_chat_file.exists():
                            chat.original_chat_file.unlink()
                            print(f"✓ Removed old chat file: {chat.original_chat_file.name}")
                print("Goodbye!")
                break

            elif user_input.lower() == "/help":
                print(commands)
                continue

            elif user_input.lower() == "/pref_streaming":
                current_state = "on" if text_streaming else "off"
                target_state = "off" if text_streaming else "on"

                response = input(f"Turn text streaming {target_state}? 'y' / 'n'? ").strip().lower()

                if response == 'y':
                    text_streaming = not text_streaming
                    new_state = "on" if text_streaming else "off"
                    print(f"Text streaming is now {new_state}. What would you like to discuss?")
                elif response == 'n':
                    print("No change. What would you like to discuss?")
                else:
                    print("Invalid response. No change made.")

                continue

            elif user_input.lower() == "/personas":
                personas = retriever.list_personas()
                print(f"Available personas: {', '.join(personas)}")
                continue

            elif user_input.lower() == "/subjects":
                subjects = retriever.list_subjects()
                print(f"Available subjects: {', '.join(subjects)}")
                continue

            elif user_input.lower() == "/status":
                persona = chat.current_persona or "None"
                subject = chat.current_subject or "None"
                streaming_status = "on" if text_streaming else "off"
                print(f"Persona: {persona}")
                print(f"Current Subject: {subject}")
                print(f"Model: {chat.model}")
                print(f"Text Streaming: {streaming_status}")
                continue

            elif user_input.lower() == "/clear":
                chat.clear_history()
                print("✓ Conversation history cleared")
                continue

            elif user_input.lower() == "/chat_history":
                all_chats = retriever.list_all_chats()
                if not all_chats:
                    print("No chat history found.")
                    continue

                print("\n" + "=" * 60)
                print("All Chat History")
                print("=" * 60)
                for idx, chat_info in enumerate(all_chats, 1):
                    subject, filename, file_path = chat_info
                    print(f"{idx}. [{subject}] {filename}")
                print("=" * 60)

                try:
                    selection = input("\nEnter number to open chat (or press Enter to cancel): ").strip()
                    if selection:
                        chat_idx = int(selection) - 1
                        if 0 <= chat_idx < len(all_chats):
                            subject, filename, file_path = all_chats[chat_idx]

                            loaded_history = retriever.load_chat_file(file_path)
                            chat.load_history(loaded_history)

                            system_prompt = retriever.build_system_prompt(retriever.default_persona, subject)
                            chat.set_system_prompt(system_prompt)
                            chat.set_subject_info(retriever.default_persona, subject)

                            print(f"\n✓ Loaded chat from {filename}")
                            print(f"✓ Subject: {subject}")
                            print("✓ You can now continue this conversation")

                            print("\n" + "=" * 60)
                            print("Previous Chat:")
                            print("=" * 60)
                            for msg in loaded_history:
                                role = msg['role'].capitalize()
                                content = msg['content']
                                print(f"\n{role}: {content}")
                            print("\n" + "=" * 60)

                            chat.original_chat_file = file_path
                        else:
                            print("Invalid selection.")
                except ValueError:
                    print("Invalid input.")
                continue

            elif user_input.lower().startswith("/chat_history_"):
                subject_name = user_input[14:].strip()
                if not subject_name:
                    print("Please specify a subject: /chat_history_[subject]")
                    continue

                chats = retriever.list_chats_by_subject(subject_name)
                if not chats:
                    print(f"No chat history found for subject '{subject_name}'.")
                    continue

                print("\n" + "=" * 60)
                print(f"Chat History for: {subject_name}")
                print("=" * 60)
                for idx, chat_info in enumerate(chats, 1):
                    filename, file_path = chat_info
                    print(f"{idx}. {filename}")
                print("=" * 60)

                try:
                    selection = input("\nEnter number to open chat (or press Enter to cancel): ").strip()
                    if selection:
                        chat_idx = int(selection) - 1
                        if 0 <= chat_idx < len(chats):
                            filename, file_path = chats[chat_idx]

                            loaded_history = retriever.load_chat_file(file_path)
                            chat.load_history(loaded_history)

                            system_prompt = retriever.build_system_prompt(retriever.default_persona, subject_name)
                            chat.set_system_prompt(system_prompt)
                            chat.set_subject_info(retriever.default_persona, subject_name)

                            print(f"\n✓ Loaded chat from {filename}")
                            print(f"✓ Subject: {subject_name}")
                            print("✓ You can now continue this conversation")

                            print("\n" + "=" * 60)
                            print("Previous Chat:")
                            print("=" * 60)
                            for msg in loaded_history:
                                role = msg['role'].capitalize()
                                content = msg['content']
                                print(f"\n{role}: {content}")
                            print("\n" + "=" * 60)

                            chat.original_chat_file = file_path
                        else:
                            print("Invalid selection.")
                except ValueError:
                    print("Invalid input.")
                continue

            elif user_input.lower().startswith("/new_subject"):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2 or not parts[1].strip():
                    print("✗ Usage: /new_subject [subject_name]")
                    continue

                subject_name = parts[1].strip()

                try:
                    subject_created = retriever.create_subject_folder(subject_name)
                    if subject_created:
                        print(f"✓ '{subject_name}' created.")

                        add_instructions = input("Do you want to add subject instructions? (y/n): ").lower().strip()

                        if add_instructions == 'y':
                            print("\nThe next prompt will be saved as instructions for this subject.")
                            print("Enter your instructions (press Enter when done):\n")

                            instructions = input("> ").strip()

                            if instructions:
                                retriever.save_subject_instructions(subject_name, instructions)
                                print(f"✓ Instructions saved.")
                            else:
                                print("⚠ No instructions provided.")

                            print(f"\nWhat is your first prompt for '{subject_name}'?")
                        else:
                            print(f"\nWhat is your first prompt for '{subject_name}'?")

                        system_prompt = retriever.build_system_prompt(retriever.default_persona, subject_name)
                        chat.set_system_prompt(system_prompt)
                        chat.set_subject_info(retriever.default_persona, subject_name)
                        chat.clear_history()
                        print(f"✓ Loaded Subject: {subject_name}")
                    else:
                        print(f"✗ Subject '{subject_name}' already exists.")

                except Exception as e:
                    print(f"✗ Error creating subject: {e}")

                continue

            elif user_input.lower().startswith("/new_persona"):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print("Usage: /new_persona [persona_name]")
                    continue

                persona_name = parts[1].strip()

                if not persona_name.replace('_', '').replace('-', '').isalnum():
                    print("✗ Error: Persona name must be alphanumeric (underscores and hyphens allowed)")
                    continue

                persona_file = retriever.personas_path / f"{persona_name.lower()}.md"
                if persona_file.exists():
                    print(f"✗ Error: Persona '{persona_name}' already exists")
                    continue

                try:
                    retriever.personas_path.mkdir(parents=True, exist_ok=True)
                    print(f"{persona_name} created.")
                    print("The next prompt will be saved as instructions for this persona.")

                    persona_description = input("\n> ").strip()

                    if not persona_description:
                        print("✗ Error: Persona description cannot be empty")
                        continue

                    with open(persona_file, 'w', encoding='utf-8') as f:
                        f.write(persona_description)

                    print(f"\nPersona description saved.")

                    current_subject = chat.current_subject or retriever.default_subject
                    system_prompt = retriever.build_system_prompt(persona_name, current_subject)
                    chat.set_system_prompt(system_prompt)
                    chat.set_subject_info(persona_name, current_subject)
                    chat.clear_history()

                    print(f"✓ Loaded Persona: {persona_name}")
                    print(f"What is your first prompt for {persona_name}?")

                except Exception as e:
                    print(f"✗ Error creating persona: {e}")

                continue

            # Check if user is setting persona/subject
            persona, subject, prompt = retriever.parse_subject_command(user_input)

            if persona and subject:
                try:
                    actual_persona = persona
                    actual_subject = subject
                    
                    persona_file = retriever.personas_path / f"{persona.lower()}.md"
                    if not persona_file.exists():
                        print(f"⚠ Persona '{persona}' not found, using default")
                        print(f"\t- You can use '/new_persona {persona}' to create a new persona")
                        actual_persona = retriever.default_persona
                    
                    subject_folder = retriever.subjects_path / subject
                    if not subject_folder.exists():
                        print(f"⚠ Subject '{subject}' not found, using default")
                        print(f"\t- You can use '/new_subject {subject}' to create a new subject")
                        actual_subject = retriever.default_subject
                    
                    system_prompt = retriever.build_system_prompt(actual_persona, actual_subject)
                    chat.set_system_prompt(system_prompt)
                    chat.set_subject_info(actual_persona, actual_subject)
                    chat.clear_history()
                    print(f"✓ Loaded Persona: {actual_persona}")
                    print(f"✓ Loaded Subject: {actual_subject}")

                    if prompt:
                        user_input = prompt
                    else:
                        continue
                except FileNotFoundError as e:
                    print(f"✗ Error: {e}")
                    continue

            print()

            if text_streaming:
                for chunk in chat.send_message_stream(user_input):
                    print(chunk, end='', flush=True)
                print()
            else:
                response = chat.send_message(user_input)
                print(response)

        except KeyboardInterrupt:
            print("\n⚠ Use /exit to save and quit.")
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()
