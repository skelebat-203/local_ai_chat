## Local Perplexity clone
There are 3 reasons for this project.
1. I want a local chat interface I control
2. I want to learn some skills
3. I want to brushup on other 

## Requirements
- ollama - Core Ollama API client - enables communication with local Ollama LLM models for chat functionality
- prompt_toolkit - Add keyboard navigation controls
- llama3 - this is the default model the bot looks for
- qwen2.5-coder:32b - only needed if you want to use the swap command
- watchdog - only needed if you want to run file_watcher.  See "AI Assistant" in this doc for more info

## To run
1. In terminal navigate to local_chat_bot/backend/src
2. run `python3 main.py`

## Features
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
- Allow swap between modals, llama3 and qwen2.5-coder:32b

### Version 2: App UI and sources
- This has been moved to a separate repo. [local_ai_chat_v2](https://github.com/skelebat-203/local_ai_chat_v2)

## Default personas
- default - a general persona focusing on sort factual responses
- gm - game master for TTRPG
- teacher - basic teacher / mentor 
- writer - basic writing assistant

## Subjects
- no_subject - default location for chats
- fantasy_story and scifi_story - these have simple source instructions about a fantasy / scifi story concept.

## AI Assistant
A text version of all program files has been uploaded as source documents (example: chat_[time-stamp].txt is a copy of chat.py). The assisant should use the .txt docs as reference for the source code as of the start of the current day. 

When writing code the AI assistant's output should be in py format and when applicable in a py file.

### file_watcher.py
The chat service, Perplexity.ai, I am using to help with the project cannot store python files to use as sources. This script exists as a workaround for that bug. It watches for when a python file is saved. When a file is saved. It copies the file in .txt format with a timestamp. And deletes the old .txt version if one exists. 

### Current copies
- chat\_[time-stamp].txt = chat.py
- chat\_commands\_[time-stamp].txt = chat\_commands.py
- commands\_handler\_[time-stamp].txt = commands\_handler.py
- commands.init_[time-stamp].txt = commands/terminal/ \_\_init\_\_.py
- core.init\__[time-stamp].txt = core/ \_\_init\_\_.py
- file\_watcher\_[time-stamp].txt = file\_watcher.py
- logger\_[time-stamp].txt = logger.py
- main\_[time-stamp].txt = main.py
- retriever\_[time-stamp].txt = retriever.py
- subject\_commands\_[time-stamp].txt = subject\_commands.py
- ui\_[time-stamp].txt = ui.py
- utils.init\_[time-stamp].txt = utils/ \_\_init\_\_.py