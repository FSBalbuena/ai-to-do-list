import os
from persistence import load_tasks, save_tasks
from task import Task

TASKS_SEPARATOR = "\n"
ACTION_FAIL_STATUS = False
ACTION_SUCCESS_STATUS = True

TASK_NOT_FOUND_STATUS = False
TASK_FOUND_STATUS = True

class TaskManager:
    """ 
        Task manager methods return a tuple (Boolean, Boolean):(ACTION_STATUS, TASK_FOUND_STATUS)
    """

    def __init__(self, filepath):
        self.filepath = filepath
        
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
        return (ACTION_SUCCESS_STATUS, TASK_FOUND_STATUS)

    def complete_task(self, id):
        for task in self._tasks:
            if task.id == id:
                if task.is_completed():
                    return (ACTION_FAIL_STATUS, TASK_FOUND_STATUS)
                else:
                    task.mark_completed()
                    self._save()
                    return (ACTION_SUCCESS_STATUS, TASK_FOUND_STATUS)
        return (ACTION_FAIL_STATUS, TASK_NOT_FOUND_STATUS)

    def delete_task(self, id):
        new_list = [task for task in self._tasks if task.id != id]
        if len(new_list) == len(self._tasks):
            return (ACTION_FAIL_STATUS, TASK_NOT_FOUND_STATUS)
        else:
            self._tasks = new_list
            self._save()
            return (ACTION_SUCCESS_STATUS, TASK_FOUND_STATUS)