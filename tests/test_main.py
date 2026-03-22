import os
import sys
import pytest
import builtins

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import clear_screen, show_menu, main, select_id
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


def test_main_exits_on_option_6(monkeypatch, capsys, tmp_path):
    """Test that main() exits when user selects option 6."""
    monkeypatch.setenv('TASKS_FILE_PATH', str(tmp_path / 'tasks.json'))

    # Mock input to return OPTION_6 immediately
    inputs = iter([copywrite.OPTION_6])
    monkeypatch.setattr(builtins, 'input', lambda prompt: next(inputs))

    # Call main - it should exit after one iteration
    main()

    # Check that GOOD_BYE was printed
    captured = capsys.readouterr()
    assert copywrite.GOOD_BYE in captured.out


def test_main_handles_invalid_option(monkeypatch, capsys, tmp_path):
    """Test that main() shows invalid option message and continues."""
    monkeypatch.setenv('TASKS_FILE_PATH', str(tmp_path / 'tasks.json'))

    # Mock input: invalid option, press key, then exit
    inputs = iter(["invalid", "enter", copywrite.OPTION_6])
    monkeypatch.setattr(builtins, 'input', lambda prompt: next(inputs))

    main()

    captured = capsys.readouterr()
    assert copywrite.INVALID_OPTION_MSG in captured.out
    assert copywrite.GOOD_BYE in captured.out


def test_select_id_retries_invalid_input(monkeypatch, capsys):
    """Test that select_id retries on invalid numeric entry."""
    inputs = iter(["abc", "100"])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

    value = select_id("Enter ID: ")

    captured = capsys.readouterr()
    assert "Please introduce a numeric id" in captured.out
    assert value == 100


def test_main_complex_task_fallback_to_add_task(monkeypatch, capsys, tmp_path):
    """Test that main() falls back to add_task when complex task assistant fails."""
    monkeypatch.setenv('TASKS_FILE_PATH', str(tmp_path / 'tasks.json'))

    # Force call_cohere_generate_subtasks to throw
    monkeypatch.setattr('main.call_cohere_generate_subtasks', lambda description: (_ for _ in ()).throw(Exception('API fail')))

    inputs = iter([copywrite.OPTION_2, 'Fallback task', '', copywrite.OPTION_6])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

    main()

    captured = capsys.readouterr()
    assert "Something went wrong. (AI service error)" in captured.out
    assert "[Fallback task] " in captured.out
    assert copywrite.CREATE_TASK_SUCCESS in captured.out


def test_main_complex_task_success(monkeypatch, capsys, tmp_path):
    """Test that main() outputs generated subtasks when AI assistant succeeds."""
    monkeypatch.setenv('TASKS_FILE_PATH', str(tmp_path / 'tasks.json'))
    monkeypatch.setattr('main.call_cohere_generate_subtasks', lambda description: ['A', 'B', 'C'])

    inputs = iter([copywrite.OPTION_2, 'Generate me tasks', '', copywrite.OPTION_6])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

    main()

    captured = capsys.readouterr()
    assert "[Generating subtasks...]" in captured.out
    assert "3 Complex task subtasks generated successfully" in captured.out

