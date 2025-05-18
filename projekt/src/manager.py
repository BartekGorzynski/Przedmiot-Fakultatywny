"""Moduł zarządzania zadaniami."""

from datetime import date, timedelta
from typing import List, Optional
from .task import Task, TaskNotFoundError


class TaskManager:
    """Zarządza kolekcją zadań w pamięci."""

    def __init__(self):
        """Zainicjuj menedżera z pustą listą zadań."""
        self._tasks: List[Task] = []

    @property
    def tasks(self) -> List[Task]:
        """Zwróć listę wszystkich zadań."""
        return list(self._tasks)

    def add_task(self, title: str, description: str = "", due_date: Optional[date] = None) -> Task:
        """Dodaj nowe zadanie do kolekcji."""
        task = Task(title=title, description=description, due_date=due_date)
        self._tasks.append(task)
        return task

    def remove_task(self, task_id: str) -> None:
        """Usuń zadanie o podanym ID lub rzuć wyjątek."""
        task = self.get_task(task_id)
        self._tasks.remove(task)

    def get_task(self, task_id: str) -> Task:
        """Zwróć zadanie o danym ID lub rzuć wyjątek."""
        for t in self._tasks:
            if t.id == task_id:
                return t
        raise TaskNotFoundError(f"Task with id {task_id} not found")

    def list_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """Zwróć wszystkie zadania lub przefiltruj po statusie completed."""
        if completed is None:
            return list(self._tasks)
        return [t for t in self._tasks if t.completed is completed]

    def complete_task(self, task_id: str) -> None:
        """Oznacz zadanie jako ukończone."""
        task = self.get_task(task_id)
        task.mark_completed()

    def list_overdue(self, days: int = 0) -> List[Task]:
        """Zwróć zadania przeterminowane o więcej niż `days` dni."""
        result: List[Task] = []
        today = date.today()
        for t in self._tasks:
            if t.completed or t.due_date is None:
                continue
            if today > t.due_date + timedelta(days=days):
                result.append(t)
        return result
