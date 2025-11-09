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
        efficiency = calculate_path_efficiency(path_length, len(self.optimal_path) - 1)
        
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
