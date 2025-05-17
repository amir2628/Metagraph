"""
Модуль парсинга входного файла метаграфа.
Автор: Бахрами Амир
"""
import logging


def parse_input(filename: str):
    """
    Считывает файл с описанием метаграфа.
    
    Формат входного файла:
    - 1 строка: количество вершин и рёбер (NV NE)
    - NE строк с описанием рёбер (from to)
    - NV строк с правилами для вершин
    - NE строк с правилами для рёбер
    
    Возвращает: количество вершин, количество рёбер, список рёбер, 
                правила для вершин, правила для рёбер
    """
    logging.info(f"Чтение и разбор файла {filename}")
    lines = []
    
    # Пробуем открыть файл в разных кодировках
    encodings = ['utf-8', 'cp1251', 'latin-1']
    for enc in encodings:
        try:
            with open(filename, encoding=enc) as f:
                raw = f.read()
            logging.info(f"Файл успешно прочитан в кодировке {enc}")
            break
        except UnicodeDecodeError:
            continue
    else:
        # Если ни одна кодировка не подошла
        raise IOError(f"Не удалось декодировать файл. Проверьте кодировку (поддерживаются: {', '.join(encodings)})")
    
    # Обрабатываем строки, пропуская комментарии и пустые линии
    for ln in raw.splitlines():
        # Отбрасываем комментарии и пробелы по краям
        txt = ln.split('#', 1)[0].strip()
        if txt:  # Если что-то осталось после удаления комментариев
            lines.append(txt)
    
    # Проверяем, что файл не пустой
    if len(lines) < 1:
        raise ValueError("Пустой или некорректный файл")
    
    # Считываем количество вершин и рёбер
    parts = lines[0].split()
    nv, ne = map(int, parts[:2])
    
    # Считываем список рёбер
    edges = []
    for i in range(1, ne + 1):
        if i >= len(lines):
            raise ValueError(f"Неполное описание рёбер. Ожидалось {ne}, получено {i-1}")
        u, v = map(int, lines[i].split())
        edges.append((u, v))
    
    # Индекс начала правил для вершин
    vr_start = 1 + ne
    
    # Считываем правила для вершин
    vertex_rules = lines[vr_start: vr_start + nv]
    if len(vertex_rules) < nv:
        raise ValueError(f"Неполное описание правил для вершин. Ожидалось {nv}, получено {len(vertex_rules)}")
    
    # Считываем правила для рёбер
    edge_rules = lines[vr_start + nv: vr_start + nv + ne]
    if len(edge_rules) < ne:
        raise ValueError(f"Неполное описание правил для рёбер. Ожидалось {ne}, получено {len(edge_rules)}")
    
    logging.info(f"Прочитано: {nv} вершин, {ne} рёбер, {len(vertex_rules)} правил для вершин, {len(edge_rules)} правил для рёбер")
    return nv, ne, edges, vertex_rules, edge_rules