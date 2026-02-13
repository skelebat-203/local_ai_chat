from retriever import SubjectRetriever
from chat import ChatSession
from logger import ChatLogger
import sys

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
• /new_subject [subject_name]- Create a new subject by enteringhte command followed by the subject name
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
    # Print welcome message and instructions
    print(welcome)

def main():
    # Initialize components
    retriever = SubjectRetriever(basepath=".")
    chat = ChatSession(model="llama3")
    logger = ChatLogger(basepath=".")
    
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
                # Save chat log if there's conversation history
                if chat.current_subject and chat.conversation_history:
                    save = input(f"Save chat to '{chat.current_subject}'? (y/n): ").lower()
                    if save == 'y':
                        log_file = logger.save_chat(chat.current_subject, chat.conversation_history)
                        print(f"✓ Chat saved to {log_file}")
                        
                        # Delete original file if this was a resumed chat
                        if hasattr(chat, 'original_chat_file') and chat.original_chat_file.exists():
                            chat.original_chat_file.unlink()
                            print(f"✓ Removed old chat file: {chat.original_chat_file.name}")
                print("Goodbye!")
                break

            elif user_input.lower() == "/help":
                print(commands)
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
                print(f"Persona: {persona}")
                print(f"Current Subject: {subject}")
                print(f"Model: {chat.model}")
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
            
            elif user_input.lower().startswith("/new_subject"):
                # Extract subject name
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2 or not parts[1].strip():
                    print("✗ Usage: /new_subject [subject_name]")
                    continue
                
                subject_name = parts[1].strip()
                
                # Create subject folder
                try:
                    subject_created = retriever.create_subject_folder(subject_name)
                    if subject_created:
                        print(f"✓ '{subject_name}' created.")
                        
                        # Ask about instructions
                        add_instructions = input("Do you want to add subject instructions? (y/n): ").lower().strip()
                        
                        if add_instructions == 'y':
                            print("\nThe next prompt will be saved as instructions for this subject.")
                            print("Enter your instructions (press Enter when done):\n")
                            
                            # Get instructions from user
                            instructions = input("> ").strip()
                            
                            if instructions:
                                # Save instructions
                                retriever.save_subject_instructions(subject_name, instructions)
                                print(f"✓ Instructions saved.")
                            else:
                                print("⚠ No instructions provided.")
                            
                            print(f"\nWhat is your first prompt for '{subject_name}'?")
                        else:
                            print(f"\nWhat is your first prompt for '{subject_name}'?")
                        
                        # Load the new subject
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
                
                print("\n" + "=" * 60)
                print("All Chat History")
                print("=" * 60)
                for idx, chat_info in enumerate(all_chats, 1):
                    subject, filename, file_path = chat_info
                    print(f"{idx}. [{subject}] {filename}")
                print("=" * 60)
                
                # Allow user to select a chat
                try:
                    selection = input("\nEnter number to open chat (or press Enter to cancel): ").strip()
                    if selection:
                        chat_idx = int(selection) - 1
                        if 0 <= chat_idx < len(all_chats):
                            subject, filename, file_path = all_chats[chat_idx]
                            
                            # Load the chat
                            loaded_history = retriever.load_chat_file(file_path)
                            chat.load_history(loaded_history)
                            
                            # Load subject context
                            system_prompt = retriever.build_system_prompt(retriever.default_persona, subject)
                            chat.set_system_prompt(system_prompt)
                            chat.set_subject_info(retriever.default_persona, subject)
                            
                            print(f"\n✓ Loaded chat from {filename}")
                            print(f"✓ Subject: {subject}")
                            print("✓ You can now continue this conversation")
                            
                            # Display the loaded chat history
                            print("\n" + "=" * 60)
                            print("Previous Chat:")
                            print("=" * 60)
                            for msg in loaded_history:
                                role = msg['role'].capitalize()
                                content = msg['content']
                                print(f"\n{role}: {content}")
                            print("\n" + "=" * 60)
                            
                            # Store original file path for deletion later
                            chat.original_chat_file = file_path
                        else:
                            print("Invalid selection.")
                except ValueError:
                    print("Invalid input.")
                continue
            
            elif user_input.lower().startswith("/chat_history_"):
                subject_name = user_input[14:].strip()  # Extract subject after /chat_history_
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
                
                # Allow user to select a chat
                try:
                    selection = input("\nEnter number to open chat (or press Enter to cancel): ").strip()
                    if selection:
                        chat_idx = int(selection) - 1
                        if 0 <= chat_idx < len(chats):
                            filename, file_path = chats[chat_idx]
                            
                            # Load the chat
                            loaded_history = retriever.load_chat_file(file_path)
                            chat.load_history(loaded_history)
                            
                            # Load subject context
                            system_prompt = retriever.build_system_prompt(retriever.default_persona, subject_name)
                            chat.set_system_prompt(system_prompt)
                            chat.set_subject_info(retriever.default_persona, subject_name)
                            
                            print(f"\n✓ Loaded chat from {filename}")
                            print(f"✓ Subject: {subject_name}")
                            print("✓ You can now continue this conversation")
                            
                            # Display the loaded chat history
                            print("\n" + "=" * 60)
                            print("Previous Chat:")
                            print("=" * 60)
                            for msg in loaded_history:
                                role = msg['role'].capitalize()
                                content = msg['content']
                                print(f"\n{role}: {content}")
                            print("\n" + "=" * 60)
                            
                            # Store original file path for deletion later
                            chat.original_chat_file = file_path
                        else:
                            print("Invalid selection.")
                except ValueError:
                    print("Invalid input.")
                continue
            
            # Check if user is setting persona/subject
            persona, subject, prompt = retriever.parse_subject_command(user_input)
            
            if persona and subject:
                # Load new subject
                try:
                    system_prompt = retriever.build_system_prompt(persona, subject)
                    chat.set_system_prompt(system_prompt)
                    chat.set_subject_info(persona, subject)
                    chat.clear_history()
                    print(f"✓ Loaded Persona: {persona}")
                    print(f"✓ Loaded Subject: {subject}")
                    
                    # If there's a prompt after the subject setting, process it
                    if prompt:
                        user_input = prompt
                    else:
                        continue
                except FileNotFoundError as e:
                    print(f"✗ Error: {e}")
                    continue
            
            # Send message and stream response
            print()  # New line before streaming response
            for chunk in chat.send_message_stream(user_input):
                print(chunk, end='', flush=True)
            print()  # New line after streaming completes
            
        except KeyboardInterrupt:
            print("\n⚠ Use /exit to save and quit.")
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()
