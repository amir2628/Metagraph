import pytest
from metagraph.evaluator import calculate_attributes

def test_evaluator_simple():
    """Тестирование простого случая расчета атрибутов."""
    nv, ne = 2, 1
    edges = [(1, 2)]
    vr = ['5', 'min']  # правила для вершин
    er = ['v 1']       # правила для рёбер
    
    # Вычисляем атрибуты
    vals = calculate_attributes(nv, ne, edges, vr, er)
    
    # Проверяем результаты
    assert vals[('v', 1)] == 5
    assert vals[('e', 1)] == 5
    assert vals[('v', 2)] == 5