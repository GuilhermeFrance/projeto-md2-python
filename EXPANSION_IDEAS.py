"""
EXEMPLOS DE EXPANSÃO - PathFinder Adventure

Este arquivo contém ideias e exemplos de como expandir o jogo
com novas features e funcionalidades!
"""

# ============================================================================
# 1. ADICIONAR INIMIGOS AO JOGO
# ============================================================================

"""
from dataclasses import dataclass

@dataclass
class Enemy:
    node: int
    speed: float  # frames até próximo movimento
    
    def move(self, graph):
        # Move aleatoriamente pelos nós vizinhos
        import random
        neighbors = list(graph.neighbors(self.node))
        self.node = random.choice(neighbors)

class GameWithEnemies(Game):
    def __init__(self):
        super().__init__()
        self.enemies = []
    
    def start_level(self, level_id):
        super().start_level(level_id)
        # Cria inimigos
        num_enemies = level_id  # Aumenta com dificuldade
        for i in range(num_enemies):
            import random
            random_node = random.choice(list(self.world.graph.nodes()))
            self.enemies.append(Enemy(random_node, speed=0.5))
    
    def check_enemy_collision(self):
        for enemy in self.enemies:
            if enemy.node == self.player.current_node:
                self.player.take_damage(10)
                if self.player.health <= 0:
                    self.game_state = "game_over"
    
    def update(self):
        super().update()
        for enemy in self.enemies:
            enemy.move(self.world.graph)
        self.check_enemy_collision()
"""

# ============================================================================
# 2. ADICIONAR POWER-UPS
# ============================================================================

"""
from enum import Enum

class PowerUpType(Enum):
    SPEED_BOOST = "⚡"  # Mostra caminho ótimo
    HEAL = "❤️"  # Recupera vida
    SHIELD = "🛡️"  # Proteção contra inimigos
    DOUBLE_XP = "⭐⭐"  # Dobra XP ganho

class PowerUp:
    def __init__(self, node, power_type):
        self.node = node
        self.type = power_type
        self.collected = False
    
    def apply(self, player):
        if self.type == PowerUpType.HEAL:
            player.heal(50)
        elif self.type == PowerUpType.DOUBLE_XP:
            # Aplicar em level_complete
            pass

def add_powerups_to_level(world, num_powerups=3):
    import random
    powerups = []
    for _ in range(num_powerups):
        node = random.choice(list(world.graph.nodes()))
        ptype = random.choice(list(PowerUpType))
        powerups.append(PowerUp(node, ptype))
    return powerups
"""

# ============================================================================
# 3. SISTEMA DE SAVE/LOAD
# ============================================================================

"""
import json
import os

def save_game(player, filename="savegame.json"):
    data = {
        "player": {
            "name": player.name,
            "level": player.level,
            "experience": player.experience,
            "points": player.points,
            "health": player.health,
            "max_health": player.max_health,
            "items": player.items,
        },
        "best_times": player.best_times,
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Jogo salvo em {filename}")

def load_game(filename="savegame.json"):
    if not os.path.exists(filename):
        print(f"❌ Arquivo de save não encontrado: {filename}")
        return None
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    player = Player(data["player"]["name"])
    player.level = data["player"]["level"]
    player.experience = data["player"]["experience"]
    player.points = data["player"]["points"]
    player.health = data["player"]["health"]
    player.max_health = data["player"]["max_health"]
    player.items = data["player"]["items"]
    player.best_times = data["best_times"]
    
    print(f"✅ Jogo carregado de {filename}")
    return player
"""

# ============================================================================
# 4. ADICIONAR SONS E MÚSICA
# ============================================================================

"""
import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = None
    
    def load_sound(self, name, filepath):
        try:
            self.sounds[name] = pygame.mixer.Sound(filepath)
        except:
            print(f"⚠️ Som não encontrado: {filepath}")
    
    def load_music(self, filepath):
        try:
            pygame.mixer.music.load(filepath)
        except:
            print(f"⚠️ Música não encontrada: {filepath}")
    
    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
    
    def play_music(self, loop=True):
        if self.music:
            pygame.mixer.music.play(-1 if loop else 0)
    
    def stop_music(self):
        pygame.mixer.music.stop()

# No main.py:
audio = AudioManager()
audio.load_music("assets/music/castle_theme.mp3")
audio.load_sound("move", "assets/sounds/move.wav")
audio.load_sound("complete", "assets/sounds/level_complete.wav")
"""

# ============================================================================
# 5. ADICIONAR DIFERENTES ALGORITMOS DE IA
# ============================================================================

"""
from enum import Enum

class AIAlgorithm(Enum):
    DIJKSTRA = "dijkstra"
    BFS = "bfs"
    DFS = "dfs"
    A_STAR = "a_star"

def get_algorithm_description(algo):
    descriptions = {
        AIAlgorithm.DIJKSTRA: "Encontra garantidamente o caminho ótimo em grafos ponderados",
        AIAlgorithm.BFS: "Encontra o caminho com menor número de arestas",
        AIAlgorithm.DFS: "Explora profundamente, útil em labirintos",
        AIAlgorithm.A_STAR: "Mais rápido que Dijkstra usando heurísticas",
    }
    return descriptions.get(algo, "Algoritmo desconhecido")

# Adicionar modo de aprendizado onde você escolhe algoritmos
class LearningMode:
    def __init__(self):
        self.algorithms = [AIAlgorithm.DIJKSTRA, AIAlgorithm.BFS, AIAlgorithm.DFS]
    
    def run_learning_level(self, algorithm):
        # Mostra o grafo
        # Pede ao jogador para resolver
        # Depois mostra como cada algoritmo resolveria
        pass
"""

# ============================================================================
# 6. SISTEMA DE ACHIEVEMENTS/TROFÉUS
# ============================================================================

"""
from dataclasses import dataclass

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    icon: str
    condition: callable

class AchievementManager:
    def __init__(self):
        self.achievements = [
            Achievement(
                "first_win",
                "Primeira Vitória",
                "Complete o primeiro nível",
                "🏆",
                lambda p: p.level >= 1
            ),
            Achievement(
                "perfect_score",
                "Perfeição",
                "Complete um nível com 100% de eficiência",
                "⭐",
                lambda p: False  # Verificar nos resultados
            ),
            Achievement(
                "speed_runner",
                "Corredor Veloz",
                "Complete qualquer nível em menos de 30 segundos",
                "⚡",
                lambda p: False  # Verificar nos resultados
            ),
            Achievement(
                "explorer",
                "Explorador",
                "Desbloqueie todos os 4 mundos",
                "🗺️",
                lambda p: p.level >= 4
            ),
        ]
        self.unlocked = set()
    
    def check_achievements(self, player, level_results):
        for achievement in self.achievements:
            if achievement.id not in self.unlocked:
                if achievement.condition(player):
                    self.unlock(achievement)
    
    def unlock(self, achievement):
        self.unlocked.add(achievement.id)
        print(f"🏆 TROFÉU DESBLOQUEADO: {achievement.name}")
        print(f"   {achievement.description}")
"""

# ============================================================================
# 7. ADICIONAR CUSTOMIZAÇÃO DE PERSONAGEM
# ============================================================================

"""
class CustomPlayer(Player):
    def __init__(self, name, color, icon):
        super().__init__(name)
        self.color = color  # RGB tuple
        self.icon = icon    # Emoji ou sprite
    
    def get_display_name(self):
        return f"{self.icon} {self.name}"

# Exemplo de uso:
player = CustomPlayer(
    name="Mago",
    color=(150, 100, 255),
    icon="🧙"
)
"""

# ============================================================================
# 8. MODO MULTIPLAYER LOCAL
# ============================================================================

"""
class MultiplayerGame(Game):
    def __init__(self, players_count=2):
        super().__init__()
        self.players = [Player(f"Jogador {i+1}") for i in range(players_count)]
        self.current_player_idx = 0
    
    @property
    def current_player(self):
        return self.players[self.current_player_idx]
    
    def next_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
    
    def complete_level(self):
        super().complete_level()
        # Salva resultado do jogador
        self.next_player()
        self.start_level(self.current_level)
    
    def show_leaderboard(self):
        sorted_players = sorted(self.players, key=lambda p: p.points, reverse=True)
        print("\n🏆 PLACAR")
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player.name}: {player.points} pontos")
"""

# ============================================================================
# 9. GERAR GRAFOS ALEATÓRIOS
# ============================================================================

"""
import networkx as nx
import random

def generate_random_graph(num_nodes, edge_probability=0.3, weighted=True):
    '''Gera um grafo aleatório usando modelo de Erdős-Rényi'''
    G = nx.erdos_renyi_graph(num_nodes, edge_probability)
    
    if weighted:
        for edge in G.edges():
            G[edge[0]][edge[1]]['weight'] = random.randint(1, 10)
    
    return G

def generate_sparse_graph(num_nodes):
    '''Gera um grafo esparso (poucos edges)'''
    return generate_random_graph(num_nodes, edge_probability=0.2)

def generate_dense_graph(num_nodes):
    '''Gera um grafo denso (muitos edges)'''
    return generate_random_graph(num_nodes, edge_probability=0.6)

def generate_tree(num_nodes):
    '''Gera uma árvore (sem ciclos)'''
    return nx.random_tree(num_nodes)

def generate_bipartite_graph(n1, n2):
    '''Gera um grafo bipartido (útil para emparelhamento)'''
    return nx.complete_bipartite_graph(n1, n2)
"""

# ============================================================================
# 10. ANÁLISE DE GRAFOS E ESTATÍSTICAS
# ============================================================================

"""
def analyze_graph(graph):
    '''Retorna estatísticas sobre o grafo'''
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": nx.density(graph),
        "average_degree": sum(dict(graph.degree()).values()) / graph.number_of_nodes(),
        "is_connected": nx.is_connected(graph),
        "diameter": nx.diameter(graph) if nx.is_connected(graph) else None,
        "avg_shortest_path": nx.average_shortest_path_length(graph) if nx.is_connected(graph) else None,
    }

def print_graph_analysis(graph):
    analysis = analyze_graph(graph)
    print("\n📊 ANÁLISE DO GRAFO:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
"""

# ============================================================================
# COMO ADICIONAR ESSAS FEATURES:
# ============================================================================

"""
1. INIMIGOS:
   - Importar Enemy class no main.py
   - Criar lista de inimigos em start_level
   - Atualizar posição em update()
   - Desenhar no visualizer
   - Verificar colisão com jogador

2. POWER-UPS:
   - Adicionar à visualização
   - Detectar coleta ao mover
   - Aplicar efeito
   - Desenhar ícone

3. SAVE/LOAD:
   - Adicionar botão no menu
   - Chamar save_game()
   - Chamar load_game()
   - Restaurar estado do jogador

4. SONS:
   - Criar pasta assets/sounds/
   - Importar AudioManager
   - Chamar ao jogar, ganhar, etc

5. ACHIEVEMENTS:
   - Instanciar AchievementManager no Game
   - Verificar ao completar níveis
   - Exibir notificação ao desbloquear

6. CUSTOMIZAÇÃO:
   - Tela de customização no menu
   - Salvar configurações
   - Usar na visualização

7. MULTIPLAYER:
   - Estender Game para MultiplayerGame
   - Adicionar tela de placar
   - Turn-based ou simultâneo

8. GRAFOS ALEATÓRIOS:
   - Substituir generators fixos
   - Usar em um modo "Infinito"
   - Aumentar dificuldade dinamicamente

9. ANÁLISE:
   - Adicionar à educação
   - Mostrar estatísticas entre rounds
   - Ensinar propriedades

10. LEADERBOARD:
    - Salvar melhores tempos
    - Ranking global (com API)
    - Badges e distinções
"""

print("✨ Veja os exemplos acima para ideias de expansão!")
