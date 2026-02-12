from retriever import SubjectRetriever
from chat import ChatSession
from logger import ChatLogger

def print_welcome():
    """Print welcome message and instructions"""
    print("=" * 60)
    print("Subject-Aware Chat Application (Ollama + Llama3)")
    print("=" * 60)
    print()
    print("• Persona: <name>, Subject: <name>, <prompt>")
    print("  - Load persona and subject, then send prompt")
    print("• /personas - List available personas")
    print("• /subjects - List available subjects")
    print("• /status - Show current persona and subject")
    print("• /clear - Clear conversation history")
    print("• /exit - Save and exit")
    print("=" * 60)

def main():
    # Initialize components
    retriever = SubjectRetriever(basepath=".")
    chat = ChatSession(model="llama3")  # Using llama3 model
    logger = ChatLogger(basepath=".")
    
    print_welcome()
    
    # Main interaction loop
    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "/exit":
                # Save chat log if there's an active subject
                if chat.current_subject and chat.conversation_history:
                    save = input(f"Save chat to '{chat.current_subject}'? (y/n): ").lower()
                    if save == 'y':
                        log_file = logger.save_chat(chat.current_subject, chat.conversation_history)
                        print(f"✓ Chat saved to {log_file}")
                print("Goodbye!")
                break
            
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
            
            # Check if user is setting persona/subject
            persona, subject, prompt = retriever.parse_subject_command(user_input)
            
            if persona and subject:
                # Load new subject
                try:
                    system_prompt = retriever.build_system_prompt(persona, subject)
                    chat.set_system_prompt(system_prompt)
                    chat.set_subject_info(persona, subject)
                    chat.clear_history()  # Start fresh with new subject
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
            
            # Check if subject is set before allowing chat
            if not chat.current_subject:
                print("Please set a persona and subject first.")
                print("Example: Persona: writer, Subject: fantasy_story")
                continue
            
            # Send message and get response
            response = chat.send_message(user_input)
            print(f"\n{response}")
            
        except KeyboardInterrupt:
            print("\n⚠ Use /exit to save and quit.")
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()
