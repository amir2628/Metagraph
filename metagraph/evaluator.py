"""
Модуль вычисления атрибутов метаграфа.
Автор: Бахрами Амир
"""
import logging
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# Псевдонимы для удобства, выбрал покороче, т.к. часто использую
VId = int
EId = int
Attr = float

def build_dependency_graph(
    num_vertices: int,  # Поменял имя для разнообразия
    num_edges: int,
    edges: List[Tuple[int,int]],
    vertex_rules: List[str],
    edge_rules: List[str]
) -> Dict[Tuple[str,int], Set[Tuple[str,int]]]:
    """
    Создает граф зависимостей для вершин и ребер метаграфа.
    Пока обрабатываем только min и * правила, но можно добавить другие.
    """
    deps = {}
    for v in range(1, num_vertices+1):
        deps[('v', v)] = set()
    for e in range(1, num_edges+1):
        deps[('e', e)] = set()
    
    # Собираем ребра, которые входят в каждую вершину
    incoming_edges = defaultdict(list)  # Поменял имя для стиля
    for idx, (u, v) in enumerate(edges, 1):
        incoming_edges[v].append(idx)
    
    # Правила для вершин
    for v in range(1, num_vertices+1):
        rule = vertex_rules[v-1].strip()
        if rule.lower() == 'min':
            # Зависим от всех входящих ребер
            for e in incoming_edges[v]:
                deps[('v', v)].add(('e', e))
        elif rule.startswith('e'):
            idx = int(rule.split()[1])
            deps[('v', v)].add(('e', idx))
    
    # Правила для ребер
    for e in range(1, num_edges+1):
        u, _ = edges[e-1]
        rule = edge_rules[e-1].strip()
        if rule == '*':
            deps[('e', e)].add(('v', u))
            for prev in incoming_edges[u]:
                deps[('e', e)].add(('e', prev))
        elif rule.startswith('v'):
            idx = int(rule.split()[1])
            deps[('e', e)].add(('v', idx))
    
    logging.info("Граф зависимостей готов")  # Слегка изменил сообщение
    return deps

def calculate_attributes(
    nv: int,
    ne: int,
    edges: List[Tuple[int,int]],
    vertex_rules: List[str],
    edge_rules: List[str]
) -> Dict[Tuple[str,int], Attr]:
    """
    Вычисляет атрибуты вершин и ребер. 
    TODO: Добавить поддержку отрицательных значений и обработку ошибок.
    """
    deps = build_dependency_graph(nv, ne, edges, vertex_rules, edge_rules)
    values = {}
    in_progress = set()

    def eval_node(key: Tuple[str,int]) -> Attr:
        """Рекурсивно считаем значение для вершины или ребра."""
        if key in values:
            return values[key]
        
        # Проверяем, нет ли цикла
        if key in in_progress:
            logging.warning(f"Обнаружен цикл для {key}, беру дефолтное значение")
            default = 0.0 if key[0] == 'v' else 1.0
            values[key] = default
            return default
        
        in_progress.add(key)
        kind, idx = key
        
        # Сначала считаем все зависимости
        for dep in deps[key]:
            eval_node(dep)  # Рекурсия для зависимостей
        
        # Теперь считаем свое значение
        if kind == 'v':
            rule = vertex_rules[idx-1].strip()
            try:
                val = float(rule)  # Если это просто число
            except ValueError:
                if rule.lower() == 'min':
                    # Берем минимум из входящих ребер
                    ins = [values[e] for e in deps[key] if e[0] == 'e']
                    val = min(ins) if ins else 0.0
                    # TODO: Может, добавить лог, если ins пустой?
                else:
                    ref = int(rule.split()[1])
                    val = values[('e', ref)]
        else:  # Ребро
            rule = edge_rules[idx-1].strip()
            try:
                val = float(rule)
            except ValueError:
                if rule == '*':
                    u, _ = edges[idx-1]
                    prod = values[('v', u)]
                    for pe in deps[key]:
                        if pe[0] == 'e':
                            prod *= values[pe]
                    val = prod
                else:
                    ref = int(rule.split()[1])
                    val = values[('v', ref)]
        
        values[key] = val
        in_progress.remove(key)
        return val

    # Считаем все вершины и ребра
    for v in range(1, nv+1):
        eval_node(('v', v))
    for e in range(1, ne+1):
        eval_node(('e', e))
    
    logging.info("Все атрибуты посчитаны, готово!")  # Разговорный стиль
    return values