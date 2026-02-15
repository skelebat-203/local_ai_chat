#!/usr/bin/env python3
import os
import time
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PyFileHandler(FileSystemEventHandler):
    def __init__(self, project_dir, for_ai_dir):
        self.project_dir = Path(project_dir)
        self.for_ai_dir = Path(for_ai_dir)
        # Create for_ai directory if it doesn't exist
        self.for_ai_dir.mkdir(exist_ok=True)
    
    def on_modified(self, event):
        # Only process .py files that are actually files (not directories)
        if not event.is_directory and event.src_path.endswith('.py'):
            self.copy_to_txt(event.src_path)
    
    def on_created(self, event):
        # Handle newly created .py files too
        if not event.is_directory and event.src_path.endswith('.py'):
            self.copy_to_txt(event.src_path)
    
    def get_txt_filename(self, py_file):
        """Generate appropriate txt filename based on whether it's __init__.py or not"""
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
        
        if py_file.name == '__init__.py':
            # Get parent folder name
            parent = py_file.parent.name
            base_name = f"{parent}.init"
            return f"{base_name}_{timestamp}.txt"
        else:
            # Regular Python files
            return f"{py_file.stem}_{timestamp}.txt"
    
    def copy_to_txt(self, py_file_path):
        py_file = Path(py_file_path)
        
        # Skip files in the for_ai directory itself
        if self.for_ai_dir in py_file.parents:
            return
        
        # Skip the watcher script itself
        # if py_file.name == 'file_watcher.py':
        #     return
        
        # Determine the base name for matching old files
        if py_file.name == '__init__.py':
            parent = py_file.parent.name
            base_pattern = f"{parent}.init_*.txt"
        else:
            base_pattern = f"{py_file.stem}_*.txt"
        
        # Delete any existing .txt files for this .py file (ignore timestamps)
        for existing_file in self.for_ai_dir.glob(base_pattern):
            try:
                existing_file.unlink()
                print(f"✗ Deleted old version: {existing_file.name}")
            except Exception as e:
                print(f"✗ Error deleting {existing_file.name}: {e}")
        
        # Generate new filename
        txt_filename = self.get_txt_filename(py_file)
        txt_file = self.for_ai_dir / txt_filename
        
        try:
            # Copy contents from .py to .txt
            shutil.copy2(py_file, txt_file)
            print(f"✓ Created {txt_filename}")
        except Exception as e:
            print(f"✗ Error copying {py_file.name}: {e}")

def main():
    # Find project root (backend directory)
    # Start from current file location and go up to find 'backend'
    current_file = Path(__file__).resolve()
    project_dir = current_file.parent
    
    # Navigate up until we find the backend directory
    while project_dir.name != 'backend' and project_dir.parent != project_dir:
        project_dir = project_dir.parent
    
    # If we didn't find 'backend', use current working directory
    if project_dir.name != 'backend':
        project_dir = Path.cwd()
    
    # Set for_ai directory at backend/src/utils/for_ai/
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
