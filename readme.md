## Local Perplexity clone
There are 3 reasons for this project.
1. I want a local chat interface I control
2. I want to learn some skills
3. I want to brushup on other 

## To run
1. In terminal navigate to local_chat_bot/backend/src
2. run `python3 main.py`

## Features
### Current Features
- Default subject / persona
- Set alternate subject / persona
- Store subject related chat in subject log
- Retrieve subject instructions and chat logs
- View chats, all chat or subject specific
- Allow creation of new subject / persona
- Allow user to see and update subject and persona instructions
- Allow user ability to delete chats, subjects, and persona
- Allow user ability to move chats to other subject
- UI update: start prompt / response with "User:\n" and "Assistant:\n"
- Allow swap between modals

## Updates needed reach version 1 (.v01) milestonets
- Allow user modify chat title
   - On save Title = 1st 10 words of chat.
   - Format: (word_word_word)
     - If multiple chats hav ethe same name appeand -[nn] to the end. Format: (word_word_word-01)
   - add command "/update_title"
      - display the existing title.
      - user can update the title at anytime.
- UI Update: "/chat_history" and "/chat_history [subject]" better formated chat names
   - "/chat_history" Format: [number] [title] [subject] [hh:mm] [yyyy-mm-dd]
   - "/chat_history [subject]" Format: [title] [hh:mm] [yyyy-mm-dd]
   - still want to select a chat by the displayed list item number
- Version 1 complete

### Version 2: App UI and sources
- Add UI
- Sources docs for specific subjects 
- Sources links doc for specific subjects

## Sucture
- data/
- src/
- .gitignore - everthing git should ignore when doing its thing.
- readme.md - you're currently reading this.
- requirements.txt - all the stuff required to run this app.

### data
- personas
- subjects
- chatlogs

### src
- commands/ - chat, central, and subject/persona management command handlers.
- core/ - logic for chat, logging chat, and retrieving chat, subject, persona
- utils/ - terminal UI and stuff for my AI assistant workaround
- main.py - central contol for app

## file_watcher.py
The chat service I am using to help with the project cannot store / "see" .py files to use a sources. This script exists as a workaround for that bug. It watches for when a python file is saved. When a file is saved. It copies the file in .txt format with a timestamp. And deletes the old .txt version if one exists. 

### Full App Structure
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
- chat_[time-stamp].txt = chat.py
- chat_commands_[time-stamp].txt = chat_commands.py
- commands_handler_[time-stamp].txt = commands_handler.py
- commands.init_[time-stamp].txt = commands/ \__init\__.py
- core.init_[time-stamp].txt = core/ \__init\__.py
- file_watcher_[time-stamp].txt = file_watcher.py
- logger_[time-stamp].txt = logger.py
- main_[time-stamp].txt = main.py
- retriever_[time-stamp].txt = retriever.py
- subject_commands_[time-stamp].txt = subject_commands.py
- ui_[time-stamp].txt = ui.py
- utils.init_[time-stamp].txt = utils/ \__init\__.py