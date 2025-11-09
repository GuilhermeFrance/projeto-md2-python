"""
Módulo do personagem do jogador
"""

class Player:
    def __init__(self, name="Explorador", starting_node=0):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.experience = 0
        self.level = 1
        self.points = 0
        self.current_node = starting_node
        self.path_taken = [starting_node]
        self.items = []
        self.best_times = {}  # {level_id: best_time}
        
    def move_to_node(self, node):
        """Move o personagem para um nó"""
        self.current_node = node
        self.path_taken.append(node)
        
    def add_experience(self, amount):
        """Adiciona experiência e faz level up se necessário"""
        self.experience += amount
        # A cada 100 XP, faz level up
        if self.experience >= 100:
            self.level += 1
            self.experience -= 100
            self.max_health += 10
            self.health = self.max_health
            
    def add_points(self, amount):
        """Adiciona pontos"""
        self.points += amount
        
    def take_damage(self, amount):
        """Recebe dano"""
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
    def heal(self, amount):
        """Recupera vida"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
            
    def add_item(self, item):
        """Adiciona um item ao inventário"""
        self.items.append(item)
        
    def get_stats(self):
        """Retorna as estatísticas do jogador"""
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "level": self.level,
            "experience": self.experience,
            "points": self.points,
            "items": len(self.items),
            "current_node": self.current_node
        }
    
    def reset_level(self, starting_node):
        """Reseta o estado para um novo nível"""
        self.current_node = starting_node
        self.path_taken = [starting_node]
        self.health = self.max_health
