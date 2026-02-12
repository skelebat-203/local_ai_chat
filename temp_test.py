# from pathlib import Path
# import os

# print(f"Current working directory:\n {os.getcwd()}")
# print("\nFiles and folders here:")
# for item in os.listdir('.'):
#     print(f"  - {item}")


# # Test if the path exists
# print("Test if the path exists:")
# base = Path("./Chat_app")  # or "." if running from inside Chat_app
# print(f"\tBase exists: {base.exists()}")
# print(f"\tSubjects path exists: {(base / 'subjects').exists()}")
# print(f"\tFantasy story exists: {(base / 'subjects' / 'fantasy_story').exists()}")
# print(f"\tInstructions exists: {(base / 'subjects' / 'fantasy_story' / 'instructions.md').exists()}")

from pathlib import Path
base = Path(".")  # Current directory
print(f"Base exists: {base.exists()}")
print(f"Subjects exists: {(base / 'subjects').exists()}")
print(f"Fantasy story exists: {(base / 'subjects' / 'fantasy_story').exists()}")
print(f"Instructions exists: {(base / 'subjects' / 'fantasy_story' / 'instructions.md').exists()}")

# from pathlib import Path
# base = Path(".")
# subjects_path = base / "subjects"

# print("Contents of subjects folder:")
# for item in subjects_path.iterdir():
#     print(f"  - {item.name} (is_dir: {item.is_dir()})")
