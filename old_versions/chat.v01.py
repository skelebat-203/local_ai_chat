import ollama
from logger import start_session, log_message  # NEW

def main():
    print("Local chat with llama3. Type /exit to quit.\n")

    # start markdown logging
    log_path = start_session()  # NEW

    # keep conversation history for the model
    messages = []

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() == "/exit":
            print("Goodbye!")
            break

        # log user message
        log_message(log_path, "User", user_input)  # NEW

        messages.append({"role": "user", "content": user_input})

        response = ollama.chat(
            model="llama3",
            messages=messages,
        )

        assistant_reply = response["message"]["content"]
        print(f"Assistant: {assistant_reply}\n")

        # log assistant reply
        log_message(log_path, "Assistant", assistant_reply)  # NEW

        messages.append({"role": "assistant", "content": assistant_reply})

if __name__ == "__main__":
    main()
