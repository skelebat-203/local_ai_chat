## Local Perplexity clone
There are 3 reasons for this project.
1. I want a local chat interface I control
2. I want to learn some skills
3. I want to brushup on other skills

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


## For AI Assistant
A text version of all program files has been uploaded as source documents (example: chat_[time-stamp].txt is a copy of chat.py). The assisant should use the .txt docs as reference for the source code as of the start of the current day. 

When writing code the AI assistant's output should be in py format and when applicable in a py file.
### Current copies
- main_[time-stamp].txt = main.py
- main_streaming_[time-stamp].txt = main_streaming.py
- chat_[time-stamp].txt = chat.py
- logger_[time-stamp].txt = logger.py
- retriever_[time-stamp].txt = retriever.py

### App Structure
Chat_app/
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
