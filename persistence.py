import json
from pathlib import Path

def load_tasks(filepath):
    """Load tasks from JSON file. Return empty list if file doesn't exist."""
    path = Path(filepath)
    if not path.exists():
        return []
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('tasks', [])
    except (json.JSONDecodeError, KeyError, IOError):
        # Corrupted file or I/O error - start fresh
        return []

def save_tasks(filepath, tasks):
    """Save tasks to JSON file."""
    path = Path(filepath)
    data = {'tasks': tasks}
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except IOError:
        # Handle write errors (permissions, disk full, etc.)
        pass  # Could log or raise, but for now just fail silently