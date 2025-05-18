import pytest
from src.storage import save_tasks, load_tasks, StorageError
from src.task import Task


def make_tasks(n):
    return [Task(title=f"T{i}", due_date=None) for i in range(n)]


class TestStorageFunctionality:
    @pytest.mark.parametrize("count", [0, 1, 5])
    def test_save_and_load_roundtrip(self, tmp_path, count):
        tasks = make_tasks(count)
        fp = tmp_path / "tasks.json"
        save_tasks(str(fp), tasks)
        loaded = load_tasks(str(fp))
        assert isinstance(loaded, list)
        assert len(loaded) == count
        for orig, new in zip(tasks, loaded):
            assert orig.id == new.id
            assert orig.title == new.title

    @pytest.mark.parametrize("bad_content", ["not json", "[]]", "{]", "[1,2,}", '{"key":1]'])
    def test_load_invalid_json_raises(self, tmp_path, bad_content):
        fp = tmp_path / "bad.json"
        fp.write_text(bad_content)
        with pytest.raises(StorageError):
            load_tasks(str(fp))

    def test_save_io_error(self, tmp_path):
        dir_path = tmp_path / "dir"
        dir_path.mkdir()
        with pytest.raises(StorageError):
            save_tasks(str(dir_path), make_tasks(1))

    def test_load_nonexistent_raises(self, tmp_path):
        with pytest.raises(StorageError):
            load_tasks(str(tmp_path / "nope.json"))
