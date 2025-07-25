import pytest

from main import main, calc_avg
from exceptions import EmptyList


def test_type_main():
    """Проверка возвращаемого типа."""
    assert isinstance(main(['example1.log'], 'average'), dict)


def test_empty_args():
    """Проверка пустых аргументов."""
    with pytest.raises(EmptyList):
        main([], 'average')


def test_wrong_filename():
    """Проверка неверного названия файлов."""
    assert not main(['incorrect.log'], 'average')


def test_missing_key():
    """Проверка отсутствия ключа."""
    with pytest.raises(KeyError):
        with open('wronglog.log', 'r', encoding='utf-8') as file:
            calc_avg(file, 'average')
