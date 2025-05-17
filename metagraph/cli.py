"""
Командная обертка для работы с метаграфами.
Написал: Бахрами Амир, для проекта по графовым моделям.
"""
import argparse
import logging
from metagraph.parser import parse_input
from metagraph.evaluator import calculate_attributes
from metagraph.visualizer import visualize

def main():
    # Настраиваем аргументы для запуска
    parser = argparse.ArgumentParser(
        description="Программа для обработки метаграфов (парсинг, атрибуты, картинки)"
    )
    parser.add_argument('input_file', help="Файл с описанием метаграфа")  # Поменял имя
    parser.add_argument('output_file', help="Куда сохранить результаты")
    parser.add_argument('--visualize', action='store_true', help="Нарисовать граф")  # Другое имя
    parser.add_argument('--log-level', default='INFO', help="Логи: DEBUG, INFO, WARNING")
    
    args = parser.parse_args()

    # Настраиваем логи, добавил свой формат
    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s | %(levelname)s | %(message)s"  # Слегка изменил
    )

    # Читаем входной файл
    logging.info(f"Загружаю {args.input_file}...")
    nv, ne, edges, vr, er = parse_input(args.input_file)
    
    # Считаем атрибуты
    values = calculate_attributes(nv, ne, edges, vr, er)

    # Сохраняем результаты
    # TODO: Добавить опцию для формата вывода (csv?)
    with open(args.output_file, 'w') as out:
        for v in range(1, nv+1):
            out.write(f"Vertex {v}: {values[('v',v)]}\n")  # Более читаемый вывод
        for e in range(1, ne+1):
            out.write(f"Edge {e}: {values[('e',e)]}\n")
    
    logging.info(f"Результаты сохранены в {args.output_file}")

    # Если попросили визуализацию
    if args.visualize:
        visualize(nv, ne, edges, vr, er, values)
        logging.info("Картинка metagraph.png готова!")