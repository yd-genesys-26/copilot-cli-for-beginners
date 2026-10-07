import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app
import books
from books import BookCollection


@pytest.fixture
def collection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> BookCollection:
    data_file = tmp_path / "data.json"
    data_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    book_collection = BookCollection()
    monkeypatch.setattr(book_app, "collection", book_collection)
    return book_collection


def test_list_unread_command_displays_only_unread_books(
    collection: BookCollection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.mark_as_read("Dune")
    monkeypatch.setattr(sys, "argv", ["book_app.py", "list-unread"])

    book_app.main()

    output = capsys.readouterr().out
    assert "The Hobbit by J.R.R. Tolkien (1937)" in output
    assert "Dune by Frank Herbert (1965)" not in output


def test_list_unread_command_reports_empty_result(
    collection: BookCollection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")
    monkeypatch.setattr(sys, "argv", ["book_app.py", "list-unread"])

    book_app.main()

    assert capsys.readouterr().out.strip() == "No books found."
