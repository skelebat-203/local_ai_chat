"""Core modules for the local chat bot application.

This package exposes the main building blocks of the subject-aware
local chat app so callers can import them from a single place:
    - SubjectRetriever: manages personas, subjects, and system prompts
    - ChatSession: wraps the Ollama chat API and tracks history
    - ChatLogger: persists conversations to disk as markdown
"""

from .retriever import SubjectRetriever
from .chat import ChatSession
from .logger import ChatLogger

__all__ = ["SubjectRetriever", "ChatSession", "ChatLogger"]
