import os
import sys
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from task_manager import TaskManager
from task import Task


def test_task_manager_init_with_empty_file(tmp_path):
    """Test TaskManager initializes with empty file."""
    filepath = tmp_path / "empty.json"
    manager = TaskManager(str(filepath))
    
    assert manager.filepath == str(filepath)
    assert manager.list_tasks() == ""


def test_add_task_returns_success_and_increments_id(tmp_path):
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))

    result = manager.add_task("First task")
    assert result == (True, True)

    result2 = manager.add_task("Second task")
    assert result2 == (True, True)

    tasks_list = manager.list_tasks().split("\n")
    assert "#1" in tasks_list[0]
    assert "#2" in tasks_list[1]


def test_complete_task_marks_as_completed(tmp_path):
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))
    manager.add_task("Task to complete")

    result = manager.complete_task(1)
    assert result == (True, True)

    # Complete again returns fail and found status
    result_again = manager.complete_task(1)
    assert result_again == (False, True)


def test_delete_task_removes_existing_task(tmp_path):
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))
    manager.add_task("Task to delete")

    result = manager.delete_task(1)
    assert result == (True, True)

    # Once deleted, deleting again should return not found
    result_not_found = manager.delete_task(1)
    assert result_not_found == (False, False)


def test_complete_or_delete_nonexistent_task(tmp_path):
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))

    assert manager.complete_task(999) == (False, False)
    assert manager.delete_task(999) == (False, False)


def test_task_manager_persistence_saves_to_file(tmp_path):
    """Test that tasks are saved to file after operations."""
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))
    
    manager.add_task("Persisted task")
    
    assert filepath.exists()
    data = json.loads(filepath.read_text(encoding='utf-8'))
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["description"] == "Persisted task"


def test_task_manager_loads_persisted_tasks(tmp_path):
    """Test that TaskManager loads previously saved tasks."""
    filepath = tmp_path / "tasks.json"
    
    # Create first manager and add tasks
    manager1 = TaskManager(str(filepath))
    manager1.add_task("First task")
    manager1.add_task("Second task")
    manager1.complete_task(1)
    
    # Create second manager (simulates app restart)
    manager2 = TaskManager(str(filepath))
    
    assert len(manager2._tasks) == 2
    assert manager2._tasks[0].description == "First task"
    assert manager2._tasks[0].is_completed()
    assert manager2._tasks[1].description == "Second task"
    assert not manager2._tasks[1].is_completed()


def test_task_to_dict_conversion(tmp_path):
    """Test private _task_to_dict method."""
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))
    
    task = Task(1, "Test task", completed=True)
    task_dict = manager._task_to_dict(task)
    
    assert task_dict["id"] == 1
    assert task_dict["description"] == "Test task"
    assert task_dict["completed"] is True


def test_dict_to_task_conversion(tmp_path):
    """Test private _dict_to_task method."""
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))
    
    task_dict = {"id": 1, "description": "Test task", "completed": True}
    task = manager._dict_to_task(task_dict)
    
    assert task.id == 1
    assert task.description == "Test task"
    assert task.is_completed()


def test_task_manager_next_id_after_load(tmp_path):
    """Test that next_id is correctly set after loading persisted tasks."""
    filepath = tmp_path / "tasks.json"
    
    manager1 = TaskManager(str(filepath))
    manager1.add_task("Task 1")
    manager1.add_task("Task 2")
    manager1.delete_task(1)  # Delete first task
    
    manager2 = TaskManager(str(filepath))
    manager2.add_task("Task 3")
    
    # New task should have ID 3 (next after max existing)
    assert manager2._tasks[-1].id == 3
