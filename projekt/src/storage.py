"""Moduł zapisu i odczytu zadań do/z pliku JSON."""

import json
from typing import List
from .task import Task


class StorageError(Exception):
    """Wyjątek dla błędów zapisu/odczytu zadań."""
    pass


def save_tasks(path: str, tasks: List[Task]) -> None:
    """Zapisz `tasks` do pliku JSON `path`."""
    data = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "completed": t.completed,
        }
        for t in tasks
    ]
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except IOError as exc:
        raise StorageError(f"Cannot write to {path}") from exc


def load_tasks(path: str) -> List[Task]:
    """Wczytaj zadania z pliku JSON `path`."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (IOError, json.JSONDecodeError) as exc:
        raise StorageError(f"Cannot read from {path}") from exc

    tasks: List[Task] = []
    from datetime import date as _date

    for item in raw:
        try:
            due_str = item.get("due_date")
            due = _date.fromisoformat(due_str) if due_str else None
            task = Task(
                title=item["title"],
                description=item.get("description", ""),
                due_date=due,
                id=item.get("id"),
            )
            if item.get("completed"):
                task.completed = True
        except (KeyError, TypeError, ValueError):
            continue
        tasks.append(task)

    return tasks
