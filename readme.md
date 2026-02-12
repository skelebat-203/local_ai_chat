# Local Perplexity clone
There are 3 reasons for this project.
1. I want a local chat interface I control
2. I want to learn some skills
3. I wnat to brushup on other skills

## Log Structure
**Chat_app**
- subjects
    - fantasy_story
        - instructions.md
        - [chat_01]
        - ...
    - scifi_story
        - instructions.md
        - [chat_01]
        - ...
- personas
    - writer.md
    - [other_persona]
    - [other_persona]
    - ...
### Personas
Holds the different types of personalities I want to choose from.
- GM
- Teacher
- Writer
- etc.
### Contexts
Holds a number of subject folders: my_novel, coding_project_01, etc.  In each subject folder is a sources_docs folder, links.txt, an instructions.md file, and chat logs related to that subject.

#### Sources
Holds a file for any source uploaded to the 

#### Instructions.md
This holds all instructions for a specific topic

**Example:** Use the source docs and links as your primary sources...

#### Sources_docs - TBD
Holds source docs related to the subject: current novel doc, source code, etc.

#### Links.txt - TBD
Holds links to websites, and possilly system files.

#### Chat logs
Previous chats that relate the the subject.

## Python files
### main.py main_streaming.py
This is UX thing. 
- main.py runs with no indication the chatbot is doing anything. Then, prints the response all at once.
- main_streaming.py slowly prints the response, more human like.

run with `python3 main.py` or `python3 main_streaming.py`

### chat.py
Chat logic: sending messages, receiving responses, managing conversation flow
chat.txt is a copy of chat.py meant to do used as a source doc by an AI assistant.

### logger.py
This is curently how I am saving and sorting the current chat once I type /exit

### retriever.py
This currently grabs the persona and context when the user requests it.

## Future Functions
### Persona - TBD
TBD - plan this to create new personas
- Create Persona file
- Write persona instructions to the file

### New Subject - TBD
TBD - plan this to create new subjects
- Create Subject folder
- Write subject instructions file
- add Sources and links

### Delete - TBD
- Delete Persona
- Delete Subject
- Delete Chat

### Modify - TBD
- Modify Persona
- Modify Subject
    - name
    - instructions
- Modify Chat - add a title for easier reference

## For AI Assistant
A text version of all program files has been uploaded as source documents (example: chat_[time-stamp].txt is a copy of chat.py). The assisant should use the .txt docs as reference for the source code as of the start of the current day. 

When writing code the AI assistant's output should be in py format and when applicable in a py file.
### Current copies
- main_[time-stamp].txt = main.py
- main_streaming_[time-stamp].txt = main_streaming.py
- chat_[time-stamp].txt = chat.py
- logger_[time-stamp].txt = logger.py
- retriever_[time-stamp].txt = retriever.py
