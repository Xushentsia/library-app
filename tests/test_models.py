import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from models import Book


def test_book_creation():
    """Проверяет, что объект Book создаётся с правильными полями"""
    book = Book(
        id=1,
        title="Война и мир",
        author="Лев Толстой",
        year=1869,
        description="Роман-эпопея"
    )

    assert book.id == 1
    assert book.title == "Война и мир"
    assert book.author == "Лев Толстой"
    assert book.year == 1869
    assert book.description == "Роман-эпопея"


def test_book_optional_fields():
    """Проверяет, что year и description могут быть None (необязательные поля)"""
    # Создаём книгу только с обязательными полями
    book = Book(
        title="Евгений Онегин",
        author="Александр Пушкин"
    )

    # Проверяем что книга создалась с переданными значениями
    assert book.title == "Евгений Онегин"
    assert book.author == "Александр Пушкин"

    # Проверяем что необязательные поля равны None
    assert book.year is None
    assert book.description is None