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
    """Retorna a configuração de um nível (1-20)"""
    levels = {
        # FÁCIL (1-5) - Introdução aos conceitos
        1: {
            "name": "🏯 Dojo dos Iniciantes",
            "description": "Fuja do castelo encantado no menor tempo!",
            "difficulty": "Fácil",
            "time_limit": 120,
            "generator": generate_castle_graph,
        },
        2: {
            "name": "🌲 Floresta dos Shinobi",
            "description": "Navegue pela floresta repleta de magia!",
            "difficulty": "Fácil",
            "time_limit": 130,
            "generator": generate_forest_graph,
        },
        3: {
            "name": "⛩️ Templo dos Samurai",
            "description": "Explore as ruínas do templo perdido!",
            "difficulty": "Fácil",
            "time_limit": 140,
            "generator": generate_temple_graph,
        },
        4: {
            "name": "🏝️ Ilha dos Ronin",
            "description": "Atravesse a ilha repleta de mistérios!",
            "difficulty": "Fácil",
            "time_limit": 150,
            "generator": generate_island_graph,
        },
        5: {
            "name": "⚡ Vale dos Raijin",
            "description": "Escape do laboratório carregado de energia!",
            "difficulty": "Fácil",
            "time_limit": 160,
            "generator": generate_lab_graph,
        },
        
        # MÉDIO (6-10) - Complexidade crescente
        6: {
            "name": "🌃 Edo dos Ninja",
            "description": "Escape da metrópole do futuro!",
            "difficulty": "Médio",
            "time_limit": 180,
            "generator": generate_city_graph,
        },
        7: {
            "name": "🌋 Montanha do Dragão",
            "description": "Fuja antes que a lava chegue até você!",
            "difficulty": "Médio",
            "time_limit": 200,
            "generator": generate_volcano_graph,
        },
        8: {
            "name": "❄️ Picos de Yuki-Onna",
            "description": "Navegue pelas cavernas congelantes!",
            "difficulty": "Médio",
            "time_limit": 220,
            "generator": generate_ice_caves_graph,
        },
        9: {
            "name": "🎆 Festival Matsuri",
            "description": "Encontre a saída no circo encantado!",
            "difficulty": "Médio",
            "time_limit": 240,
            "generator": generate_circus_graph,
        },
        10: {
            "name": "☁️ Fortaleza Celestial",
            "description": "Escape da estação antes da explosão!",
            "difficulty": "Médio",
            "time_limit": 260,
            "generator": generate_space_station_graph,
        },
        
        # MÉDIO AVANÇADO (11-15) - Desafios maiores
        11: {
            "name": "🏰 Palácio do Shogun",
            "description": "Atravesse o lar do dragão ancestral!",
            "difficulty": "Médio Avançado",
            "time_limit": 280,
            "generator": generate_dragon_castle_graph,
        },
        12: {
            "name": "🌀 Portal dos Kami",
            "description": "Navegue entre as dimensões paralelas!",
            "difficulty": "Médio Avançado",
            "time_limit": 300,
            "generator": generate_portal_graph,
        },
        13: {
            "name": "🏙️ Kyoto Fantasma",
            "description": "Escape da cidade fantasma!",
            "difficulty": "Médio Avançado",
            "time_limit": 320,
            "generator": generate_abandoned_city_graph,
        },
        14: {
            "name": "🌀 Labirinto Zen",
            "description": "Resolva o puzzle da física quântica!",
            "difficulty": "Médio Avançado",
            "time_limit": 340,
            "generator": generate_quantum_maze_graph,
        },
        15: {
            "name": "⚔️ Arena do Bushido",
            "description": "Sobreviva na arena dos campeões!",
            "difficulty": "Médio Avançado",
            "time_limit": 360,
            "generator": generate_gladiator_arena_graph,
        },
        
        # DIFÍCIL (16-20) - Máximo desafio
        16: {
            "name": "✨ Via Láctea Shinobi",
            "description": "Navegue pelos confins do universo!",
            "difficulty": "Difícil",
            "time_limit": 400,
            "generator": generate_galaxy_graph,
        },
        17: {
            "name": "🌸 Santuário dos Ancestrais",
            "description": "Desvende os segredos da magia antiga!",
            "difficulty": "Difícil",
            "time_limit": 420,
            "generator": generate_arcane_matrix_graph,
        },
        18: {
            "name": "🌙 Torre da Lua Negra",
            "description": "Evite o colapso do reator!",
            "difficulty": "Difícil",
            "time_limit": 440,
            "generator": generate_nuclear_reactor_graph,
        },
        19: {
            "name": "Tempestade Temporal",
            "description": "Escape da distorção do tempo!",
            "difficulty": "Difícil",
            "time_limit": 460,
            "generator": generate_time_storm_graph,
        },
        20: {
            "name": "👑 Ascensão do Mestre",
            "description": "Sobreviva na dimensão desconhecida!",
            "difficulty": "Difícil",
            "time_limit": 480,
            "generator": generate_alien_graph,
        },
    }
    return levels.get(level_id)

# ===== NOVOS NÍVEIS FÁCEIS (3-5) =====

def generate_temple_graph():
    """Gera o grafo do templo antigo - Fácil"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 3),
        1: (1, 4),
        2: (2, 3),
        3: (1, 2),
        4: (2, 1),
        5: (3, 2),
        6: (3, 4),
        7: (4, 3),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 2),
        (0, 3, 3),
        (1, 2, 2),
        (1, 6, 2),
        (2, 7, 3),
        (3, 4, 2),
        (4, 5, 2),
        (5, 7, 2),
        (6, 7, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 7

def generate_island_graph():
    """Gera o grafo da ilha misteriosa - Fácil"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 4),
        1: (1, 3),
        2: (2, 4),
        3: (1, 1),
        4: (3, 2),
        5: (4, 3),
        6: (3, 0),
        7: (5, 2),
        8: (4, 5),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 2),
        (0, 2, 3),
        (1, 3, 2),
        (2, 4, 2),
        (2, 8, 3),
        (3, 6, 3),
        (4, 5, 2),
        (4, 7, 2),
        (5, 7, 2),
        (5, 8, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 8

def generate_lab_graph():
    """Gera o grafo do laboratório elétrico - Fácil"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 2),
        1: (1, 3),
        2: (2, 2),
        3: (3, 3),
        4: (1, 1),
        5: (3, 1),
        6: (4, 2),
        7: (2, 4),
        8: (4, 4),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 2),
        (0, 4, 2),
        (1, 2, 2),
        (1, 7, 3),
        (2, 3, 2),
        (2, 5, 3),
        (3, 6, 2),
        (3, 8, 2),
        (4, 5, 2),
        (6, 8, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 8

# ===== NOVOS NÍVEIS MÉDIOS (7-10) =====

def generate_volcano_graph():
    """Gera o grafo do vulcão ativo - Médio"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 4),
        1: (1, 5),
        2: (2, 4),
        3: (3, 5),
        4: (1, 3),
        5: (2, 2),
        6: (3, 3),
        7: (4, 4),
        8: (1, 1),
        9: (3, 1),
        10: (4, 2),
        11: (5, 3),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 3), (0, 4, 2), (1, 2, 2), (1, 4, 3),
        (2, 3, 2), (2, 5, 3), (3, 6, 2), (3, 7, 3),
        (4, 5, 2), (4, 8, 3), (5, 6, 2), (5, 9, 2),
        (6, 7, 2), (6, 10, 3), (7, 11, 2), (8, 9, 2),
        (9, 10, 2), (10, 11, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 11

def generate_ice_caves_graph():
    """Gera o grafo das cavernas geladas - Médio"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 3),
        1: (1, 4),
        2: (2, 3),
        3: (3, 4),
        4: (1, 2),
        5: (2, 1),
        6: (3, 2),
        7: (4, 3),
        8: (1, 0),
        9: (4, 1),
        10: (5, 2),
        11: (4, 5),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 2), (0, 4, 3), (1, 2, 3), (1, 3, 2),
        (2, 6, 2), (3, 7, 2), (3, 11, 3), (4, 5, 2),
        (4, 8, 2), (5, 6, 3), (5, 9, 2), (6, 7, 2),
        (6, 10, 3), (7, 10, 2), (8, 9, 3), (9, 10, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 11

def generate_circus_graph():
    """Gera o grafo do circo mágico - Médio"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 4),
        1: (1, 5),
        2: (2, 4),
        3: (3, 5),
        4: (1, 3),
        5: (2, 2),
        6: (3, 3),
        7: (4, 4),
        8: (0, 2),
        9: (1, 1),
        10: (3, 1),
        11: (4, 2),
        12: (5, 3),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 2), (0, 4, 3), (0, 8, 2), (1, 2, 2), (1, 4, 3),
        (2, 3, 2), (2, 5, 3), (3, 6, 2), (3, 7, 3), (4, 5, 2),
        (4, 9, 2), (5, 6, 2), (5, 10, 3), (6, 7, 2), (6, 11, 2),
        (7, 12, 2), (8, 9, 2), (9, 10, 2), (10, 11, 2), (11, 12, 3),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 12

def generate_space_station_graph():
    """Gera o grafo da estação espacial - Médio"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 4),
        1: (1, 5),
        2: (2, 4),
        3: (3, 5),
        4: (1, 3),
        5: (2, 2),
        6: (3, 3),
        7: (4, 4),
        8: (0, 2),
        9: (1, 1),
        10: (3, 1),
        11: (4, 2),
        12: (5, 3),
        13: (2, 6),
        14: (4, 6),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 2), (0, 4, 3), (0, 8, 2), (1, 2, 2), (1, 13, 3),
        (2, 3, 2), (2, 5, 3), (3, 6, 2), (3, 7, 3), (4, 5, 2),
        (4, 9, 2), (5, 6, 2), (5, 10, 3), (6, 7, 2), (6, 11, 2),
        (7, 12, 2), (7, 14, 3), (8, 9, 2), (9, 10, 2), (10, 11, 2),
        (11, 12, 3), (13, 14, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 14

# ===== NOVOS NÍVEIS MÉDIO AVANÇADO (11-15) =====

def generate_dragon_castle_graph():
    """Gera o grafo do castelo do dragão - Médio Avançado"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 5), 1: (1, 6), 2: (2, 5), 3: (3, 6),
        4: (1, 4), 5: (2, 3), 6: (3, 4), 7: (4, 5),
        8: (0, 3), 9: (1, 2), 10: (3, 2), 11: (4, 3),
        12: (5, 4), 13: (1, 0), 14: (3, 0), 15: (5, 2),
        16: (6, 3), 17: (2, 7), 18: (4, 7), 19: (6, 5),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 3), (0, 4, 2), (0, 8, 3), (1, 2, 2), (1, 17, 4),
        (2, 3, 2), (2, 5, 3), (3, 6, 2), (3, 18, 4), (4, 5, 2),
        (4, 9, 2), (5, 6, 2), (5, 10, 3), (6, 7, 2), (6, 11, 2),
        (7, 12, 2), (7, 19, 3), (8, 9, 2), (9, 10, 3), (9, 13, 3),
        (10, 11, 2), (10, 14, 2), (11, 12, 3), (11, 15, 2),
        (12, 16, 2), (13, 14, 2), (14, 15, 3), (15, 16, 2), (16, 19, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 19

def generate_portal_graph():
    """Gera o grafo do portal dimensional - Médio Avançado"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 4), 1: (1, 5), 2: (2, 4), 3: (3, 5),
        4: (1, 3), 5: (2, 2), 6: (3, 3), 7: (4, 4),
        8: (0, 2), 9: (1, 1), 10: (3, 1), 11: (4, 2),
        12: (5, 3), 13: (2, 6), 14: (4, 6), 15: (5, 1),
        16: (6, 2), 17: (6, 4), 18: (0, 6), 19: (1, 7),
        20: (3, 7), 21: (5, 5), 22: (7, 3), 23: (7, 5),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 3), (0, 4, 2), (0, 8, 4), (1, 2, 2), (1, 13, 4),
        (2, 3, 3), (2, 5, 2), (3, 6, 2), (3, 20, 4), (4, 5, 2),
        (4, 9, 3), (5, 6, 2), (5, 10, 3), (6, 7, 2), (6, 11, 2),
        (7, 12, 3), (7, 14, 4), (8, 9, 2), (8, 18, 3), (9, 10, 2),
        (10, 11, 2), (10, 15, 3), (11, 12, 2), (11, 16, 3),
        (12, 17, 2), (12, 21, 3), (13, 19, 3), (14, 21, 2),
        (15, 16, 2), (16, 17, 3), (16, 22, 4), (17, 22, 2),
        (17, 23, 2), (21, 23, 3), (22, 23, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 23

def generate_abandoned_city_graph():
    """Gera o grafo da metrópole abandonada - Médio Avançado"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 5), 1: (1, 6), 2: (2, 5), 3: (3, 6),
        4: (1, 4), 5: (2, 3), 6: (3, 4), 7: (4, 5),
        8: (0, 3), 9: (1, 2), 10: (3, 2), 11: (4, 3),
        12: (5, 4), 13: (1, 0), 14: (3, 0), 15: (5, 2),
        16: (6, 3), 17: (7, 4), 18: (2, 7), 19: (4, 7),
        20: (6, 1), 21: (7, 2), 22: (0, 1), 23: (5, 6),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (0, 1, 3), (0, 4, 2), (0, 8, 3), (1, 2, 2), (1, 18, 4),
        (2, 3, 2), (2, 5, 3), (3, 6, 2), (3, 19, 4), (4, 5, 2),
        (4, 9, 2), (5, 6, 2), (5, 10, 3), (6, 7, 2), (6, 11, 2),
        (7, 12, 2), (7, 23, 3), (8, 9, 2), (8, 22, 2), (9, 10, 3),
        (9, 13, 3), (10, 11, 2), (10, 14, 2), (11, 12, 3), (11, 15, 2),
        (12, 16, 2), (13, 14, 2), (13, 22, 3), (14, 15, 3), (15, 16, 2),
        (15, 20, 3), (16, 17, 2), (16, 21, 2), (17, 21, 2), (20, 21, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 0, 17

def generate_quantum_maze_graph():
    """Gera o grafo do labirinto quântico - Médio Avançado"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 4), 1: (1, 5), 2: (2, 4), 3: (3, 5),
        4: (1, 3), 5: (2, 2), 6: (3, 3), 7: (4, 4),
        8: (0, 2), 9: (1, 1), 10: (3, 1), 11: (4, 2),
        12: (5, 3), 13: (2, 6), 14: (4, 6), 15: (5, 1),
        16: (6, 2), 17: (6, 4), 18: (7, 3), 19: (0, 0),
        20: (2, 0), 21: (4, 0), 22: (6, 0), 23: (7, 1),
        24: (1, 7), 25: (3, 7), 26: (5, 5), 27: (7, 5),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (19, 8, 3), (19, 20, 4), (20, 9, 2), (20, 21, 4),
        (8, 0, 2), (8, 9, 2), (9, 4, 2), (9, 10, 3),
        (0, 1, 3), (0, 4, 2), (1, 2, 2), (1, 13, 4),
        (2, 3, 3), (2, 5, 2), (4, 5, 2), (5, 6, 2),
        (5, 10, 3), (6, 7, 2), (6, 11, 2), (10, 11, 2),
        (10, 15, 3), (11, 12, 3), (11, 16, 2), (15, 16, 2),
        (15, 22, 4), (16, 17, 2), (16, 23, 3), (12, 17, 2),
        (12, 26, 3), (17, 18, 2), (17, 27, 3), (21, 23, 3),
        (22, 23, 2), (23, 18, 2), (18, 27, 2), (3, 25, 4),
        (7, 14, 4), (13, 24, 3), (14, 26, 2), (26, 27, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 19, 27

def generate_gladiator_arena_graph():
    """Gera o grafo da arena de gladiadores - Médio Avançado"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 4), 1: (1, 5), 2: (2, 4), 3: (3, 5),
        4: (1, 3), 5: (2, 2), 6: (3, 3), 7: (4, 4),
        8: (0, 2), 9: (1, 1), 10: (3, 1), 11: (4, 2),
        12: (5, 3), 13: (2, 6), 14: (4, 6), 15: (5, 1),
        16: (6, 2), 17: (6, 4), 18: (7, 3), 19: (0, 6),
        20: (1, 7), 21: (3, 7), 22: (5, 5), 23: (6, 6),
        24: (7, 5), 25: (0, 0), 26: (2, 0), 27: (4, 0),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (25, 8, 3), (25, 26, 4), (26, 9, 2), (26, 27, 4),
        (8, 0, 2), (8, 9, 2), (9, 4, 2), (9, 10, 3),
        (0, 1, 3), (0, 4, 2), (0, 19, 4), (1, 2, 2), (1, 13, 4),
        (2, 3, 3), (2, 5, 2), (4, 5, 2), (5, 6, 2),
        (5, 10, 3), (6, 7, 2), (6, 11, 2), (10, 11, 2),
        (10, 15, 3), (11, 12, 3), (11, 16, 2), (15, 16, 2),
        (12, 17, 2), (12, 22, 3), (16, 17, 2), (16, 18, 2),
        (17, 18, 2), (17, 23, 2), (18, 24, 2), (7, 14, 4),
        (13, 20, 3), (14, 22, 2), (19, 20, 2), (20, 21, 2),
        (21, 22, 3), (22, 23, 2), (23, 24, 2), (27, 15, 3),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 25, 24

# ===== NOVOS NÍVEIS DIFÍCEIS (16-19) =====

def generate_galaxy_graph():
    """Gera o grafo da galáxia perdida - Difícil"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 5), 1: (1, 6), 2: (2, 5), 3: (3, 6), 4: (4, 5),
        5: (1, 4), 6: (2, 3), 7: (3, 4), 8: (4, 3), 9: (5, 4),
        10: (0, 3), 11: (1, 2), 12: (3, 2), 13: (4, 1), 14: (5, 2),
        15: (6, 3), 16: (1, 0), 17: (3, 0), 18: (5, 0), 19: (6, 1),
        20: (7, 2), 21: (2, 7), 22: (4, 7), 23: (6, 5), 24: (7, 4),
        25: (0, 1), 26: (2, 1), 27: (7, 0), 28: (0, 7), 29: (1, 8),
        30: (3, 8), 31: (5, 6), 32: (7, 6), 33: (8, 3), 34: (8, 5),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (25, 10, 3), (25, 16, 4), (16, 11, 2), (16, 26, 3), (16, 17, 4),
        (10, 0, 2), (10, 11, 2), (11, 5, 2), (11, 12, 3), (26, 6, 2),
        (0, 1, 3), (0, 5, 2), (0, 28, 4), (1, 2, 2), (1, 21, 4),
        (5, 6, 2), (6, 7, 2), (6, 12, 3), (2, 3, 3), (2, 7, 2),
        (7, 8, 2), (7, 12, 2), (12, 13, 2), (12, 17, 3), (13, 14, 3),
        (13, 18, 4), (17, 18, 2), (18, 19, 2), (19, 20, 2), (19, 27, 4),
        (8, 9, 2), (8, 14, 2), (14, 15, 3), (14, 19, 2), (9, 15, 2),
        (9, 23, 4), (15, 20, 2), (15, 23, 2), (20, 24, 2), (20, 27, 3),
        (3, 4, 2), (3, 22, 4), (4, 9, 2), (4, 31, 3), (23, 24, 2),
        (23, 31, 2), (24, 32, 2), (24, 33, 3), (31, 32, 3), (32, 34, 2),
        (21, 29, 3), (22, 30, 3), (28, 29, 2), (29, 30, 2), (33, 34, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 25, 34

def generate_arcane_matrix_graph():
    """Gera o grafo da matriz arcana - Difícil"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 6), 1: (1, 7), 2: (2, 6), 3: (3, 7), 4: (4, 6),
        5: (1, 5), 6: (2, 4), 7: (3, 5), 8: (4, 4), 9: (5, 5),
        10: (0, 4), 11: (1, 3), 12: (3, 3), 13: (4, 2), 14: (5, 3),
        15: (6, 4), 16: (1, 1), 17: (3, 1), 18: (5, 1), 19: (6, 2),
        20: (7, 3), 21: (2, 8), 22: (4, 8), 23: (6, 6), 24: (7, 5),
        25: (0, 2), 26: (2, 2), 27: (7, 1), 28: (8, 2), 29: (0, 8),
        30: (1, 9), 31: (3, 9), 32: (5, 7), 33: (7, 7), 34: (8, 4),
        35: (0, 0), 36: (2, 0), 37: (4, 0), 38: (6, 0), 39: (8, 0),
        40: (8, 6), 41: (9, 3), 42: (9, 5), 43: (8, 8), 44: (9, 7),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (35, 25, 4), (35, 36, 4), (36, 16, 2), (36, 26, 3), (36, 37, 4),
        (25, 10, 2), (25, 16, 3), (16, 11, 2), (16, 17, 3), (26, 6, 2),
        (10, 0, 2), (10, 11, 2), (11, 5, 2), (11, 12, 3), (6, 7, 2),
        (0, 1, 3), (0, 5, 2), (0, 29, 4), (1, 2, 2), (1, 21, 4),
        (5, 6, 2), (7, 8, 2), (7, 12, 2), (12, 13, 2), (12, 17, 3),
        (2, 3, 3), (2, 7, 2), (13, 14, 3), (13, 18, 4), (17, 18, 2),
        (37, 18, 3), (18, 19, 2), (19, 20, 2), (19, 27, 4), (27, 28, 2),
        (8, 9, 2), (8, 14, 2), (14, 15, 3), (14, 19, 2), (9, 15, 2),
        (9, 23, 4), (15, 20, 2), (15, 23, 2), (20, 24, 2), (20, 28, 3),
        (3, 4, 2), (3, 22, 4), (4, 9, 2), (4, 32, 3), (23, 24, 2),
        (23, 32, 2), (24, 33, 2), (24, 34, 3), (32, 33, 3), (33, 40, 2),
        (21, 30, 3), (22, 31, 3), (29, 30, 2), (30, 31, 2), (28, 34, 2),
        (34, 41, 3), (40, 42, 2), (40, 43, 3), (41, 42, 2), (42, 44, 2),
        (38, 27, 4), (39, 28, 4), (43, 44, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 35, 43

def generate_nuclear_reactor_graph():
    """Gera o grafo do reator nuclear - Difícil"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 5), 1: (1, 6), 2: (2, 5), 3: (3, 6), 4: (4, 5),
        5: (1, 4), 6: (2, 3), 7: (3, 4), 8: (4, 3), 9: (5, 4),
        10: (0, 3), 11: (1, 2), 12: (3, 2), 13: (4, 1), 14: (5, 2),
        15: (6, 3), 16: (1, 0), 17: (3, 0), 18: (5, 0), 19: (6, 1),
        20: (7, 2), 21: (2, 7), 22: (4, 7), 23: (6, 5), 24: (7, 4),
        25: (0, 1), 26: (2, 1), 27: (7, 0), 28: (8, 1), 29: (0, 7),
        30: (1, 8), 31: (3, 8), 32: (5, 6), 33: (7, 6), 34: (8, 3),
        35: (8, 5), 36: (0, 9), 37: (2, 9), 38: (4, 9), 39: (6, 7),
        40: (8, 7), 41: (9, 2), 42: (9, 4), 43: (9, 6), 44: (8, 9),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (25, 10, 3), (25, 16, 4), (16, 11, 2), (16, 26, 3), (16, 17, 4),
        (10, 0, 2), (10, 11, 2), (11, 5, 2), (11, 12, 3), (26, 6, 2),
        (0, 1, 3), (0, 5, 2), (0, 29, 4), (1, 2, 2), (1, 21, 4),
        (5, 6, 2), (6, 7, 2), (6, 12, 3), (2, 3, 3), (2, 7, 2),
        (7, 8, 2), (7, 12, 2), (12, 13, 2), (12, 17, 3), (13, 14, 3),
        (13, 18, 4), (17, 18, 2), (18, 19, 2), (19, 20, 2), (19, 27, 4),
        (27, 28, 2), (28, 34, 3), (8, 9, 2), (8, 14, 2), (14, 15, 3),
        (14, 19, 2), (9, 15, 2), (9, 23, 4), (15, 20, 2), (15, 23, 2),
        (20, 24, 2), (20, 41, 4), (34, 41, 2), (41, 42, 2), (24, 33, 2),
        (24, 34, 3), (3, 4, 2), (3, 22, 4), (4, 9, 2), (4, 32, 3),
        (23, 32, 2), (32, 33, 3), (33, 35, 2), (33, 39, 2), (35, 40, 2),
        (35, 42, 3), (21, 30, 3), (22, 31, 3), (29, 30, 2), (29, 36, 4),
        (30, 31, 2), (30, 37, 3), (31, 37, 2), (31, 38, 3), (39, 40, 2),
        (39, 43, 3), (40, 43, 2), (40, 44, 4), (42, 43, 2), (36, 37, 2),
        (37, 38, 2), (38, 44, 4), (43, 44, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 25, 44

def generate_time_storm_graph():
    """Gera o grafo da tempestade temporal - Difícil"""
    G = nx.Graph()
    
    nodes = {
        0: (0, 6), 1: (1, 7), 2: (2, 6), 3: (3, 7), 4: (4, 6),
        5: (1, 5), 6: (2, 4), 7: (3, 5), 8: (4, 4), 9: (5, 5),
        10: (0, 4), 11: (1, 3), 12: (3, 3), 13: (4, 2), 14: (5, 3),
        15: (6, 4), 16: (1, 1), 17: (3, 1), 18: (5, 1), 19: (6, 2),
        20: (7, 3), 21: (2, 8), 22: (4, 8), 23: (6, 6), 24: (7, 5),
        25: (0, 2), 26: (2, 2), 27: (7, 1), 28: (8, 2), 29: (0, 8),
        30: (1, 9), 31: (3, 9), 32: (5, 7), 33: (7, 7), 34: (8, 4),
        35: (0, 0), 36: (2, 0), 37: (4, 0), 38: (6, 0), 39: (8, 0),
        40: (8, 6), 41: (9, 3), 42: (9, 5), 43: (9, 7), 44: (8, 8),
        45: (0, 10), 46: (2, 10), 47: (4, 10), 48: (6, 8), 49: (8, 10),
    }
    
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, name=f"Nó {node}")
    
    edges = [
        (35, 25, 4), (35, 36, 4), (36, 16, 2), (36, 26, 3), (36, 37, 4),
        (25, 10, 2), (25, 16, 3), (16, 11, 2), (16, 17, 3), (26, 6, 2),
        (10, 0, 2), (10, 11, 2), (11, 5, 2), (11, 12, 3), (6, 7, 2),
        (0, 1, 3), (0, 5, 2), (0, 29, 4), (1, 2, 2), (1, 21, 4),
        (5, 6, 2), (7, 8, 2), (7, 12, 2), (12, 13, 2), (12, 17, 3),
        (2, 3, 3), (2, 7, 2), (13, 14, 3), (13, 18, 4), (17, 18, 2),
        (37, 18, 3), (18, 19, 2), (19, 20, 2), (19, 27, 4), (27, 28, 2),
        (39, 28, 4), (8, 9, 2), (8, 14, 2), (14, 15, 3), (14, 19, 2),
        (9, 15, 2), (9, 23, 4), (15, 20, 2), (15, 23, 2), (20, 24, 2),
        (20, 28, 3), (3, 4, 2), (3, 22, 4), (4, 9, 2), (4, 32, 3),
        (23, 24, 2), (23, 32, 2), (24, 33, 2), (24, 34, 3), (32, 33, 3),
        (33, 40, 2), (21, 30, 3), (22, 31, 3), (22, 47, 4), (29, 30, 2),
        (29, 45, 4), (30, 31, 2), (30, 46, 3), (28, 34, 2), (34, 41, 3),
        (40, 42, 2), (40, 44, 3), (40, 48, 2), (41, 42, 2), (42, 43, 2),
        (44, 49, 4), (31, 46, 2), (31, 47, 2), (43, 48, 2), (45, 46, 2),
        (46, 47, 2), (47, 49, 3), (48, 49, 2),
    ]
    
    for start, end, weight in edges:
        G.add_edge(start, end, weight=weight)
    
    return G, 35, 49
