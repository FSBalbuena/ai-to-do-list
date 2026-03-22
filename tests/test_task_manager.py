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
    assert result == (True, True, None)

    result2 = manager.add_task("Second task")
    assert result2 == (True, True, None)

    tasks_list = manager.list_tasks().split("\n")
    assert "#1" in tasks_list[0]
    assert "#2" in tasks_list[1]


def test_complete_task_marks_as_completed(tmp_path):
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))
    manager.add_task("Task to complete")

    result = manager.complete_task(1)
    assert result == (True, True, None)

    # Complete again returns fail and found status
    result_again = manager.complete_task(1)
    assert result_again == (False, True, None)


def test_delete_task_removes_existing_task(tmp_path):
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))
    manager.add_task("Task to delete")

    result = manager.delete_task(1)
    assert result == (True, True, None)

    # Once deleted, deleting again should return not found
    result_not_found = manager.delete_task(1)
    assert result_not_found == (False, False, None)


def test_complete_or_delete_nonexistent_task(tmp_path):
    filepath = tmp_path / "tasks.json"
    manager = TaskManager(str(filepath))

    assert manager.complete_task(999) == (False, False, None)
    assert manager.delete_task(999) == (False, False, None)


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


def test_generate_complex_task_from_ai_creates_three_tasks(tmp_path):
    """Test that generate_complex_task creates 3 subtasks when AI succeeds."""
    filepath = tmp_path / "tasks.json"
    
    mock_subtasks = [
        "[Plan] -> Define scope",
        "[Design] -> Prepare architecture",
        "[Execute] -> Implement features",
    ]
    
    def mock_complex_task_assistant(description):
        return mock_subtasks
    
    manager = TaskManager(str(filepath), complex_task_assistant=mock_complex_task_assistant)
    (success, added, count) = manager.generate_complex_task('Build an AI-driven list')

    assert success is True
    assert added is True
    assert count == 3
    assert len(manager._tasks) == 3
    assert manager._tasks[0].description == mock_subtasks[0]
    assert manager._tasks[1].description == mock_subtasks[1]
    assert manager._tasks[2].description == mock_subtasks[2]


def test_generate_complex_task_returns_fail_on_ai_error(tmp_path):
    """Test that generate_complex_task returns failure when assistant raises."""
    filepath = tmp_path / "tasks.json"

    def mock_complex_task_assistant_error(description):
        raise Exception("API Key invalid")

    manager = TaskManager(str(filepath), complex_task_assistant=mock_complex_task_assistant_error)
    original_description = "Build an AI-driven list"

    success, added, metadata = manager.generate_complex_task(original_description)
    assert success is False
    assert added is False
    assert metadata == "AI service error"
    assert len(manager._tasks) == 0


def test_generate_complex_task_returns_fail_on_invalid_response_format(tmp_path):
    """Test that generate_complex_task returns failure when assistant returns wrong count."""
    filepath = tmp_path / "tasks.json"

    def mock_invalid_assistant(description):
        return ["Only one task"]

    manager = TaskManager(str(filepath), complex_task_assistant=mock_invalid_assistant)
    original_description = "Build an AI-driven list"

    success, added, metadata = manager.generate_complex_task(original_description)
    assert success is False
    assert added is False
    assert metadata == "Invalid number of subtasks"
    assert len(manager._tasks) == 0


def test_generate_complex_task_returns_fail_when_no_assistant(tmp_path):
    """Test that generate_complex_task returns failure when no assistant is configured."""
    filepath = tmp_path / "tasks.json"

    manager = TaskManager(str(filepath), complex_task_assistant=None)
    original_description = "Build an AI-driven list"

    success, added, metadata = manager.generate_complex_task(original_description)
    assert success is False
    assert added is False
    assert metadata == "No AI assistant available"
    assert len(manager._tasks) == 0


def test_generate_complex_task_persists_tasks_to_file(tmp_path):
    """Test that generated complex tasks are persisted to file."""
    filepath = tmp_path / "tasks.json"
    
    mock_subtasks = [
        "[Step 1] -> First step",
        "[Step 2] -> Second step",
        "[Step 3] -> Third step",
    ]
    
    def mock_complex_task_assistant(description):
        return mock_subtasks
    
    manager = TaskManager(str(filepath), complex_task_assistant=mock_complex_task_assistant)
    manager.generate_complex_task('Complex task')

    assert filepath.exists()
    data = json.loads(filepath.read_text(encoding='utf-8'))
    assert len(data["tasks"]) == 3
    assert data["tasks"][0]["description"] == mock_subtasks[0]


def test_ai_assistant_callable_injection(tmp_path):
    """Test AI assistant callable dependency injection without environment variables."""
    filepath = tmp_path / 'tasks.json'
    
    mock_subtasks = ['[Plan] -> A', '[Task] -> B', '[Review] -> C']
    
    def mock_callable(description):
        return mock_subtasks
    
    manager = TaskManager(str(filepath), complex_task_assistant=mock_callable)
    success, added, count = manager.generate_complex_task('Make a report')

    assert success is True
    assert added is True
    assert count == 3
    assert len(manager._tasks) == 3
    assert manager._tasks[0].description == '[Plan] -> A'
