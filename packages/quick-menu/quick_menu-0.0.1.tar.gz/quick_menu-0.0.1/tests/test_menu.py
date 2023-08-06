from unittest.mock import Mock

import pytest  # type: ignore

from quick_menu.menu import Menu, MenuItem


@pytest.fixture
def menu_item():
    item = MenuItem("1", "Label")
    return item


def test_menu_item_default():
    menu_item = MenuItem("1", "First Item")
    assert menu_item.choice == "1"
    assert menu_item.label == "First Item"
    assert menu_item.action is None
    assert menu_item.kwargs == {}
    assert menu_item.is_exit is False


def test_run_action():
    fun = Mock()
    menu_item = MenuItem("1", "Call Func", action=fun)
    ret_val = menu_item.select()
    assert fun.called
    assert ret_val is True


def test_run_menu():
    mock_menu = Mock()
    menu_item = MenuItem("1", "Sub Menu", action=mock_menu.run)
    ret_val = menu_item.select()
    assert mock_menu.run.called
    assert ret_val is True


def test_run_with_exit():
    menu_item = MenuItem("1", "Exit", is_exit=True)
    ret_val = menu_item.select()
    assert ret_val is False


def test_menu(monkeypatch):
    responses = iter(["1", "2", "x"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    func1 = Mock()
    func2 = Mock()
    menu = Menu(
        "Title",
        menu_items=[
            MenuItem("1", "First item", action=func1),
            MenuItem("2", "Second item", action=func2),
            MenuItem("X", "Exit", is_exit=True),
        ],
    )
    menu.run()
    assert func1.called
    assert func2.called


def test_submenu(monkeypatch):
    responses = iter(["S", "1", "B", "x"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    func1 = Mock()
    submenu = (
        Menu("Submenu Title").add(MenuItem("1", "Func1", action=func1)).add(MenuItem("B", "Go back", is_exit=True))
    )
    menu = Menu("Menu Title").add(MenuItem("S", "Submenu", action=submenu.run)).add(MenuItem("X", "Exit", is_exit=True))
    menu.run()
    assert func1.called


def test_menu_display():
    expected = """\
============== Menu Title ==============
1: Item 1
S: Submenu
X: Exit
========================================"""
    menu = (
        Menu("Menu Title")
        .add(MenuItem("1", "Item 1"))
        .add(MenuItem("S", "Submenu"))
        .add(MenuItem("X", "Exit", is_exit=True))
    )
    assert menu.display() == expected


def test_func_with_kwargs(monkeypatch):
    responses = iter(["1", "x"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    func1 = Mock()
    menu = Menu(
        "Title",
        menu_items=[
            MenuItem("1", "First item", action=func1, kwargs={"val": 4}),
            MenuItem("X", "Exit", is_exit=True),
        ],
    )
    menu.run()
    func1.assert_called_once_with(val=4)
