import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False


def test_get_unread_books_returns_only_unread_books() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.mark_as_read("Dune")

    unread_books = collection.get_unread_books()

    assert [book.title for book in unread_books] == ["The Hobbit"]


def test_get_unread_books_returns_empty_for_empty_collection() -> None:
    collection = BookCollection()

    assert collection.get_unread_books() == []


def test_get_unread_books_returns_empty_when_all_books_are_read() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")

    assert collection.get_unread_books() == []


def test_get_unread_books_returns_all_books_when_none_are_read() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    unread_books = collection.get_unread_books()

    assert [book.title for book in unread_books] == ["Dune", "The Hobbit"]


def test_get_unread_books_preserves_order_of_multiple_unread_books() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("1984", "George Orwell", 1949)
    collection.mark_as_read("The Hobbit")

    unread_books = collection.get_unread_books()

    assert [book.title for book in unread_books] == ["Dune", "1984"]


def test_get_unread_books_reflects_books_marked_as_read() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert [book.title for book in collection.get_unread_books()] == ["Dune"]

    collection.mark_as_read("Dune")

    assert collection.get_unread_books() == []


def test_get_unread_books_does_not_mutate_collection() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.mark_as_read("Dune")
    original_books = collection.books.copy()

    unread_books = collection.get_unread_books()
    unread_books.clear()

    assert collection.books == original_books
    assert [book.read for book in collection.books] == [True, False]

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False
