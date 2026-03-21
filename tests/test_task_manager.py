import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from task_manager import TaskManager
from task import Task


def test_add_task_returns_success_and_increments_id():
    manager = TaskManager()

    result = manager.add_task("First task")
    assert result == (True, True)

    result2 = manager.add_task("Second task")
    assert result2 == (True, True)

    tasks_list = manager.list_tasks().split("\n")
    assert "#1" in tasks_list[0] or "1" in tasks_list[0]
    assert "#2" in tasks_list[1] or "2" in tasks_list[1]


def test_complete_task_marks_as_completed():
    manager = TaskManager()
    manager.add_task("Task to complete")

    result = manager.complete_task(1)
    assert result == (True, True)

    # Complete again returns fail and found status
    result_again = manager.complete_task(1)
    assert result_again == (False, True)


def test_delete_task_removes_existing_task():
    manager = TaskManager()
    manager.add_task("Task to delete")

    result = manager.delete_task(1)
    assert result == (True, True)

    # Once deleted, deleting again should return not found
    result_not_found = manager.delete_task(1)
    assert result_not_found == (False, False)


def test_complete_or_delete_nonexistent_task():
    manager = TaskManager()

    assert manager.complete_task(999) == (False, False)
    assert manager.delete_task(999) == (False, False)
