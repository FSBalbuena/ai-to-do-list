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

    def __init__(self):
        self._tasks = []
        self._next_id = 1

    def increment_next_id(self):
        self._next_id += 1

    def list_tasks(self):
        return TASKS_SEPARATOR.join([str(task) for task in self._tasks])

    def add_task(self, description):
        id = self._next_id
        self.increment_next_id()
        new_list = self._tasks.copy()
        new_list.append(Task(id, description))
        self._tasks = new_list
        return (ACTION_SUCCESS_STATUS, TASK_FOUND_STATUS)

    def complete_task(self, id):
        for task in self._tasks:
            if task.id == id:
                if task.is_completed():
                    return (ACTION_FAIL_STATUS, TASK_FOUND_STATUS)
                else:
                    task.mark_completed()
                    return (ACTION_SUCCESS_STATUS, TASK_FOUND_STATUS)
        return (ACTION_FAIL_STATUS, TASK_NOT_FOUND_STATUS)

    def delete_task(self, id):
        new_list = [task for task in self._tasks if task.id !=id]
        if len(new_list) == len(self._tasks):
            return (ACTION_FAIL_STATUS, TASK_NOT_FOUND_STATUS)
        else:
            self._tasks = new_list
            return (ACTION_SUCCESS_STATUS, TASK_FOUND_STATUS)