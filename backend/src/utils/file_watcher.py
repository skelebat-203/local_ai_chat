#!/usr/bin/env python3
"""Watch a project tree and mirror .py files into timestamped .txt copies.

This tool is used for keeping an AI-friendly snapshot of the backend
source code. Whenever a Python file changes or is created, a matching
.txt file is generated under src/utils/for_ai, and older snapshots for
that same source file are deleted.
"""

import os
import time
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class PyFileHandler(FileSystemEventHandler):
    """Handle filesystem events for Python files and mirror them to .txt."""

    def __init__(self, project_dir, for_ai_dir):
        """Create a new file event handler.

        Args:
            project_dir: Root directory to watch for .py changes.
            for_ai_dir: Directory where .txt snapshots will be stored.
        """
        self.project_dir = Path(project_dir)
        self.for_ai_dir = Path(for_ai_dir)
        self.for_ai_dir.mkdir(exist_ok=True)

    def on_modified(self, event):
        """React to a modified file by mirroring .py files to .txt."""
        if not event.is_directory and event.src_path.endswith(".py"):
            self.copy_to_txt(event.src_path)

    def on_created(self, event):
        """React to a newly created .py file by mirroring it to .txt."""
        if not event.is_directory and event.src_path.endswith(".py"):
            self.copy_to_txt(event.src_path)

    def get_txt_filename(self, py_file: Path) -> str:
        """Generate a txt filename for a given .py file.

        __init__.py files are named using their parent directory plus
        '.init', while other files use their stem name.

        Args:
            py_file: Path to the source .py file.

        Returns:
            A filename string including a timestamp and .txt extension.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")

        if py_file.name == "__init__.py":
            parent = py_file.parent.name
            base_name = f"{parent}.init"
            return f"{base_name}_{timestamp}.txt"
        return f"{py_file.stem}_{timestamp}.txt"

    def copy_to_txt(self, py_file_path: str) -> None:
        """Mirror a .py file into the for_ai directory as a timestamped .txt.

        Old snapshots for the same base file are deleted before the new
        one is written.

        Args:
            py_file_path: Path (string) to the .py file that changed.
        """
        py_file = Path(py_file_path)

        if self.for_ai_dir in py_file.parents:
            return

        if py_file.name == "__init__.py":
            parent = py_file.parent.name
            base_pattern = f"{parent}.init_*.txt"
        else:
            base_pattern = f"{py_file.stem}_*.txt"

        for existing_file in self.for_ai_dir.glob(base_pattern):
            try:
                existing_file.unlink()
                print(f"✗ Deleted old version: {existing_file.name}")
            except Exception as e:
                print(f"✗ Error deleting {existing_file.name}: {e}")

        txt_filename = self.get_txt_filename(py_file)
        txt_file = self.for_ai_dir / txt_filename

        try:
            shutil.copy2(py_file, txt_file)
            print(f"✓ Created {txt_filename}")
        except Exception as e:
            print(f"✗ Error copying {py_file.name}: {e}")


def main():
    """Run the file watcher loop until interrupted with Ctrl+C."""
    current_file = Path(__file__).resolve()
    project_dir = current_file.parent

    while project_dir.name != "backend" and project_dir.parent != project_dir:
        project_dir = project_dir.parent

    if project_dir.name != "backend":
        project_dir = Path.cwd()

    for_ai_dir = project_dir / "src" / "utils" / "for_ai"

    print(f"Watching for .py file changes in: {project_dir}")
    print(f"Output directory: {for_ai_dir}")
    print("Press Ctrl+C to stop\n")

    event_handler = PyFileHandler(project_dir, for_ai_dir)
    observer = Observer()
    observer.schedule(event_handler, project_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching files")

    observer.join()


if __name__ == "__main__":
    main()
