"""Model pojedynczego zadania."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
import uuid
import re


class TaskNotFoundError(Exception):
    """Gdy zadanie o podanym ID nie istnieje."""
    pass


@dataclass
class Task:
    """Reprezentuje pojedyncze zadanie TODO."""
    title: str
    description: str = ""
    due_date: Optional[date] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    completed: bool = False

    def mark_completed(self) -> None:
        """Oznacz zadanie jako ukończone."""
        self.completed = True

    def is_overdue(self) -> bool:
        """Zwróć True, gdy zadanie jest przeterminowane i nieukończone."""
        if self.completed or self.due_date is None:
            return False
        return date.today() > self.due_date


def parse_due_date(date_str: str) -> date:
    """Parsuj datę w formacie YYYY-MM-DD.

    Raises:
        ValueError: gdy format jest nieprawidłowy lub data nie istnieje.
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        raise ValueError(f"Invalid date format: {date_str}")

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {date_str}") from exc
