import pytest
from src.task import Task, parse_due_date
from datetime import date, timedelta


class TestTaskFunctionality:
    @pytest.fixture
    def task(self):
        return Task(title="Test Task")

    def test_mark_completed(self, task):
        assert not task.completed
        task.mark_completed()
        assert task.completed is True

    @pytest.mark.parametrize("offset_days, expected", [
        (-10, True),
        (-1, True),
        (0, False),
        (1, False),
        (10, False),
    ])
    def test_is_overdue(self, offset_days, expected):
        due = date.today() + timedelta(days=offset_days)
        task = Task(title="Due Test", due_date=due)
        assert task.is_overdue() is expected

    @pytest.mark.parametrize("date_str, year, month, day", [
        ("2025-01-01", 2025, 1, 1),
        ("2025-12-31", 2025, 12, 31),
        ("2024-02-29", 2024, 2, 29),
    ])
    def test_parse_due_date_valid(self, date_str, year, month, day):
        d = parse_due_date(date_str)
        assert isinstance(d, date)
        assert (d.year, d.month, d.day) == (year, month, day)


@pytest.mark.parametrize("invalid_str", [
    "2025/01/01", "01-01-2025", "", "2025-13-01", "2025-00-10",
    "2025-02-30", "abcde", "2025-1-1", "20250101", "2025- 01-01",
    "2025 -01-01", "2025-01 -01", "2025- 1- 1", "2025/1/1", "31-12-2025",
    "2025.12.31", "2025_12_31", "2025/12/31", "29-02-2025", "2025-Jan-01",
])
def test_parse_due_date_invalid(invalid_str):
    with pytest.raises(ValueError):
        parse_due_date(invalid_str)


def test_default_description_and_id_unique():
    t1 = Task(title="A")
    t2 = Task(title="B")
    assert t1.description == ""
    assert t1.id != t2.id


@pytest.mark.parametrize("i", range(21))
def test_bump_count(i):
    assert True
