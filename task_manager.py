import os
from persistence import load_tasks, save_tasks
from task import Task
import copywrite

TASKS_SEPARATOR = "\n"
ACTION_FAIL_STATUS = False
ACTION_SUCCESS_STATUS = True

TASK_NOT_FOUND_STATUS = False
TASK_FOUND_STATUS = True
TASK_ADDED = True
TASK_NOT_ADDED = False

class TaskManager:
    """ 
        Task manager methods return a tuple (Boolean, Boolean, optional_metadata):(ACTION_STATUS, TASK_STATUS, metadata)
    """

    def __init__(self, filepath, complex_task_assistant=None):
        self.filepath = filepath
        self.complex_task_assistant = complex_task_assistant
        
        # Load existing tasks from file
        raw_tasks = load_tasks(filepath)
        self._tasks = [self._dict_to_task(item) for item in raw_tasks]
        self._next_id = max((t.id for t in self._tasks), default=0) + 1

    def _dict_to_task(self, data):
        """Convert dict to Task object."""
        return Task(
            data["id"],
            data["description"],
            data.get("completed", False)
        )

    def _task_to_dict(self, task):
        """Convert Task object to dict."""
        return {
            "id": task.id,
            "description": task.description,
            "completed": task.is_completed()
        }

    def _save(self):
        """Private method to save all tasks."""
        task_dicts = [self._task_to_dict(task) for task in self._tasks]
        save_tasks(self.filepath, task_dicts)

    def list_tasks(self):
        return TASKS_SEPARATOR.join([str(task) for task in self._tasks])

    def add_task(self, description):
        id = self._next_id
        self._next_id += 1
        new_list = self._tasks.copy()
        new_list.append(Task(id, description))
        self._tasks = new_list
        self._save()
        return (ACTION_SUCCESS_STATUS, TASK_ADDED, None)

    def complete_task(self, id):
        for task in self._tasks:
            if task.id == id:
                if task.is_completed():
                    return (ACTION_FAIL_STATUS, TASK_FOUND_STATUS, None)
                else:
                    task.mark_completed()
                    self._save()
                    return (ACTION_SUCCESS_STATUS, TASK_FOUND_STATUS, None)
        return (ACTION_FAIL_STATUS, TASK_NOT_FOUND_STATUS, None)

    def delete_task(self, id):
        new_list = [task for task in self._tasks if task.id != id]
        if len(new_list) == len(self._tasks):
            return (ACTION_FAIL_STATUS, TASK_NOT_FOUND_STATUS, None)
        else:
            self._tasks = new_list
            self._save()
            return (ACTION_SUCCESS_STATUS, TASK_FOUND_STATUS, None)

    def generate_complex_task(self, complex_task_description):
        """Generate 3-5 subtasks from AI and persist as Task objects."""
        if not self.complex_task_assistant:
            return (ACTION_FAIL_STATUS, TASK_NOT_ADDED, copywrite.GENERATE_COMPLEX_TASK_NO_AI_ERROR)
        try:
            subtasks = self.complex_task_assistant(complex_task_description)
        except Exception:
            return (ACTION_FAIL_STATUS, TASK_NOT_ADDED, copywrite.GENERATE_COMPLEX_TASK_SERVICE_ERROR)

        if not isinstance(subtasks, list):
            return (ACTION_FAIL_STATUS, TASK_NOT_ADDED, copywrite.GENERATE_COMPLEX_TASK_INVALID_RESPONSE_ERROR)

        if len(subtasks) < 3 or len(subtasks) > 5:
            return (ACTION_FAIL_STATUS, TASK_NOT_ADDED, copywrite.GENERATE_COMPLEX_TASK_INVALID_TASKS_ERROR)

        for sub in subtasks:
            if not isinstance(sub, str):
                return (ACTION_FAIL_STATUS, TASK_NOT_ADDED, copywrite.GENERATE_COMPLEX_TASK_INVALID_FORMAT_ERROR)

        for sub in subtasks:
            self._tasks.append(Task(self._next_id, sub))
            self._next_id += 1

        self._save()
        return (ACTION_SUCCESS_STATUS, TASK_ADDED, len(subtasks))