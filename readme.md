## Local Perplexity clone
There are 3 reasons for this project.
1. I want a local chat interface I control
2. I want to learn some skills
3. I want to brushup on other 

## Updates needed reach version 1 (.v01) milestone
1. Add the ability to see and update subject and persona instructions
2. Add the ability to move chats to other subjects
3. Add the ability to delete chats, subjects, and persona
4. Add "User:\n" and "Assistant:\n" to prompt / response
5. Add chat title
   - On save Title = 1st 10 words of chat.
   - add command "/update_title"
      - display the existing title.
      - user can update the title at anytime.
6. "/chat_history" and "/chat_history [subject]" better formated chat names
   - "/chat_history" Format: [number] [title] [subject] [hh:mm] [yyyy-mm-dd]
   - "/chat_history [subject]" Format: [title] [hh:mm] [yyyy-mm-dd]
   - still want to select a chat by the displayed list item number
7. Milestone 1 complete
   - Milestone 2 will be an app UI. So, Users aren't workin gin terminal.

## Chat Logs
Sort historic chats are sorted by subject.

## Subjects
Holds a number of subject folders: my_novel, coding_project_01, etc.  In each subject folder is a sources_docs folder, links.txt, an instructions.md file, and chat logs related to that subject.

### Structure
Chat_app/
├── subjects/
│   └── [subject_folder]/
│       ├── instructions.md
│       └── chat_[time_stamp].md

### Current Features
- Set subject
- Store subject related chat in subject log
- Retrieve subject instructions and chat logs
- Create undefined subject folder and instructions
- Allow users to chat without defining a subject
- View chats, all and within a specific subject
- Allow creation of new subject

### Upcoming Features
- Allow modification of a  subject
- Allow deletion of a subject
- Sources docs for specific subjects 
- Sources links doc for specific subjects

#### Future structure update
Chat_app/
├── subjects/
│   └── [subject_folder]/
│       ├──[sources_folder]/
│           ├── instructions.md
│           ├── links.md
│           ├── [source_doc]
│           └── [source_doc]
│       └── chat_[time_stamp].md

## Personas
Holds the different types of personalities the user can choose from.

### Structure
Chat_app/
├── personas/
│   └── [persona].md

### Current Features
- Set persona
- Create a default person that I like
- Allow users to chat without defining a persona
- Allow users to create a persona

### Upcoming Features
- Allow modification of a persona
- Allow deletion of a persona

## Python files
### main.py
Manages the app.

### chat.py
Chat logic: sending messages, receiving responses, managing conversation flow
chat.txt is a copy of chat.py meant to do used as a source doc by an AI assistant.

### logger.py
This is curently how I am saving and sorting the current chat once I type /exit

### retriever.py
This currently grabs the persona and context when the user requests it.

### file_watcher.py
Watch for when a python file is saved. When a file is saved. Copy the file in .txt format with a timestamp. Delete old .txt version if one exists. The chat service I am using to help with the project cannot store / "see" .py files. This script exists as a workaround for that bug. 

### Planned App Structure
I'm working on it...  I build a while. If I'm still interested in a few weeks, I fix the structure. I should have this cleaned up / refactored over the next week.

local_chat_bot/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── command_handler.py
│   │   │   ├── chat_commands.py
│   │   │   └── subject_commands.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   ├── logger.py
│   │   │   └── retriever.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── file_watcher.py
│   │   │   └── ui.py
│   │   └── api/
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── data/
│   │   ├── personas/
│   │   │   └── [persona].md
│   │   └── subjects/
│   │       └── [subject_folder]/
│   │           ├── instructions.md
│   │           ├── sources/
│   │           │   └── [source_docs]
│   │           ├── links.md
│   │           └── chat_[timestamp].md
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_chat.py
│   │   ├── test_logger.py
│   │   └── test_retriever.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── assets/
│   │   │   ├── images/
│   │   │   └── fonts/
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   │   ├── ChatWindow.tsx
│   │   │   │   ├── MessageList.tsx
│   │   │   │   └── InputBox.tsx
│   │   │   ├── Sidebar/
│   │   │   │   ├── SubjectList.tsx
│   │   │   │   └── PersonaSelector.tsx
│   │   │   └── Common/
│   │   │       ├── Button.tsx
│   │   │       └── Modal.tsx
│   │   ├── pages/
│   │   │   ├── ChatPage.tsx
│   │   │   ├── SettingsPage.tsx
│   │   │   └── HistoryPage.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── chatService.ts
│   │   ├── styles/
│   │   │   ├── main.scss
│   │   │   ├── variables.scss
│   │   │   └── components/
│   │   │       ├── chat.scss
│   │   │       └── sidebar.scss
│   │   ├── types/
│   │   │   ├── chat.ts
│   │   │   └── persona.ts
│   │   ├── utils/
│   │   │   └── helpers.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md
├── for_ai/
│   └── [python_file_timestamp].txt
├── docs/
│   ├── api_documentation.md
│   ├── setup_guide.md
│   └── architecture.md
├── .gitignore
├── .env.example
├── docker-compose.yml
└── README.md


## For AI Assistant
A text version of all program files has been uploaded as source documents (example: chat_[time-stamp].txt is a copy of chat.py). The assisant should use the .txt docs as reference for the source code as of the start of the current day. 

When writing code the AI assistant's output should be in py format and when applicable in a py file.
### Current copies
- main_[time-stamp].txt = main.py
- main_streaming_[time-stamp].txt = main_streaming.py
- chat_[time-stamp].txt = chat.py
- logger_[time-stamp].txt = logger.py
- retriever_[time-stamp].txt = retriever.py

### Current Structure
local_chat_bot/
├── for_ai/
│   └── [python_file].txt
├── personas/
│   └── [persona].md
├── subjects/
│   └── [subject_folder]/
│       ├── instructions.md
│       └── chat_[timestamp].md
├── chat.py
├── file_watcher.py
├── logger.py
├── main_streaming.py
├── main.py
└── retriever.py