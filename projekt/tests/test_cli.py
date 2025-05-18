import pytest
from src.cli import display_menu, parse_choice


class TestCLI:
    def test_display_menu_contains_options(self):
        menu = display_menu()
        assert "1. Add task" in menu
        assert "6. Exit" in menu

    @pytest.mark.parametrize("valid", ["1", "2", "3", "4", "5", "6"])
    def test_parse_choice_valid(self, valid):
        val = parse_choice(valid)
        assert isinstance(val, int)
        assert 1 <= val <= 6

    @pytest.mark.parametrize("invalid", ["0", "7", "a", "", "-1", " 1", "1 ", "10", "x2", "None"])
    def test_parse_choice_invalid(self, invalid):
        with pytest.raises(ValueError):
            parse_choice(invalid)
