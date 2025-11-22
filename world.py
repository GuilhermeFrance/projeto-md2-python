"""
Módulo que gerencia o mundo e os níveis do jogo
"""
from graph_generator import get_level_config
from pathfinding import dijkstra, calculate_path_efficiency
import time

class World:
    def __init__(self, level_id=1):
        self.level_id = level_id
        self.config = get_level_config(level_id)
        
        # Gera o grafo do nível
        generator = self.config["generator"]
        self.graph, self.start_node, self.end_node = generator()
        
        # Encontra o caminho ótimo
        self.optimal_path, self.optimal_distance = dijkstra(
            self.graph, self.start_node, self.end_node
        )
        
        # Gerar inimigos a partir do nível médio (nível 4+)
        self.enemies = set()
        if level_id >= 4:
            self._generate_enemies()
        
        self.start_time = None
        self.end_time = None
        self.completed = False
        
    def start_level(self):
        """Inicia o nível"""
        self.start_time = time.time()
        
    def complete_level(self, player_path):
        """Marca o nível como completo e calcula a pontuação"""
        self.end_time = time.time()
        self.completed = True
        
        elapsed_time = self.end_time - self.start_time
        path_length = len(player_path) - 1  # Número de arestas
        
        # Calcula a eficiência
        optimal_length = len(self.optimal_path) - 1
        efficiency = calculate_path_efficiency(path_length, optimal_length)
        
        # Calcula a pontuação base (0-100)
        base_score = int(efficiency * 100)
        
        # Bônus por tempo
        time_limit = self.config["time_limit"]
        time_bonus = max(0, int((time_limit - elapsed_time) / time_limit * 50))
        
        total_score = base_score + time_bonus
        
        return {
            "level_id": self.level_id,
            "level_name": self.config["name"],
            "time_taken": elapsed_time,
            "time_limit": time_limit,
            "player_distance": path_length,
            "optimal_distance": len(self.optimal_path) - 1,
            "efficiency": efficiency,
            "base_score": base_score,
            "time_bonus": time_bonus,
            "total_score": total_score,
            "xp_gained": int(efficiency * 50 + (time_bonus / 50) * 25),
        }
    
    def get_graph_info(self):
        """Retorna informações sobre o grafo"""
        return {
            "nodes": list(self.graph.nodes()),
            "edges": list(self.graph.edges(data=True)),
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
        }
    
    def _generate_enemies(self):
        """Gera inimigos em nós estratégicos"""
        import random
        
        # Obter todos os nós exceto início e fim
        all_nodes = list(self.graph.nodes())
        available_nodes = [n for n in all_nodes if n != self.start_node and n != self.end_node]
        
        if not available_nodes:
            return
            
        # Número de inimigos baseado no nível (mais inimigos em níveis avançados)
        if self.level_id < 8:  # Níveis médios (4-7)
            num_enemies = random.randint(1, 2)
        elif self.level_id < 15:  # Níveis difíceis (8-14)
            num_enemies = random.randint(2, 3)
        else:  # Níveis extremos (15+)
            num_enemies = random.randint(3, 4)
        
        # Limitar o número de inimigos ao número de nós disponíveis
        num_enemies = min(num_enemies, len(available_nodes))
        
        # Selecionar nós aleatórios para colocar inimigos
        enemy_nodes = random.sample(available_nodes, num_enemies)
        self.enemies = set(enemy_nodes)
        
        print(f"🧌 Inimigos gerados no nível {self.level_id}: {list(self.enemies)}")
    
    def has_enemy(self, node_id):
        """Verifica se um nó tem inimigo"""
        return node_id in self.enemies
    
    def remove_enemy(self, node_id):
        """Remove um inimigo de um nó (quando derrotado)"""
        if node_id in self.enemies:
            self.enemies.remove(node_id)
