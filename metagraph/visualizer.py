"""
Модуль для рисования метаграфов.
Автор: Бахрами Амир, вдохновлялся визуализациями из курсов по графам.
"""
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import logging
from random import uniform

def tweak_positions(pos, shift=0.15):
    """
    Сдвигаю узлы, если они слипаются. 
    Подобрал shift=0.15 экспериментально.
    """
    new_pos = {}
    seen = set()
    for node, (x, y) in pos.items():
        coord = (round(x, 2), round(y, 2))
        while coord in seen:
            # Случайный сдвиг, чтобы узлы не накладывались
            x += uniform(-shift, shift)
            y += uniform(-shift, shift)
            coord = (round(x, 2), round(y, 2))
        seen.add(coord)
        new_pos[node] = (x, y)
    return new_pos

def visualize(nv, ne, edges, vertex_rules, edge_rules, values=None, output_path="metagraph.png"):
    """
    Рисует метаграф с вершинами и ребрами.
    Пробовал разные layouts, dot от Graphviz лучше всего.
    """
    G = nx.DiGraph()
    
    # Вершины как узлы
    for v in range(1, nv + 1):
        val = f"\n{values[('v', v)]:.2f}" if values else ""  # Поменял формат
        G.add_node(f"v{v}", 
                   label=f"v{v}\n{vertex_rules[v-1]}{val}", 
                   color='skyblue',  # Другой оттенок
                   type='vertex')
    
    # Ребра как узлы
    for e in range(1, ne + 1):
        val = f"\n{values[('e', e)]:.2f}" if values else ""
        G.add_node(f"e{e}", 
                   label=f"e{e}\n{edge_rules[e-1]}{val}", 
                   color='lightcoral',  # Другой цвет
                   type='edge')
    
    # Добавляем связи
    for e_idx, (src, dst) in enumerate(edges, start=1):
        G.add_edge(f"v{src}", f"e{e_idx}", color='gray')
        G.add_edge(f"e{e_idx}", f"v{dst}", color='navy')  # Поменял цвет
    
    plt.figure(figsize=(max(12, nv * 1.2), max(8, ne * 0.8)))  # Уменьшил размер
    
    # Пробуем расположить узлы
    pos = None
    try:
        logging.info("Пробую Graphviz dot...")
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    except Exception as e:
        logging.warning(f"Graphviz не сработал: {e}, беру spring")
        pos = nx.spring_layout(G, seed=42, k=2.0)  # Уменьшил k
    
    # Исправляем наложения
    pos = tweak_positions(pos, shift=0.2)
    
    # Рисуем узлы
    vertex_nodes = [n for n, d in G.nodes(data=True) if d['type'] == 'vertex']
    edge_nodes = [n for n, d in G.nodes(data=True) if d['type'] == 'edge']
    nx.draw_networkx_nodes(G, pos, nodelist=vertex_nodes, node_color='skyblue',
                          node_size=1400, edgecolors='black')
    nx.draw_networkx_nodes(G, pos, nodelist=edge_nodes, node_color='lightcoral',
                          node_size=1400, edgecolors='black')
    
    # Метки
    labels = {n: G.nodes[n]['label'] for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10)  # Увеличил шрифт
    
    # Ребра
    edge_colors = [G.edges[e].get('color', 'navy') for e in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowstyle='->', arrowsize=12)
    
    plt.axis('off')
    
    # Легенда
    legend = [
        Patch(facecolor='skyblue', edgecolor='black', label='Вершина'),
        Patch(facecolor='lightcoral', edgecolor='black', label='Ребро')
    ]
    plt.legend(handles=legend, loc='upper left', fontsize=11)  # Поменял угол
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=250)  # Уменьшил dpi
    plt.close()
    
    logging.info(f"Сохранил граф в {output_path}, надеюсь, красиво!")
    return output_path