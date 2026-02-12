#!/usr/bin/env python3
import os
import time
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PyFileHandler(FileSystemEventHandler):
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.for_ai_dir = self.project_dir / "for_ai"
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
    
    def copy_to_txt(self, py_file_path):
        py_file = Path(py_file_path)
        
        # Skip files in the for_ai directory itself
        if self.for_ai_dir in py_file.parents:
            return
        
        # Skip the watcher script itself
        if py_file.name == 'file_watcher.py':
            return
        
        # Delete any existing .txt files for this .py file (ignore timestamps)
        base_name = py_file.stem
        for existing_file in self.for_ai_dir.glob(f"{base_name}_*.txt"):
            try:
                existing_file.unlink()
                print(f"✗ Deleted old version: {existing_file.name}")
            except Exception as e:
                print(f"✗ Error deleting {existing_file.name}: {e}")
        
        # Create timestamp in yyyy-mm-dd-hh-mm format
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
        
        # Create corresponding .txt filename with timestamp
        txt_filename = f"{base_name}_{timestamp}.txt"
        txt_file = self.for_ai_dir / txt_filename
        
        try:
            # Copy contents from .py to .txt
            shutil.copy2(py_file, txt_file)
            print(f"✓ Created {txt_filename}")
        except Exception as e:
            print(f"✗ Error copying {py_file.name}: {e}")

def main():
    # Get project directory (current directory by default)
    project_dir = os.getcwd()
    print(f"Watching for .py file changes in: {project_dir}")
    print(f"Output directory: {project_dir}/for_ai")
    print("Press Ctrl+C to stop\n")
    
    event_handler = PyFileHandler(project_dir)
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