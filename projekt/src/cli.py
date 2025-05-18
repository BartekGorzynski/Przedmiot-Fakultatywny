"""Moduł odpowiedzialny za interfejs CLI TODO-listy."""


def display_menu() -> str:
    """Zwróć tekst menu aplikacji."""
    return (
        "1. Add task\n"
        "2. Remove task\n"
        "3. List tasks\n"
        "4. Mark task completed\n"
        "5. List overdue\n"
        "6. Exit\n"
    )


def parse_choice(choice: str) -> int:
    """Przekształć wybór (str) na numer opcji.

    Raises:
        ValueError: gdy choice nie jest liczbą w zakresie 1–6.
    """
    if not isinstance(choice, str):
        raise ValueError("Choice must be a string")

    if not choice.isdigit():
        raise ValueError("Choice must be a number")

    val = int(choice)

    if val < 1 or val > 6:
        raise ValueError("Choice out of range")

    return val
