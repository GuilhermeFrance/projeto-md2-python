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
        self.level_stars = {}  # {level_id: stars_earned}
        self.lives = 3  # Sistema de vidas
        self.max_lives = 3
        
    def move_to_node(self, node):
        """Move o personagem para um nó"""
        old_node = self.current_node
        self.current_node = node
        # Só adiciona se não for o mesmo nó que já está no final do caminho
        if len(self.path_taken) == 0 or self.path_taken[-1] != node:
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
    
    def calculate_stars(self, efficiency):
        """Calcula quantas estrelas o jogador ganhou baseado na eficiência"""
        # Converte eficiência de 0-1 para 0-100
        efficiency_percent = efficiency * 100
        
        if efficiency_percent >= 95:
            return 3  # Perfeito ou quase perfeito (95%+)
        elif efficiency_percent >= 80:
            return 2  # Muito bom (80%+)
        elif efficiency_percent >= 60:
            return 1  # Razoavel (60%+)
        else:
            return 0  # 0 estrelas (<60%)
    
    def update_level_stars(self, level_id, stars):
        """Atualiza as estrelas de um nível (mantém o melhor resultado)"""
        if level_id not in self.level_stars or stars > self.level_stars[level_id]:
            self.level_stars[level_id] = stars
    
    def get_level_stars(self, level_id):
        """Retorna quantas estrelas o jogador tem no nível"""
        return self.level_stars.get(level_id, 0)
    
    def can_advance_level(self, level_id):
        """Verifica se o jogador pode avançar de nível (precisa de pelo menos 2 estrelas)"""
        return self.get_level_stars(level_id) >= 2
    
    def lose_life(self):
        """Remove uma vida do jogador"""
        if self.lives > 0:
            self.lives -= 1
        return self.lives > 0
    
    def has_lives(self):
        """Verifica se o jogador ainda tem vidas"""
        return self.lives > 0
    
    def reset_lives(self):
        """Reseta as vidas para o máximo"""
        self.lives = self.max_lives
