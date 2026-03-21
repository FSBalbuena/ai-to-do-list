import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from task import Task


def test_task_init_default_not_completed():
    """Test Task initializes with completed=False by default."""
    t = Task(1, "New task")
    assert not t.is_completed()


def test_task_init_with_completed_true():
    """Test Task can initialize with completed=True."""
    t = Task(1, "Completed task", completed=True)
    assert t.is_completed()


def test_task_init_with_completed_false():
    """Test Task can explicitly initialize with completed=False."""
    t = Task(1, "Pending task", completed=False)
    assert not t.is_completed()


def test_task_mark_completed():
    """Test marking a task as completed."""
    t = Task(2, "Task to complete")
    assert not t.is_completed()
    
    t.mark_completed()
    assert t.is_completed()


def test_task_str_representation_pending():
    """Test string representation of pending task."""
    t = Task(1, "Pending task")
    output = str(t)
    assert "#1" in output
    assert "Pending task" in output
    assert "✓" not in output


def test_task_str_representation_completed():
    """Test string representation of completed task."""
    t = Task(1, "Completed task", completed=True)
    output = str(t)
    assert "#1" in output
    assert "Completed task" in output
    assert "✓" in output
