"""
Módulo para gerar grafos temáticos para os níveis
"""
import networkx as nx
import random

def generate_castle_graph():
    """Gera um grafo simples em forma de castelo (Nível 1)"""
    G = nx.Graph()
    
    # Adiciona nós com posições
    nodes = {
        0: (2, 3),    # Entrada (A)
        1: (4, 3),    # Torre (B)
        2: (2, 1),    # Masmorra (C)
        3: (4, 1),    # Saída (D)
    }
    
    # Adiciona nós com posições
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=["Entrada", "Torre", "Masmorra", "Saída"][node])
    
    # Adiciona arestas com pesos
    edges = [
        (0, 1, 3),  # Entrada -> Torre
        (0, 2, 4),  # Entrada -> Masmorra
        (1, 3, 5),  # Torre -> Saída
        (2, 3, 2),  # Masmorra -> Saída
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 3  # start, end

def generate_forest_graph():
    """Gera um grafo médio em forma de floresta (Nível 2)"""
    G = nx.Graph()
    
    nodes = {
        0: (1, 4),    # Início
        1: (2, 5),
        2: (3, 4),
        3: (2, 3),
        4: (1, 2),
        5: (3, 2),
        6: (2, 1),    # Saída
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 2),
        (0, 3, 3),
        (1, 2, 2),
        (1, 3, 1),
        (2, 5, 3),
        (3, 4, 2),
        (3, 6, 4),
        (4, 6, 3),
        (5, 6, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 6

def generate_city_graph():
    """Gera um grafo complexo em forma de cidade (Nível 3)"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 4),
        1: (1, 5),
        2: (2, 4),
        3: (3, 5),
        4: (1, 3),
        5: (2, 2),
        6: (3, 3),
        7: (1, 1),
        8: (3, 1),
        9: (4, 2),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 2), (0, 4, 3), (1, 2, 2), (1, 4, 1),
        (2, 3, 2), (2, 5, 3), (3, 6, 2), (4, 5, 2),
        (4, 7, 3), (5, 6, 2), (5, 8, 2), (6, 9, 3),
        (7, 8, 2), (8, 9, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 9

def generate_alien_graph():
    """Gera um grafo muito complexo para alienígenas (Nível 4)"""
    G = nx.complete_graph(8)
    
    # Atribui posições em círculo
    import math
    for i in range(8):
        angle = 2 * math.pi * i / 8
        x = 3 + 2 * math.cos(angle)
        y = 3 + 2 * math.sin(angle)
        G.nodes[i]['pos'] = (x, y)
        G.nodes[i]['name'] = f"Nó {i}"
    
    # Atribui pesos aleatórios
    random.seed(42)
    for start, end in G.edges():
        if start < end:  # Para não adicionar duas vezes
            weight = random.randint(1, 8)
            G[start][end]['weight'] = weight
    
    return G, 0, 7

def get_level_config(level_id):
    """Retorna a configuração de um nível"""
    levels = {
        1: {
            "name": "🏰 Castelo Encantado",
            "description": "Fuja do castelo encantado no menor tempo!",
            "difficulty": "Fácil",
            "time_limit": 120,
            "generator": generate_castle_graph,
        },
        2: {
            "name": "🌲 Floresta Mágica",
            "description": "Navegue pela floresta repleta de magia!",
            "difficulty": "Normal",
            "time_limit": 180,
            "generator": generate_forest_graph,
        },
        3: {
            "name": "🏙️ Cidade Futurista",
            "description": "Escape da metrópole do futuro!",
            "difficulty": "Difícil",
            "time_limit": 240,
            "generator": generate_city_graph,
        },
        4: {
            "name": "👽 Dimensão Alienígena",
            "description": "Sobreviva em uma dimensão desconhecida!",
            "difficulty": "Extremo",
            "time_limit": 300,
            "generator": generate_alien_graph,
        },
    }
    return levels.get(level_id)
