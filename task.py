COMPLETED_FLAG = "✓"
UNCOMPLETED_FLAG = ""
ID_CHAR = "#"

class Task:
    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self._completed = completed

    def mark_completed(self):
        self._completed = True
    
    def is_completed(self):
        return self._completed

    def __str__(self):
        status = COMPLETED_FLAG if self._completed else UNCOMPLETED_FLAG
        return f"[{status}] {ID_CHAR}{self.id} - {self.description}"