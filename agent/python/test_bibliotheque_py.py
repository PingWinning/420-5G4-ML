"""Test minimal du module pybind11 sur une copie de data/."""

import hashlib
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
BUILD_DIR = Path(os.environ.get("BIBLIOTHEQUE_PY_BUILD", ROOT / "build"))

sys.path.insert(0, str(BUILD_DIR))

import bibliotheque_py  # noqa: E402


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source_hashes = {
        name: file_hash(DATA_DIR / name) for name in ("books.txt", "users.txt")
    }

    with tempfile.TemporaryDirectory() as tmp:
        copied_data = Path(tmp) / "data"
        shutil.copytree(DATA_DIR, copied_data)

        library = bibliotheque_py.load_library(str(copied_data))
        books = library.all_books()

        expected_count = sum(
            1
            for line in (copied_data / "books.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        )

        assert len(books) == expected_count
        assert library.total_books == expected_count
        assert all(isinstance(book, bibliotheque_py.Book) for book in books)

        by_title = {book.title: book for book in books}
        assert by_title["Le Petit Prince"].available is True
        assert by_title["Les Misérables"].available is False
        assert by_title["Les Misérables"].borrower_id == "USR001"
        assert by_title["Le Petit Prince"].author == "Antoine de Saint-Exupéry"

        assert library.available_count == sum(1 for book in books if book.available)
        assert library.checked_out_count == library.total_books - library.available_count
        assert library.users_count > 0

    assert source_hashes == {
        name: file_hash(DATA_DIR / name) for name in ("books.txt", "users.txt")
    }

    print(f"OK : {len(books)} livres chargés depuis une copie de data/")


if __name__ == "__main__":
    main()
