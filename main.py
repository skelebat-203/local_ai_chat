"""
Chat Application - Main Entry Point
Orchestrates persona/context loading and chat session management
"""
from retriever import ContextRetriever
from chat import ChatSession
from logger import ChatLogger

def print_welcome():
    """Print welcome message and instructions"""
    print("=" * 60)
    print("Context-Aware Chat Application (Ollama + Llama3)")
    print("=" * 60)
    print("\nCommands:")
    print("  Persona = <name>, Context = <name>, <prompt>")
    print("    - Load persona and context, then send prompt")
    print("  /personas - List available personas")
    print("  /contexts - List available contexts")
    print("  /status   - Show current persona and context")
    print("  /clear    - Clear conversation history")
    print("  /exit     - Save and exit")
    print("\n" + "=" * 60 + "\n")


def main():
    # Initialize components
    retriever = ContextRetriever(base_path=".")
    chat = ChatSession(model="llama3")  # Using llama3 model
    logger = ChatLogger(base_path=".")

    print_welcome()

    # Main interaction loop
    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() == "/exit":
                # Save chat log if there's an active context
                if chat.current_context and chat.conversation_history:
                    save = input(f"\nSave chat to '{chat.current_context}'? (y/n): ").lower()
                    if save == 'y':
                        log_file = logger.save_chat(
                            chat.current_context,
                            chat.conversation_history
                        )
                        print(f"✓ Chat saved to {log_file}")
                print("\nGoodbye!")
                break

            elif user_input.lower() == "/personas":
                personas = retriever.list_personas()
                print(f"\nAvailable personas: {', '.join(personas)}")
                continue

            elif user_input.lower() == "/contexts":
                contexts = retriever.list_contexts()
                print(f"\nAvailable contexts: {', '.join(contexts)}")
                continue

            elif user_input.lower() == "/status":
                persona = chat.current_persona or "None"
                context = chat.current_context or "None"
                print(f"\nCurrent Persona: {persona}")
                print(f"Current Context: {context}")
                print(f"Model: {chat.model}")
                continue

            elif user_input.lower() == "/clear":
                chat.clear_history()
                print("\n✓ Conversation history cleared")
                continue

            # Check if user is setting persona/context
            persona, context, prompt = retriever.parse_context_command(user_input)

            if persona and context:
                # Load new context
                try:
                    system_prompt = retriever.build_system_prompt(persona, context)
                    chat.set_system_prompt(system_prompt)
                    chat.set_context_info(persona, context)
                    chat.clear_history()  # Start fresh with new context

                    print(f"\n✓ Loaded Persona: {persona}")
                    print(f"✓ Loaded Context: {context}")

                    # If there's a prompt after the context setting, process it
                    if prompt:
                        user_input = prompt
                    else:
                        continue

                except FileNotFoundError as e:
                    print(f"\n✗ Error: {e}")
                    continue

            # Check if context is set before allowing chat
            if not chat.current_context:
                print("\n⚠ Please set a persona and context first.")
                print("Example: Persona = writer, Context = fantasy_story")
                continue

            # Send message and get response
            response = chat.send_message(user_input)
            print(f"\nAssistant: {response}")

        except KeyboardInterrupt:
            print("\n\nInterrupted. Use /exit to save and quit.")
        except Exception as e:
            print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
