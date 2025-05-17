import pytest
from metagraph.parser import parse_input

def test_parse_basic(tmp_path):
    """
    Проверяем корректность парсинга простого входного файла.
    """
    # Создаем тестовый файл
    content = """
    2 1
    1 2 
    5
    min
    v 1
    """
    # Создаём временный файл
    fn = tmp_path / "test_input.txt"
    fn.write_text(content)
    
    # Парсим файл
    nv, ne, edges, vr, er = parse_input(str(fn))
    
    # Проверяем правильность парсинга
    assert nv == 2
    assert ne == 1
    assert edges == [(1, 2)]
    assert vr == ['5', 'min']
    assert er == ['v 1']