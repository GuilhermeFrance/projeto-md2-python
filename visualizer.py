"""
Módulo de visualização do grafo e interface do jogo usando Pygame
"""
import pygame
import math
from collections import defaultdict

class Visualizer:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("🧙 PathFinder Adventure")
        
        # Cores
        self.BG_COLOR = (15, 15, 35)
        self.EDGE_COLOR = (100, 120, 180)
        self.NODE_COLOR = (100, 200, 255)
        self.NODE_HIGHLIGHT = (255, 200, 100)
        self.PATH_COLOR = (200, 255, 100)
        self.TEXT_COLOR = (255, 255, 255)
        self.PLAYER_COLOR = (255, 100, 100)
        self.EXIT_COLOR = (100, 255, 100)
        
        # Fontes
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)
        
    def draw_graph(self, world, player, clicked_nodes=None):
        """Desenha o grafo na tela"""
        self.screen.fill(self.BG_COLOR)
        
        if clicked_nodes is None:
            clicked_nodes = set()
        
        # Calcula posições dos nós (escala para caber na tela)
        node_positions = self._calculate_node_positions(world.graph)
        
        # Desenha arestas
        for start, end, data in world.graph.edges(data=True):
            start_pos = node_positions[start]
            end_pos = node_positions[end]
            weight = data.get('weight', 1)
            
            pygame.draw.line(self.screen, self.EDGE_COLOR, start_pos, end_pos, 2)
            
            # Desenha o peso da aresta
            mid_x = (start_pos[0] + end_pos[0]) / 2
            mid_y = (start_pos[1] + end_pos[1]) / 2
            weight_text = self.font_small.render(str(weight), True, self.TEXT_COLOR)
            self.screen.blit(weight_text, (mid_x - 10, mid_y - 10))
        
        # Desenha o caminho do jogador
        if len(player.path_taken) > 1:
            for i in range(len(player.path_taken) - 1):
                start = player.path_taken[i]
                end = player.path_taken[i + 1]
                start_pos = node_positions[start]
                end_pos = node_positions[end]
                pygame.draw.line(self.screen, self.PATH_COLOR, start_pos, end_pos, 3)
        
        # Desenha nós
        for node in world.graph.nodes():
            pos = node_positions[node]
            
            # Determina cor do nó
            if node == world.end_node:
                color = self.EXIT_COLOR
                radius = 20
            elif node == player.current_node:
                color = self.PLAYER_COLOR
                radius = 18
            elif node in clicked_nodes:
                color = self.NODE_HIGHLIGHT
                radius = 16
            else:
                color = self.NODE_COLOR
                radius = 14
            
            pygame.draw.circle(self.screen, color, pos, radius)
            pygame.draw.circle(self.screen, self.TEXT_COLOR, pos, radius, 2)
            
            # Desenha número do nó
            node_text = self.font_small.render(str(node), True, self.BG_COLOR)
            text_rect = node_text.get_rect(center=pos)
            self.screen.blit(node_text, text_rect)
        
        # Desenha UI (HUD)
        self._draw_hud(world, player)
        
        pygame.display.flip()
    
    def draw_menu(self, levels_completed=0):
        """Desenha o menu principal"""
        self.screen.fill(self.BG_COLOR)
        
        # Título
        title = self.font_large.render("🧙 PathFinder Adventure", True, (100, 200, 255))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_medium.render(
            "Navegue grafos, resolva puzzles, desbloqueie mundos!",
            True, self.TEXT_COLOR
        )
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 180))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        menu_items = [
            "1. Começar Novo Jogo (Nível 1)",
            "2. Ver Estatísticas",
            "3. Sair",
            "",
            f"Mundos Desbloqueados: {min(4, levels_completed + 1)}/4"
        ]
        
        y = 280
        for item in menu_items:
            text = self.font_small.render(item, True, self.TEXT_COLOR)
            self.screen.blit(text, (100, y))
            y += 50
        
        pygame.display.flip()
    
    def draw_level_complete(self, results):
        """Desenha a tela de nível completo"""
        self.screen.fill(self.BG_COLOR)
        
        # Título
        title = self.font_large.render("🎉 Nível Completo!", True, (100, 255, 100))
        title_rect = title.get_rect(center=(self.width // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Informações
        y = 150
        info_lines = [
            f"Mundo: {results['level_name']}",
            f"",
            f"Tempo: {results['time_taken']:.1f}s / {results['time_limit']}s",
            f"Distância: {results['player_distance']} / {results['optimal_distance']} (ótimo)",
            f"Eficiência: {results['efficiency']*100:.1f}%",
            f"",
            f"Pontuação Base: {results['base_score']}",
            f"Bônus Tempo: {results['time_bonus']}",
            f"Pontuação Total: {results['total_score']}",
            f"XP Ganho: +{results['xp_gained']}",
            f"",
            f"Pressione ESPAÇO para continuar..."
        ]
        
        for line in info_lines:
            text = self.font_medium.render(line, True, self.TEXT_COLOR)
            self.screen.blit(text, (100, y))
            y += 50
        
        pygame.display.flip()
    
    def _calculate_node_positions(self, graph, center_x=None, center_y=None, radius=None):
        """Calcula posições dos nós na tela"""
        if center_x is None:
            center_x = self.width // 2
        if center_y is None:
            center_y = self.height // 2
        if radius is None:
            radius = min(self.width, self.height) // 3
        
        # Se o grafo tem posições pré-calculadas, usa essas
        node_positions = {}
        if all('pos' in graph.nodes[node] for node in graph.nodes()):
            # Encontra os limites
            positions = [graph.nodes[node]['pos'] for node in graph.nodes()]
            min_x = min(p[0] for p in positions)
            max_x = max(p[0] for p in positions)
            min_y = min(p[1] for p in positions)
            max_y = max(p[1] for p in positions)
            
            # Normaliza e escala
            for node in graph.nodes():
                x, y = graph.nodes[node]['pos']
                norm_x = (x - min_x) / (max_x - min_x) if max_x != min_x else 0.5
                norm_y = (y - min_y) / (max_y - min_y) if max_y != min_y else 0.5
                
                pixel_x = center_x - radius + norm_x * radius * 2
                pixel_y = center_y - radius + norm_y * radius * 2
                node_positions[node] = (pixel_x, pixel_y)
        else:
            # Posiciona em círculo
            num_nodes = graph.number_of_nodes()
            for i, node in enumerate(graph.nodes()):
                angle = 2 * math.pi * i / num_nodes
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                node_positions[node] = (x, y)
        
        return node_positions
    
    def _draw_hud(self, world, player):
        """Desenha a interface do usuário (HUD)"""
        # Painel do jogador (canto superior esquerdo)
        hud_x, hud_y = 10, 10
        
        hud_texts = [
            f"🧙 {player.name}",
            f"❤️  {player.health}/{player.max_health}",
            f"💎 Pontos: {player.points}",
            f"⭐ XP: {player.experience}%",
            f"🏆 Nível: {player.level}",
        ]
        
        for text in hud_texts:
            surface = self.font_small.render(text, True, self.TEXT_COLOR)
            self.screen.blit(surface, (hud_x, hud_y))
            hud_y += 28
        
        # Painel do mundo (canto superior direito)
        world_x = self.width - 350
        world_y = 10
        
        world_texts = [
            f"📍 Mundo: {world.config['name']}",
            f"📊 Nós: {world.graph.number_of_nodes()}",
            f"🔗 Arestas: {world.graph.number_of_edges()}",
            f"🎯 Objetivo: Sair do mundo (Nó {world.end_node})",
        ]
        
        for text in world_texts:
            surface = self.font_small.render(text, True, self.TEXT_COLOR)
            self.screen.blit(surface, (world_x, world_y))
            world_y += 28
        
        # Instruções (parte inferior)
        instructions = [
            "Clique nos nós para se mover | ESC para sair | ESPAÇO para mostrar caminho ótimo"
        ]
        
        for text in instructions:
            surface = self.font_small.render(text, True, (200, 200, 200))
            self.screen.blit(surface, (10, self.height - 30))
