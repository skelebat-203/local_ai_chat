import ollama


class ChatSession:
    """Manage a single conversational session with an Ollama model.

    This class tracks conversation history, the current system prompt,
    and active persona/subject metadata. It provides helper methods to
    send messages (with or without streaming) and to switch models.
    """

    def __init__(self, model: str = "llama3"):
        """Initialize a new chat session.

        Args:
            model: Name of the Ollama model to use for this session.
        """
        self.conversation_history = []
        self.system_prompt = ""
        self.current_persona = None
        self.current_subject = None
        self.model = model

    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt for this session.

        Args:
            prompt: Full system prompt text to send with each request.
        """
        self.system_prompt = prompt

    def set_subject_info(self, persona: str, subject: str) -> None:
        """Store the current persona and subject metadata.

        Args:
            persona: Name of the active persona.
            subject: Name of the active subject.
        """
        self.current_persona = persona
        self.current_subject = subject

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history.

        Args:
            role: Message sender role ("user" or "assistant").
            content: Message text content.
        """
        self.conversation_history.append({"role": role, "content": content})

    def get_full_context(self) -> dict:
        """Return the full context payload for API calls.

        Returns:
            A dict with the current system prompt and conversation history.
        """
        return {
            "system_prompt": self.system_prompt,
            "history": self.conversation_history,
        }

    def send_message(self, user_message: str) -> str:
        """Send a message to Ollama and return the full response.

        The user's message is appended to history, the system prompt
        is prepended (if set), and the assistant response is stored.

        Args:
            user_message: The text of the user message to send.

        Returns:
            Assistant response content, or an error message string if
            the call fails.
        """
        self.add_message("user", user_message)

        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.extend(self.conversation_history)

        try:
            response = ollama.chat(model=self.model, messages=messages)
            response_content = response["message"]["content"]
            self.add_message("assistant", response_content)
            return response_content
        except Exception as e:
            error_msg = f"Error communicating with Ollama: {str(e)}"
            print(f"✗ {error_msg}")
            return error_msg

    def send_message_stream(self, user_message: str):
        """Send a message and yield the response as a stream of chunks.

        This behaves like send_message, but yields partial response text
        as it arrives. The full assistant response is stored in history
        once streaming completes.

        Args:
            user_message: The text of the user message to send.

        Yields:
            Small string chunks of the assistant response.
        """
        self.add_message("user", user_message)

        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.extend(self.conversation_history)

        try:
            full_response = ""
            for chunk in ollama.chat(model=self.model, messages=messages, stream=True):
                content = chunk["message"]["content"]
                full_response += content
                yield content

            self.add_message("assistant", full_response)
        except Exception as e:
            error_msg = f"Error communicating with Ollama: {str(e)}"
            print(f"✗ {error_msg}")
            yield error_msg

    def clear_history(self) -> None:
        """Clear the stored conversation history.

        Useful after switching persona/subject or models.
        """
        self.conversation_history = []

    def load_history(self, conversation_history) -> None:
        """Load an existing conversation history into this session.

        Args:
            conversation_history: List of message dictionaries to use
                as the new history.
        """
        self.conversation_history = conversation_history

    def get_history_for_logging(self) -> str:
        """Format conversation history as a plain text log string.

        Returns:
            A human‑readable string suitable for writing to log files.
        """
        log_text = []
        for msg in self.conversation_history:
            role = msg["role"].capitalize()
            content = msg["content"]
            log_text.append(f"{role}:\n{content}\n")
        return "\n".join(log_text)

    def set_model(self, model_name: str) -> None:
        """Swap the underlying Ollama model for this session.

        Args:
            model_name: New model name to use for subsequent calls.
        """
        self.model = model_name
        print(f"[info] Model switched to: {model_name}")
