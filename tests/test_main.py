import os
import sys
import pytest
import builtins

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import clear_screen, show_menu, main
import copywrite


def test_clear_screen_prints_ansi_escape(capsys):
    """Test that clear_screen prints the ANSI escape sequence."""
    clear_screen()
    captured = capsys.readouterr()
    assert "\033[2J\033[H\n" in captured.out


def test_show_menu_prints_menu_options(capsys):
    """Test that show_menu prints the menu title and options."""
    show_menu()
    captured = capsys.readouterr()
    assert copywrite.MENU_TITLE in captured.out
    assert copywrite.MENU_OPTION_1 in captured.out
    assert copywrite.MENU_OPTION_2 in captured.out
    assert copywrite.MENU_OPTION_3 in captured.out
    assert copywrite.MENU_OPTION_4 in captured.out
    assert copywrite.MENU_OPTION_5 in captured.out


def test_main_exits_on_option_5(monkeypatch, capsys):
    """Test that main() exits when user selects option 5."""
    # Mock input to return OPTION_5 immediately
    inputs = iter([copywrite.OPTION_5])
    monkeypatch.setattr(builtins, 'input', lambda prompt: next(inputs))

    # Call main - it should exit after one iteration
    main()

    # Check that GOOD_BYE was printed
    captured = capsys.readouterr()
    assert copywrite.GOOD_BYE in captured.out


def test_main_handles_invalid_option(monkeypatch, capsys):
    """Test that main() shows invalid option message and continues."""
    # Mock input: invalid option, press key, then exit
    inputs = iter(["invalid", "enter", copywrite.OPTION_5])
    monkeypatch.setattr(builtins, 'input', lambda prompt: next(inputs))

    main()

    captured = capsys.readouterr()
    assert copywrite.INVALID_OPTION_MSG in captured.out
    assert copywrite.GOOD_BYE in captured.out