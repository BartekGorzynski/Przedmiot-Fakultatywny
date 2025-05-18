import pytest
from src.manager import TaskManager, TaskNotFoundError
from datetime import date, timedelta


class TestTaskManagerBasic:
    @pytest.fixture
    def manager(self):
        return TaskManager()

    @pytest.mark.parametrize("title, desc", [(f"Task {i}", f"Desc {i}") for i in range(10)])
    def test_add_task(self, manager, title, desc):
        task = manager.add_task(title, desc)
        assert task.title == title
        assert task.description == desc
        assert task in manager.tasks

    def test_remove_and_get_task(self, manager):
        task = manager.add_task("X")
        tid = task.id
        manager.remove_task(tid)
        with pytest.raises(TaskNotFoundError):
            manager.get_task(tid)

    @pytest.mark.parametrize("count", [0, 1, 5])
    def test_list_tasks_filters(self, manager, count):
        added = []
        for i in range(count):
            added.append(manager.add_task(f"T{i}"))
        all_tasks = manager.list_tasks()
        assert len(all_tasks) == count
        for t in added[:count // 2]:
            manager.complete_task(t.id)
        completed = manager.list_tasks(completed=True)
        not_completed = manager.list_tasks(completed=False)
        assert len(completed) + len(not_completed) == count


class TestTaskManagerErrors:
    @pytest.fixture
    def manager(self):
        return TaskManager()

    @pytest.mark.parametrize("bad_id", ["", "none", "1234-5678", "abc", "-1"])
    def test_remove_nonexistent_raises(self, manager, bad_id):
        with pytest.raises(TaskNotFoundError):
            manager.remove_task(bad_id)

    @pytest.mark.parametrize("offset", [-5, -1, 1, 5])
    def test_list_overdue(self, manager, offset):
        due = date.today() + timedelta(days=offset)
        t = manager.add_task("O", due_date=due)
        overdue = manager.list_overdue()
        expected = offset < 0
        assert (t in overdue) is expected
