import os
import sys
import json
import pytest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from persistence import load_tasks, save_tasks


def test_load_tasks_from_empty_file(tmp_path):
    """Test loading tasks when file doesn't exist returns empty list."""
    filepath = tmp_path / "nonexistent.json"
    tasks = load_tasks(str(filepath))
    assert tasks == []


def test_load_tasks_from_existing_file(tmp_path):
    """Test loading tasks from an existing JSON file."""
    filepath = tmp_path / "tasks.json"
    data = {
        "tasks": [
            {"id": 1, "description": "Task 1", "completed": False},
            {"id": 2, "description": "Task 2", "completed": True}
        ]
    }
    filepath.write_text(json.dumps(data), encoding='utf-8')
    
    tasks = load_tasks(str(filepath))
    assert len(tasks) == 2
    assert tasks[0]["id"] == 1
    assert tasks[1]["completed"] is True


def test_load_tasks_from_corrupted_json(tmp_path):
    """Test loading tasks from corrupted JSON file returns empty list."""
    filepath = tmp_path / "corrupted.json"
    filepath.write_text("{ invalid json", encoding='utf-8')
    
    tasks = load_tasks(str(filepath))
    assert tasks == []


def test_save_tasks_creates_json_file(tmp_path):
    """Test saving tasks creates a JSON file."""
    filepath = tmp_path / "new_tasks.json"
    tasks = [
        {"id": 1, "description": "Task 1", "completed": False}
    ]
    
    save_tasks(str(filepath), tasks)
    
    assert filepath.exists()
    content = json.loads(filepath.read_text(encoding='utf-8'))
    assert content["tasks"][0]["id"] == 1


def test_save_and_load_roundtrip(tmp_path):
    """Test that saved tasks can be loaded back."""
    filepath = tmp_path / "roundtrip.json"
    original_tasks = [
        {"id": 1, "description": "First task", "completed": False},
        {"id": 2, "description": "Completed task", "completed": True}
    ]
    
    save_tasks(str(filepath), original_tasks)
    loaded_tasks = load_tasks(str(filepath))
    
    assert loaded_tasks == original_tasks
