"""
PathFinder Adventure - Jogo de Grafos e Matemática Discreta
Um jogo educativo que ensina conceitos de teoria dos grafos de forma divertida!
"""
import pygame
import sys
from player import Player
from world import World
from visualizer import Visualizer
from pathfinding import dijkstra, calculate_path_efficiency
import time

class Game:
    def __init__(self):
        pygame.init()
        self.visualizer = Visualizer()
        self.player = Player("Explorador")
        self.current_level = 1
        self.world = None
        self.game_state = "menu"  # menu, playing, level_complete, game_over
        self.show_optimal_path = False
        self.clicked_nodes = set()
        
    def handle_events(self):
        """Gerencia os eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "menu"
                        self.clicked_nodes = set()
                    else:
                        return False
                
                # Menu
                if self.game_state == "menu":
                    if event.key == pygame.K_1:
                        self.start_level(1)
                    elif event.key == pygame.K_2:
                        self.show_stats()
                    elif event.key == pygame.K_3:
                        return False
                
                # Durante o jogo
                if self.game_state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.show_optimal_path = not self.show_optimal_path
                
                # Level completo
                if self.game_state == "level_complete":
                    if event.key == pygame.K_SPACE:
                        # Vai para o próximo nível ou menu
                        if self.current_level < 4:
                            self.start_level(self.current_level + 1)
                        else:
                            self.game_state = "menu"
            
            # Clique do mouse durante o jogo
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "playing":
                pos = pygame.mouse.get_pos()
                clicked_node = self.get_clicked_node(pos)
                if clicked_node is not None:
                    self.handle_node_click(clicked_node)
        
        return True
    
    def get_clicked_node(self, pos):
        """Verifica qual nó foi clicado"""
        # Recalcula posições (mesmo código do visualizer)
        node_positions = self.visualizer._calculate_node_positions(self.world.graph)
        
        for node, node_pos in node_positions.items():
            distance = ((pos[0] - node_pos[0])**2 + (pos[1] - node_pos[1])**2)**0.5
            if distance < 20:  # Raio de clique
                return node
        
        return None
    
    def handle_node_click(self, node):
        """Gerencia o clique em um nó"""
        current = self.player.current_node
        
        # Verifica se o nó é vizinho
        if node in self.world.graph.neighbors(current):
            self.player.move_to_node(node)
            self.clicked_nodes.add(node)
            
            # Verifica se chegou no final
            if node == self.world.end_node:
                self.complete_level()
        else:
            print(f"❌ O nó {node} não é vizinho de {current}!")
    
    def start_level(self, level_id):
        """Inicia um novo nível"""
        self.current_level = level_id
        self.world = World(level_id)
        self.player.reset_level(self.world.start_node)
        self.world.start_level()
        self.game_state = "playing"
        self.show_optimal_path = False
        self.clicked_nodes = set()
    
    def complete_level(self):
        """Completa o nível atual"""
        results = self.world.complete_level(self.player.path_taken)
        
        # Adiciona pontos e XP ao jogador
        self.player.add_points(results["total_score"])
        self.player.add_experience(results["xp_gained"])
        
        self.level_results = results
        self.game_state = "level_complete"
    
    def show_stats(self):
        """Mostra as estatísticas do jogador"""
        print("\n" + "="*50)
        print("📊 ESTATÍSTICAS DO JOGADOR")
        print("="*50)
        stats = self.player.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print("="*50 + "\n")
        input("Pressione ENTER para voltar ao menu...")
    
    def update(self):
        """Atualiza o estado do jogo"""
        pass
    
    def draw(self):
        """Desenha o estado atual"""
        if self.game_state == "menu":
            levels_completed = self.current_level - 1
            self.visualizer.draw_menu(levels_completed)
        
        elif self.game_state == "playing":
            self.visualizer.draw_graph(self.world, self.player, self.clicked_nodes)
            
            # Se apertar espaço, mostra o caminho ótimo
            if self.show_optimal_path:
                # Desenha o caminho ótimo em cor diferente
                node_positions = self.visualizer._calculate_node_positions(self.world.graph)
                import pygame
                for i in range(len(self.world.optimal_path) - 1):
                    start = self.world.optimal_path[i]
                    end = self.world.optimal_path[i + 1]
                    start_pos = node_positions[start]
                    end_pos = node_positions[end]
                    pygame.draw.line(
                        self.visualizer.screen,
                        (0, 255, 200),  # Cyan para o caminho ótimo
                        start_pos,
                        end_pos,
                        4
                    )
                pygame.display.flip()
        
        elif self.game_state == "level_complete":
            self.visualizer.draw_level_complete(self.level_results)
    
    def run(self):
        """Loop principal do jogo"""
        clock = pygame.time.Clock()
        running = True
        
        print("""
        ╔════════════════════════════════════════╗
        ║   🧙 PathFinder Adventure 🧙          ║
        ║  Jogo de Grafos e Matemática Discreta ║
        ╚════════════════════════════════════════╝
        """)
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        print("\n👋 Obrigado por jogar PathFinder Adventure!\n")
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
