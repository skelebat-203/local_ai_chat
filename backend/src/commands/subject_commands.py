"""Subject and persona management command handlers."""

from utils.ui import (
    print_success, print_error, print_warning,
    get_user_input, get_confirmation
)


def handle_list_personas(retriever):
    """Handle /personas command."""
    personas = retriever.list_personas()
    print(f"Available personas: {', '.join(personas)}")


def handle_list_subjects(retriever):
    """Handle /subjects command."""
    subjects = retriever.list_subjects()
    print(f"Available subjects: {', '.join(subjects)}")


def handle_new_subject(retriever, chat, subject_name):
    """Handle /new_subject command."""
    if not subject_name:
        print_error("Usage: /new_subject [subject_name]")
        return False

    try:
        subject_created = retriever.create_subject_folder(subject_name)
        if subject_created:
            print_success(f"'{subject_name}' created.")

            if get_confirmation("Do you want to add subject instructions?"):
                print("\nThe next prompt will be saved as instructions for this subject.")
                print("Enter your instructions (press Enter when done):\n")

                instructions = get_user_input("> ")

                if instructions:
                    retriever.save_subject_instructions(subject_name, instructions)
                    print_success("Instructions saved.")
                else:
                    print_warning("No instructions provided.")

                print(f"\nWhat is your first prompt for '{subject_name}'?")
            else:
                print(f"\nWhat is your first prompt for '{subject_name}'?")

            system_prompt = retriever.build_system_prompt(retriever.default_persona, subject_name)
            chat.set_system_prompt(system_prompt)
            chat.set_subject_info(retriever.default_persona, subject_name)
            chat.clear_history()
            print_success(f"Loaded Subject: {subject_name}")
            return True
        else:
            print_error(f"Subject '{subject_name}' already exists.")
            return False

    except Exception as e:
        print_error(f"Error creating subject: {e}")
        return False


def handle_new_persona(retriever, chat, persona_name):
    """Handle /new_persona command."""
    if not persona_name:
        print("Usage: /new_persona [persona_name]")
        return False

    if not persona_name.replace('_', '').replace('-', '').isalnum():
        print_error("Persona name must be alphanumeric (underscores and hyphens allowed)")
        return False

    persona_file = retriever.personas_path / f"{persona_name.lower()}.md"
    if persona_file.exists():
        print_error(f"Persona '{persona_name}' already exists")
        return False

    try:
        retriever.personas_path.mkdir(parents=True, exist_ok=True)
        print(f"{persona_name} created.")
        print("The next prompt will be saved as instructions for this persona.")

        persona_description = get_user_input("\n> ")

        if not persona_description:
            print_error("Persona description cannot be empty")
            return False

        with open(persona_file, 'w', encoding='utf-8') as f:
            f.write(persona_description)

        print("\nPersona description saved.")

        current_subject = chat.current_subject or retriever.default_subject
        system_prompt = retriever.build_system_prompt(persona_name, current_subject)
        chat.set_system_prompt(system_prompt)
        chat.set_subject_info(persona_name, current_subject)
        chat.clear_history()

        print_success(f"Loaded Persona: {persona_name}")
        print(f"What is your first prompt for {persona_name}?")
        return True

    except Exception as e:
        print_error(f"Error creating persona: {e}")
        return False


def handle_persona_subject_switch(retriever, chat, user_input):
    """Handle persona/subject switching via 'Persona: X, Subject: Y, prompt' format."""
    persona, subject, prompt = retriever.parse_subject_command(user_input)

    if not (persona and subject):
        return None

    try:
        actual_persona = persona
        actual_subject = subject

        persona_file = retriever.personas_path / f"{persona.lower()}.md"
        if not persona_file.exists():
            print_warning(f"Persona '{persona}' not found, using default")
            print(f"\t- You can use '/new_persona {persona}' to create a new persona")
            actual_persona = retriever.default_persona

        subject_folder = retriever.subjects_path / subject
        if not subject_folder.exists():
            print_warning(f"Subject '{subject}' not found, using default")
            print(f"\t- You can use '/new_subject {subject}' to create a new subject")
            actual_subject = retriever.default_subject

        system_prompt = retriever.build_system_prompt(actual_persona, actual_subject)
        chat.set_system_prompt(system_prompt)
        chat.set_subject_info(actual_persona, actual_subject)
        chat.clear_history()
        print_success(f"Loaded Persona: {actual_persona}")
        print_success(f"Loaded Subject: {actual_subject}")

        return prompt if prompt else ""

    except FileNotFoundError as e:
        print_error(f"Error: {e}")
        return None
