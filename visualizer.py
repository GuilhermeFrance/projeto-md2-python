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
        
        # Cores (paleta ninja)
        self.BG_COLOR = (245, 203, 105)  # #f5cb69 - Dourado ninja
        self.BG_GRADIENT_TOP = (255, 220, 130)  # Gradiente superior mais claro
        self.BG_GRADIENT_BOTTOM = (235, 185, 80)  # Gradiente inferior mais escuro
        
        # Cores dos elementos do grafo - Paleta ninja coesa
        self.EDGE_COLOR = (60, 15, 30)  # Vinho escuro para arestas
        self.EDGE_HOVER_COLOR = (180, 40, 70)  # Hover vermelho ninja
        self.NODE_COLOR = (79, 5, 25)  # #4f0519 - Vinho escuro ninja
        self.NODE_BORDER_COLOR = (140, 25, 50)  # Borda vermelha ninja
        self.NODE_HIGHLIGHT = (200, 50, 80)  # Destaque vermelho brilhante
        self.PATH_COLOR = (220, 180, 60)  # Dourado para caminho (harmoniza com fundo)
        self.OPTIMAL_PATH_COLOR = (255, 215, 0)  # Ouro brilhante para caminho ótimo
        
        # Cores do jogador e elementos especiais - Ninja themed
        self.PLAYER_COLOR = (200, 50, 80)  # Vermelho ninja para jogador
        self.PLAYER_GLOW = (255, 100, 120)  # Brilho vermelho ninja
        self.EXIT_COLOR = (255, 215, 0)  # Ouro para saída (destaque especial)
        self.EXIT_GLOW = (255, 235, 50)  # Brilho dourado
        
        # Cores ninja especiais para efeitos
        self.NINJA_SHADOW = (20, 5, 10)  # Sombra ninja profunda
        self.NINJA_ACCENT = (180, 40, 70)  # Vermelho ninja de destaque
        self.NINJA_GOLD = (255, 215, 0)  # Ouro ninja
        self.NINJA_DARK = (40, 5, 15)  # Ninja escuro
        
        # Carregar background ninja
        self.load_background()
        
        # Carregar background de nível completo
        self.load_level_complete_background()
        
        # Carregar imagens de estrelas
        self.load_star_images()
        
        # Carregar imagens de inimigos
        self.load_enemy_images()
        
        # Sistema de som ninja
        self.load_ninja_sounds()
        
        # Carregar botões de imagem
        self.load_button_images()
        
        # Sistema de transições melhorado
        self.is_transitioning = False
        self.transition_alpha = 0
        self.transition_speed = 4  # Velocidade mais lenta para suavidade
        self.transition_callback = None
        self.fade_out_first = True
        self.transition_buffer = pygame.Surface((self.width, self.height))
        
        # Cores da interface - Design ninja elegante
        self.TEXT_COLOR = (255, 255, 255)  # Texto branco para contraste
        self.TEXT_SHADOW = (50, 10, 20)  # Sombra ninja escura
        self.PANEL_COLOR = (40, 5, 15)  # Painel ninja mais escuro
        self.PANEL_BORDER = (180, 40, 70)  # Borda vermelha ninja
        self.HEALTH_GREEN = (100, 200, 60)  # Verde ninja
        self.HEALTH_YELLOW = (255, 200, 40)  # Amarelo ninja
        self.HEALTH_RED = (220, 60, 80)  # Vermelho ninja
        
        # Animação
        self.animation_time = 0
        self.player_pulse = 0
        
        # Sistema de sprites para personagem
        self.idle_sprites = []
        self.run_sprites = []
        self.run_left_sprites = []  # Sprites para correr para a esquerda
        self.current_idle_frame = 0
        self.current_run_frame = 0
        self.current_run_left_frame = 0
        self.idle_animation_timer = 0
        self.run_animation_timer = 0
        self.run_left_animation_timer = 0
        self.idle_frame_duration = 0.15  # 150ms por frame
        self.run_frame_duration = 0.08   # 80ms por frame (mais rápido para corrida)
        self.use_sprites = True
        
        # Direção atual do movimento
        self.current_movement_direction = None
        
        # Carregar sprites de animação
        self.load_idle_sprites()
        self.load_run_sprites()
        self.load_run_left_sprites()
        
        # Sistema de sprites (removido o sistema antigo em favor do novo sistema de animação)
        
        # Fonts only for game UI (not menu)
        try:
            self.font_small = pygame.font.SysFont('Arial', 20, bold=True)
            self.font_medium = pygame.font.SysFont('Arial', 28, bold=True)
            self.font_large = pygame.font.SysFont('Arial', 42, bold=True)
            self.font_title = pygame.font.SysFont('Arial', 56, bold=True)
        except:
            self.font_small = pygame.font.Font(None, 24)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_large = pygame.font.Font(None, 48)
            self.font_title = pygame.font.Font(None, 64)
    
    def load_idle_sprites(self):
        """Carrega os sprites de animação idle (idle0.png até idle4.png)"""
        import os
        
        self.idle_sprites = []
        
        # Tenta carregar idle0.png até idle4.png
        for i in range(5):
            sprite_path = f"idle{i}.png"
            if os.path.exists(sprite_path):
                try:
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    # Redimensiona para tamanho adequado (40x40 pixels)
                    sprite = pygame.transform.scale(sprite, (120, 120))
                    self.idle_sprites.append(sprite)
                    print(f"✅ Sprite carregado: {sprite_path}")
                except pygame.error as e:
                    print(f"❌ Erro ao carregar {sprite_path}: {e}")
            else:
                print(f"⚠️ Arquivo não encontrado: {sprite_path}")
        
        if not self.idle_sprites:
            print("🎨 Nenhum sprite encontrado, usando desenho vetorial")
            self.use_sprites = False
        else:
            print(f"🎬 {len(self.idle_sprites)} sprites carregados para animação idle")
    
    def update_idle_animation(self):
        """Atualiza a animação idle do personagem"""
        if not self.idle_sprites:
            return
            
        import time
        current_time = time.time()
        
        if current_time - self.idle_animation_timer >= self.idle_frame_duration:
            self.current_idle_frame = (self.current_idle_frame + 1) % len(self.idle_sprites)
            self.idle_animation_timer = current_time
    
    def load_run_sprites(self):
        """Carrega os sprites de animação de corrida (run_0.png até run_5.png)"""
        import os
        import time
        
        self.run_sprites = []
        self.run_animation_timer = time.time()
        
        # Tenta carregar run_0.png até run_5.png
        for i in range(6):
            sprite_path = f"run_{i}.png"
            if os.path.exists(sprite_path):
                try:
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    # Redimensiona para tamanho adequado (120x120 pixels)
                    sprite = pygame.transform.scale(sprite, (120, 120))
                    self.run_sprites.append(sprite)
                    print(f"🏃 Sprite de corrida carregado: {sprite_path}")
                except pygame.error as e:
                    print(f"❌ Erro ao carregar {sprite_path}: {e}")
            else:
                print(f"⚠️ Arquivo não encontrado: {sprite_path}")
        
        if not self.run_sprites:
            print("⚠️ Nenhum sprite de corrida encontrado")
        else:
            print(f"🏃 {len(self.run_sprites)} sprites de corrida carregados!")
    
    def update_run_animation(self):
        """Atualiza a animação de corrida do personagem"""
        if not self.run_sprites:
            return
            
        import time
        current_time = time.time()
        
        if current_time - self.run_animation_timer >= self.run_frame_duration:
            self.current_run_frame = (self.current_run_frame + 1) % len(self.run_sprites)
            self.run_animation_timer = current_time
    
    def load_run_left_sprites(self):
        """Carrega os sprites de animação de corrida para a esquerda (runleft0.png até runleft5.png)"""
        import os
        import time
        
        self.run_left_sprites = []
        self.run_left_animation_timer = time.time()
        
        # Tenta carregar runleft0.png até runleft5.png
        for i in range(6):
            sprite_path = f"runleft{i}.png"
            if os.path.exists(sprite_path):
                try:
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    # Redimensiona para tamanho adequado (120x120 pixels)
                    sprite = pygame.transform.scale(sprite, (120, 120))
                    self.run_left_sprites.append(sprite)
                    print(f"🏃⬅️ Sprite de corrida esquerda carregado: {sprite_path}")
                except pygame.error as e:
                    print(f"❌ Erro ao carregar {sprite_path}: {e}")
            else:
                print(f"⚠️ Arquivo não encontrado: {sprite_path}")
        
        if not self.run_left_sprites:
            print("⚠️ Nenhum sprite de corrida esquerda encontrado")
        else:
            print(f"🏃⬅️ {len(self.run_left_sprites)} sprites de corrida esquerda carregados!")
    
    def update_run_left_animation(self):
        """Atualiza a animação de corrida para a esquerda do personagem"""
        if not self.run_left_sprites:
            return
            
        import time
        current_time = time.time()
        
        if current_time - self.run_left_animation_timer >= self.run_frame_duration:
            self.current_run_left_frame = (self.current_run_left_frame + 1) % len(self.run_left_sprites)
            self.run_left_animation_timer = current_time
        
    def draw_graph(self, world, player, clicked_nodes=None, show_optimal_path=False, hovered_node=None, animated_player_pos=None):
        """Desenha o grafo na tela com visual profissional"""
        # Atualiza animação
        self.animation_time += 0.1
        self.player_pulse = math.sin(self.animation_time * 3) * 0.3 + 1
        
        # Desenha background ninja
        self.draw_ninja_background()
        
        if clicked_nodes is None:
            clicked_nodes = set()
        
        # Calcula posições dos nós
        node_positions = self._calculate_node_positions(world.graph)
        
        # Desenha caminho ótimo se solicitado
        if show_optimal_path and hasattr(world, 'optimal_path'):
            self._draw_optimal_path(world.optimal_path, node_positions)
        
        # Desenha arestas com estilo profissional
        self._draw_edges(world.graph, node_positions)
        
        # Destaca conexões do nó hovered
        if hovered_node is not None:
            self._draw_hovered_connections(world.graph, node_positions, hovered_node)
        
        # Desenha o caminho do jogador
        self._draw_player_path(player.path_taken, node_positions)
        
        # Desenha nós com efeitos visuais
        self._draw_nodes(world, player, node_positions, clicked_nodes, hovered_node)
        
        # Desenha inimigos (se houver)
        self._draw_enemies(world, node_positions)
        
        # Desenha indicadores direcionais
        self._draw_directional_indicators(world, player, node_positions)
        
        # Desenha o personagem do jogador
        self._draw_player_character(player, node_positions, animated_player_pos)
        
        # Desenha UI (HUD) profissional
        self._draw_professional_hud(world, player)
        
        # Desenha efeitos de partículas
        self._draw_particle_effects(world, player, node_positions)
    
    def _draw_gradient_background(self):
        """Desenha um fundo com gradiente ninja refinado"""
        # Desenhar gradiente base
        for y in range(self.height):
            ratio = y / self.height
            # Suavizar transição com curva
            smooth_ratio = ratio * ratio * (3.0 - 2.0 * ratio)  # Smoothstep
            
            r = int(self.BG_GRADIENT_TOP[0] * (1 - smooth_ratio) + self.BG_GRADIENT_BOTTOM[0] * smooth_ratio)
            g = int(self.BG_GRADIENT_TOP[1] * (1 - smooth_ratio) + self.BG_GRADIENT_BOTTOM[1] * smooth_ratio)
            b = int(self.BG_GRADIENT_TOP[2] * (1 - smooth_ratio) + self.BG_GRADIENT_BOTTOM[2] * smooth_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
        
        # Adicionar textura ninja sutil
        self._add_ninja_texture()
    
    def _add_ninja_texture(self):
        """Adiciona uma textura ninja sutil ao fundo"""
        import random
        random.seed(42)  # Seed fixo para consistência
        
        # Adicionar pontos ninja sutis
        for _ in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            alpha = random.randint(8, 20)
            size = random.randint(1, 2)
            
            ninja_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            ninja_color = (*self.NINJA_SHADOW, alpha)
            pygame.draw.circle(ninja_surface, ninja_color, (size, size), size)
            self.screen.blit(ninja_surface, (x-size, y-size))
    
    def _draw_edges(self, graph, node_positions):
        """Desenha arestas com estilo profissional"""
        for start, end, data in graph.edges(data=True):
            start_pos = node_positions[start]
            end_pos = node_positions[end]
            weight = data.get('weight', 1)
            
            # Desenha sombra da aresta
            shadow_offset = 2
            pygame.draw.line(self.screen, (0, 0, 0, 50), 
                           (start_pos[0] + shadow_offset, start_pos[1] + shadow_offset),
                           (end_pos[0] + shadow_offset, end_pos[1] + shadow_offset), 3)
            
            # Desenha aresta principal
            pygame.draw.line(self.screen, self.EDGE_COLOR, start_pos, end_pos, 3)
            
            # Desenha o peso da aresta com fundo
            mid_x = (start_pos[0] + end_pos[0]) / 2
            mid_y = (start_pos[1] + end_pos[1]) / 2
            
            weight_text = self.font_small.render(str(weight), True, self.TEXT_COLOR)
            text_rect = weight_text.get_rect(center=(mid_x, mid_y))
            
            # Fundo do texto
            padding = 4
            bg_rect = text_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(self.screen, self.PANEL_COLOR, bg_rect)
            pygame.draw.rect(self.screen, self.PANEL_BORDER, bg_rect, 1)
            
            self.screen.blit(weight_text, text_rect)
    
    def _draw_player_path(self, path, node_positions):
        """Desenha o caminho percorrido pelo jogador"""
        if len(path) > 1:
            for i in range(len(path) - 1):
                start = path[i]
                end = path[i + 1]
                start_pos = node_positions[start]
                end_pos = node_positions[end]
                
                # Desenha linha mais grossa com brilho
                pygame.draw.line(self.screen, self.PATH_COLOR, start_pos, end_pos, 6)
                pygame.draw.line(self.screen, (200, 255, 200), start_pos, end_pos, 3)
    
    def _draw_optimal_path(self, optimal_path, node_positions):
        """Desenha o caminho ótimo"""
        if len(optimal_path) > 1:
            for i in range(len(optimal_path) - 1):
                start = optimal_path[i]
                end = optimal_path[i + 1]
                start_pos = node_positions[start]
                end_pos = node_positions[end]
                
                # Desenha linha pontilhada para o caminho ótimo
                self._draw_dashed_line(start_pos, end_pos, self.OPTIMAL_PATH_COLOR, 4)
    
    def _draw_dashed_line(self, start_pos, end_pos, color, width):
        """Desenha uma linha pontilhada"""
        distance = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
        dash_length = 10
        num_dashes = int(distance / (dash_length * 2))
        
        for i in range(num_dashes):
            t1 = (i * 2 * dash_length) / distance
            t2 = ((i * 2 + 1) * dash_length) / distance
            
            if t2 > 1:
                t2 = 1
            
            x1 = start_pos[0] + t1 * (end_pos[0] - start_pos[0])
            y1 = start_pos[1] + t1 * (end_pos[1] - start_pos[1])
            x2 = start_pos[0] + t2 * (end_pos[0] - start_pos[0])
            y2 = start_pos[1] + t2 * (end_pos[1] - start_pos[1])
            
            pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)
    
    def _draw_nodes(self, world, player, node_positions, clicked_nodes, hovered_node=None):
        """Desenha nós com efeitos visuais profissionais"""
        for node in world.graph.nodes():
            pos = node_positions[node]
            
            # Determina cor e tamanho do nó
            if node == world.end_node:
                # Nó de saída com efeito de brilho
                glow_radius = 35 + math.sin(self.animation_time * 4) * 5
                if node == hovered_node:
                    # Hover na saída - brilho extra
                    glow_radius += 10
                    self._draw_glow_circle(pos, glow_radius, self.EXIT_GLOW, 60)
                    
                    # Texto de hover para saída
                    exit_text = "🎯 SAÍDA - Clique para vencer!"
                    exit_surface = self.font_small.render(exit_text, True, self.TEXT_COLOR)
                    exit_rect = exit_surface.get_rect(center=(pos[0], pos[1] - 40))
                    
                    # Fundo para o texto
                    padding = 5
                    bg_rect = exit_rect.inflate(padding * 2, padding * 2)
                    bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(bg_surface, (*self.EXIT_COLOR, 150), (0, 0, bg_rect.width, bg_rect.height))
                    pygame.draw.rect(bg_surface, self.TEXT_COLOR, (0, 0, bg_rect.width, bg_rect.height), 2)
                    
                    self.screen.blit(bg_surface, bg_rect)
                    self.screen.blit(exit_surface, exit_rect)
                
                self._draw_glow_circle(pos, glow_radius, self.EXIT_GLOW, 30)
                pygame.draw.circle(self.screen, self.EXIT_COLOR, pos, 25)
                pygame.draw.circle(self.screen, self.TEXT_COLOR, pos, 25, 3)
                
                # Ícone de saída
                self._draw_exit_icon(pos)
                
            elif node == player.current_node:
                # Nó do jogador (será desenhado separadamente)
                continue
                
            elif node in clicked_nodes:
                # Nó visitado
                if node == hovered_node:
                    # Efeito de hover no nó visitado
                    self._draw_glow_circle(pos, 25, self.NODE_HIGHLIGHT, 50)
                pygame.draw.circle(self.screen, self.NODE_HIGHLIGHT, pos, 18)
                pygame.draw.circle(self.screen, self.TEXT_COLOR, pos, 18, 2)
            else:
                # Nó normal
                if node == hovered_node:
                    # Verifica se o nó é vizinho do jogador
                    is_neighbor = node in list(world.graph.neighbors(player.current_node))
                    
                    if is_neighbor:
                        # Nó alcançável - efeito de hover positivo
                        self._draw_glow_circle(pos, 28, self.EDGE_HOVER_COLOR, 60)
                        pygame.draw.circle(self.screen, self.EDGE_HOVER_COLOR, pos, 20)
                        pygame.draw.circle(self.screen, self.TEXT_COLOR, pos, 20, 3)
                        
                        # Calcula sugestão de tecla
                        suggested_keys = self._get_suggested_keys(world, player, node, node_positions)
                        hover_text = f"✓ Clique ou {suggested_keys}"
                        text_color = self.HEALTH_GREEN
                    else:
                        # Nó não alcançável - efeito de hover negativo
                        self._draw_glow_circle(pos, 28, self.HEALTH_RED, 60)
                        pygame.draw.circle(self.screen, (150, 50, 50), pos, 20)
                        pygame.draw.circle(self.screen, self.HEALTH_RED, pos, 20, 3)
                        
                        # Texto de aviso
                        hover_text = "✗ Não é vizinho"
                        text_color = self.HEALTH_RED
                    
                    hover_surface = self.font_small.render(hover_text, True, text_color)
                    hover_rect = hover_surface.get_rect(center=(pos[0], pos[1] - 35))
                    
                    # Fundo semi-transparente para o texto
                    padding = 5
                    bg_rect = hover_rect.inflate(padding * 2, padding * 2)
                    bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(bg_surface, (*self.PANEL_COLOR, 180), (0, 0, bg_rect.width, bg_rect.height))
                    pygame.draw.rect(bg_surface, self.PANEL_BORDER, (0, 0, bg_rect.width, bg_rect.height), 1)
                    
                    self.screen.blit(bg_surface, bg_rect)
                    self.screen.blit(hover_surface, hover_rect)
                else:
                    pygame.draw.circle(self.screen, self.NODE_COLOR, pos, 16)
                    pygame.draw.circle(self.screen, self.NODE_BORDER_COLOR, pos, 16, 2)
            
            # Desenha número do nó (exceto para o jogador)
            if node != player.current_node:
                node_text = self.font_small.render(str(node), True, self.TEXT_COLOR)
                text_rect = node_text.get_rect(center=pos)
                self.screen.blit(node_text, text_rect)
    
    def _draw_player_character(self, player, node_positions, animated_pos=None):
        """Desenha o personagem do jogador usando sprites ou desenho vetorial"""
        # Use posição animada se disponível, senão posição do nó atual
        pos = animated_pos if animated_pos else node_positions[player.current_node]
        
        # Determina se está se movendo
        is_moving = animated_pos is not None
        
        # Reproduzir som ninja quando se move
        if is_moving and not hasattr(self, '_last_whoosh_time'):
            self.play_ninja_whoosh()
            self._last_whoosh_time = pygame.time.get_ticks()
        elif is_moving and hasattr(self, '_last_whoosh_time'):
            # Evitar spam de som - só toca a cada 500ms
            current_time = pygame.time.get_ticks()
            if current_time - self._last_whoosh_time > 500:
                self.play_ninja_whoosh()
                self._last_whoosh_time = current_time
        
        if self.use_sprites:
            if is_moving:
                # Personagem se movendo - escolher sprite baseado na direção
                if self.current_movement_direction == "left" and self.run_left_sprites:
                    # Movimento para a esquerda
                    self.update_run_left_animation()
                    self._draw_run_left_sprite_character(pos)
                elif self.run_sprites:
                    # Movimento para outras direções (direita, cima, baixo)
                    self.update_run_animation()
                    self._draw_run_sprite_character(pos)
                else:
                    # Fallback para desenho vetorial se não há sprites
                    self._draw_vector_character(pos)
            elif not is_moving and self.idle_sprites:
                # Personagem parado - usar sprites idle
                self.update_idle_animation()
                self._draw_idle_sprite_character(pos)
            else:
                # Fallback para desenho vetorial se não há sprites
                self._draw_vector_character(pos)
        else:
            # Desenha usando formas geométricas (método original)
            self._draw_vector_character(pos)
    
    def _add_ninja_texture(self):
        """Adiciona uma textura ninja sutil ao fundo"""
        import random
        random.seed(42)  # Seed fixo para consistência
        
        # Adicionar pontos ninja sutis
        for _ in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            alpha = random.randint(8, 20)
            size = random.randint(1, 2)
            
            ninja_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            ninja_color = (*self.NINJA_SHADOW, alpha)
            pygame.draw.circle(ninja_surface, ninja_color, (size, size), size)
            self.screen.blit(ninja_surface, (x-size, y-size))
    
    def _draw_glow_circle(self, pos, radius, color, alpha):
        """Desenha um círculo com efeito de brilho"""
        glow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, alpha), (radius, radius), radius)
        self.screen.blit(glow_surf, (pos[0] - radius, pos[1] - radius))
    
    def _draw_exit_icon(self, pos):
        """Desenha ícone de saída"""
        # Estrela simples
        points = []
        for i in range(5):
            angle = i * 2 * math.pi / 5 - math.pi / 2
            outer_x = pos[0] + math.cos(angle) * 12
            outer_y = pos[1] + math.sin(angle) * 12
            points.append((outer_x, outer_y))
            
            angle = (i + 0.5) * 2 * math.pi / 5 - math.pi / 2
            inner_x = pos[0] + math.cos(angle) * 6
            inner_y = pos[1] + math.sin(angle) * 6
            points.append((inner_x, inner_y))
        
        pygame.draw.polygon(self.screen, (255, 255, 100), points)
    
    def _draw_particle_effects(self, world, player, node_positions):
        """Desenha efeitos de partículas"""
        # Partículas ao redor do jogador
        player_pos = node_positions[player.current_node]
        for i in range(3):
            angle = self.animation_time * 2 + i * 2 * math.pi / 3
            particle_x = player_pos[0] + math.cos(angle) * 35
            particle_y = player_pos[1] + math.sin(angle) * 35
            alpha = int(100 + math.sin(self.animation_time * 3 + i) * 50)
            
            particle_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (100, 200, 255, alpha), (3, 3), 3)
            self.screen.blit(particle_surf, (particle_x - 3, particle_y - 3))
        
        # Partículas ao redor da saída
        exit_pos = node_positions[world.end_node]
        for i in range(5):
            angle = -self.animation_time * 1.5 + i * 2 * math.pi / 5
            particle_x = exit_pos[0] + math.cos(angle) * 40
            particle_y = exit_pos[1] + math.sin(angle) * 40
            alpha = int(80 + math.sin(self.animation_time * 4 + i) * 40)
            
            particle_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (100, 255, 150, alpha), (2, 2), 2)
            self.screen.blit(particle_surf, (particle_x - 2, particle_y - 2))
    
    def _draw_menu_background_effects(self):
        """Desenha efeitos de fundo animados para o menu"""
        # Efeito de partículas flutuantes
        import random
        
        for i in range(20):
            # Posições baseadas no tempo para animação suave
            x = (self.animation_time * 0.5 + i * 60) % (self.width + 100) - 50
            y = 50 + math.sin(self.animation_time * 0.01 + i) * 30 + i * 25
            
            if 0 <= x <= self.width and 0 <= y <= self.height:
                # Partículas pequenas brilhantes
                alpha = int(100 + 50 * math.sin(self.animation_time * 0.02 + i))
                size = 2 + int(math.sin(self.animation_time * 0.03 + i * 0.5))
                
                particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color = (*self.EDGE_COLOR, alpha)
                pygame.draw.circle(particle_surf, color, (size, size), size)
                self.screen.blit(particle_surf, (int(x), int(y)))
        
        # Linhas de grade sutil no fundo
        grid_alpha = 30
        grid_color = (*self.EDGE_COLOR, grid_alpha)
        grid_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        for i in range(0, self.width, 100):
            pygame.draw.line(grid_surf, grid_color, (i, 0), (i, self.height), 1)
        for i in range(0, self.height, 100):
            pygame.draw.line(grid_surf, grid_color, (0, i), (self.width, i), 1)
        
        self.screen.blit(grid_surf, (0, 0))
    
    def _draw_hovered_connections(self, graph, node_positions, hovered_node):
        """Destaca as conexões do nó que está sendo hovered"""
        if hovered_node not in graph.nodes():
            return
        
        # Desenha linhas brilhantes para todos os vizinhos
        for neighbor in graph.neighbors(hovered_node):
            start_pos = node_positions[hovered_node]
            end_pos = node_positions[neighbor]
            
            # Linha brilhante animada
            glow_intensity = int(150 + 50 * math.sin(self.animation_time * 5))
            glow_color = (*self.EDGE_HOVER_COLOR, glow_intensity)
            
            # Desenha múltiplas linhas para efeito de brilho
            for thickness in [8, 6, 4, 2]:
                alpha = max(20, glow_intensity - thickness * 20)
                line_surf = pygame.Surface((abs(end_pos[0] - start_pos[0]) + thickness * 2, 
                                          abs(end_pos[1] - start_pos[1]) + thickness * 2), 
                                          pygame.SRCALPHA)
                
                offset_x = min(start_pos[0], end_pos[0]) - thickness
                offset_y = min(start_pos[1], end_pos[1]) - thickness
                
                adj_start = (start_pos[0] - offset_x, start_pos[1] - offset_y)
                adj_end = (end_pos[0] - offset_x, end_pos[1] - offset_y)
                
                pygame.draw.line(line_surf, (*self.EDGE_HOVER_COLOR, alpha), 
                               adj_start, adj_end, thickness)
                self.screen.blit(line_surf, (offset_x, offset_y))
    
    def _draw_professional_hud(self, world, player):
        """Desenha HUD profissional"""
        # Painel superior
        panel_height = 80
        panel_rect = pygame.Rect(0, 0, self.width, panel_height)
        
        # Fundo do painel com transparencia
        panel_surf = pygame.Surface((self.width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (*self.PANEL_COLOR, 200), (0, 0, self.width, panel_height))
        self.screen.blit(panel_surf, (0, 0))
        
        # Borda do painel
        pygame.draw.line(self.screen, self.PANEL_BORDER, (0, panel_height), (self.width, panel_height), 2)
        
        # Informações do jogador
        margin = 20
        y_pos = 15
        
        # Nome e nível
        name_text = self.font_medium.render(f"🧙 {player.name} (Lv.{player.level})", True, self.TEXT_COLOR)
        self.screen.blit(name_text, (margin, y_pos))
        
        # Barra de vida
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = margin + 250
        health_ratio = player.health / player.max_health
        
        # Fundo da barra
        health_bg = pygame.Rect(health_bar_x, y_pos + 5, health_bar_width, health_bar_height)
        pygame.draw.rect(self.screen, (50, 50, 50), health_bg)
        
        # Barra de vida colorida
        health_width = int(health_bar_width * health_ratio)
        if health_ratio > 0.6:
            health_color = self.HEALTH_GREEN
        elif health_ratio > 0.3:
            health_color = self.HEALTH_YELLOW
        else:
            health_color = self.HEALTH_RED
            
        if health_width > 0:
            health_fill = pygame.Rect(health_bar_x, y_pos + 5, health_width, health_bar_height)
            pygame.draw.rect(self.screen, health_color, health_fill)
        
        pygame.draw.rect(self.screen, self.TEXT_COLOR, health_bg, 2)
        
        # Texto da vida
        health_text = self.font_small.render(f"HP: {player.health}/{player.max_health}", True, self.TEXT_COLOR)
        self.screen.blit(health_text, (health_bar_x + health_bar_width + 10, y_pos + 5))
        
        # Informações do nível
        level_text = self.font_medium.render(f"Nível: {world.level_id} | Nó Atual: {player.current_node} | Meta: {world.end_node}", True, self.TEXT_COLOR)
        self.screen.blit(level_text, (margin, y_pos + 35))
        
        # XP, Pontos e Vidas
        stats_text = self.font_small.render(f"XP: {player.experience}/100 | Pontos: {player.points}", True, (255, 255, 255))
        self.screen.blit(stats_text, (self.width - 300, y_pos))
        
        # Vidas
        lives_text = self.font_small.render(f"❤️ Vidas: {player.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (self.width - 120, y_pos + 20))
        
        # Barra de vida do jogador
        self._draw_health_bar(player, y_pos - 30)
        
        # Controles - linha 1
        controls_line1 = self.font_small.render("WASD: Direções | ESPAÇO: Caminho | R: Reiniciar | ESC: Menu", True, (255, 255, 255))
        self.screen.blit(controls_line1, (self.width - 450, y_pos + 35))
        
        # Controles - linha 2 (diagonais)
        controls_line2 = self.font_small.render("Diagonais: W+A=↖ | W+D=↗ | S+A=↙ | S+D=↘", True, (255, 255, 255))
        self.screen.blit(controls_line2, (self.width - 350, y_pos + 55))

    def draw_menu(self, levels_completed=0, player=None):
        """Desenha apenas os botões de imagem sobre o video background"""
        # Verificar se temos botões carregados
        if not hasattr(self, 'button_images') or not self.button_images:
            return
            
        # Posições dos botões (centralizados verticalmente)
        mouse_pos = pygame.mouse.get_pos()
        
        # Verificar se há progresso salvo (assumindo levels_completed > 0 indica progresso)
        has_progress = levels_completed > 0
        
        # Definir botões a serem exibidos
        buttons_to_draw = [
            ('newgame', 'newgame'),
            ('continue', 'continue' if has_progress else 'continue_disabled'),
            ('exit', 'exit')
        ]
        
        # Calcular espaçamento e posição inicial
        button_spacing = 100  # Espaçamento ainda maior entre botões
        total_height = len(buttons_to_draw) * button_spacing - 30
        start_y = (self.height - total_height) // 2 + 80  # Mover botões para baixo
        
        self.menu_buttons = {}  # Armazenar rects para detecção de clique
        
        for i, (button_id, button_key) in enumerate(buttons_to_draw):
            if button_key in self.button_images:
                button_data = self.button_images[button_key]
                
                # Calcular posição do botão (centralizado)
                button_width, button_height = button_data['normal'].get_size()
                button_x = (self.width - button_width) // 2
                button_y = start_y + (i * button_spacing)
                
                # Criar rect unificado para desenho e detecção
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                
                # Verificar hover (apenas se o botão estiver habilitado)
                is_enabled = not (button_id == 'continue' and not has_progress)
                is_hover = button_rect.collidepoint(mouse_pos) and is_enabled
                
                # Escolher imagem (normal ou hover, apenas se habilitado)
                button_image = button_data['hover'] if is_hover else button_data['normal']
                
                # Desenhar botão
                self.screen.blit(button_image, button_rect)
                
                # Armazenar rect para detecção de clique (apenas se habilitado)
                if is_enabled:
                    self.menu_buttons[button_id] = button_rect
                
                # Efeito de cursor apenas se não estiver em transição e botão habilitado
                if not getattr(self, 'is_transitioning', False):
                    if is_hover and is_enabled:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def draw_level_complete(self, results):
        """Desenha a tela de nível completo com background personalizado e estrelas em imagem"""
        # Reset hover state
        self.hovered_button = None
        
        # Usar background de nível completo ou fallback para ninja
        if hasattr(self, 'level_complete_bg') and self.level_complete_bg:
            self.screen.blit(self.level_complete_bg, (0, 0))
        else:
            self.draw_ninja_background()
        
        # Sistema de estrelas com imagens (acima das estatísticas)
        stars_earned = results.get('stars_earned', 0)
        stars_y = 330  # Posição das estrelas ainda mais abaixo
        self._draw_image_stars_at_position(stars_earned, stars_y)
        
        # Relatório simplificado lado a lado (abaixo das estrelas)
        info_y = 370
        
        # Linha superior: Mundo e Eficiência
        mundo_text = self.font_medium.render(f"Mundo: {results['level_name']}", True, self.TEXT_COLOR)
        eficiencia_text = self.font_medium.render(f"Eficiência: {results['efficiency']*100:.1f}%", True, self.TEXT_COLOR)
        
        # Posicionar textos lado a lado
        mundo_x = self.width // 4 - mundo_text.get_width() // 2
        eficiencia_x = 3 * self.width // 4 - eficiencia_text.get_width() // 2
        
        self.screen.blit(mundo_text, (mundo_x, info_y))
        self.screen.blit(eficiencia_text, (eficiencia_x, info_y))
        
        # Linha inferior: Tempo e Pontuação
        tempo_text = self.font_medium.render(f"Tempo: {results['time_taken']:.1f}s", True, self.TEXT_COLOR)
        pontuacao_text = self.font_medium.render(f"Pontuação: {results['total_score']} (+{results['xp_gained']} XP)", True, self.TEXT_COLOR)
        
        tempo_x = self.width // 4 - tempo_text.get_width() // 2
        pontuacao_x = 3 * self.width // 4 - pontuacao_text.get_width() // 2
        
        self.screen.blit(tempo_text, (tempo_x, info_y + 35))
        self.screen.blit(pontuacao_text, (pontuacao_x, info_y + 35))
        
        # Botões com imagens
        y = info_y + 60  # Ainda menos espaço após as informações lado a lado
        can_advance = results.get('can_advance', False)
        
        # Botões da tela de conclusão
        completion_buttons = [
            ('next_level' if can_advance else 'next_level_disabled', 'next_level'),
            ('repeat_level', 'repeat_level'),
            ('main_menu', 'main_menu')
        ]
        
        button_spacing = 120  # Maior gap entre botões
        self.completion_buttons = {}  # Para detecção de clique
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (button_key, button_id) in enumerate(completion_buttons):
            # Pular botão de próximo nível se não habilitado e sem imagem disabled
            if button_key == 'next_level_disabled' and 'next_level_disabled' not in self.button_images:
                continue
                
            if button_key in self.button_images or (button_key == 'next_level_disabled' and 'next_level' in self.button_images):
                # Usar imagem normal para disabled se não houver versão disabled
                actual_key = button_key if button_key in self.button_images else 'next_level'
                button_data = self.button_images[actual_key]
                
                # Calcular posição do botão
                button_width, button_height = button_data['normal'].get_size()
                button_x = (self.width - button_width) // 2
                button_y = y + (i * button_spacing)
                
                # Criar rect para detecção
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                
                # Verificar hover (apenas se habilitado)
                is_enabled = not (button_key == 'next_level_disabled')
                is_hover = button_rect.collidepoint(mouse_pos) and is_enabled
                
                # Escolher imagem
                if button_key == 'next_level_disabled':
                    # Botão disabled - usar imagem normal sem hover
                    button_image = button_data['normal']
                    # Aplicar efeito de desabilitação
                    disabled_surface = button_image.copy()
                    disabled_overlay = pygame.Surface(disabled_surface.get_size(), pygame.SRCALPHA)
                    disabled_overlay.fill((128, 128, 128, 128))  # Overlay cinza
                    disabled_surface.blit(disabled_overlay, (0, 0), special_flags=pygame.BLEND_MULT)
                    button_image = disabled_surface
                else:
                    button_image = button_data['hover'] if is_hover else button_data['normal']
                
                # Desenhar botão
                self.screen.blit(button_image, button_rect)
                
                # Armazenar para detecção de clique
                if is_enabled:
                    self.completion_buttons[button_id] = button_rect
                
                # Cursor
                if not getattr(self, 'is_transitioning', False) and is_hover and is_enabled:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif not is_hover:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def _draw_rounded_rect(self, surface, color, x, y, width, height, radius):
        """Desenha um retângulo com bordas arredondadas reais"""
        # Retângulo central
        pygame.draw.rect(surface, color, (x + radius, y, width - 2 * radius, height))
        pygame.draw.rect(surface, color, (x, y + radius, width, height - 2 * radius))
        
        # Círculos nos cantos
        pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + width - radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + radius, y + height - radius), radius)
        pygame.draw.circle(surface, color, (x + width - radius, y + height - radius), radius)
    
    def _draw_rounded_rect_border(self, surface, color, x, y, width, height, radius, thickness):
        """Desenha a borda de um retângulo com bordas arredondadas usando múltiplos retângulos concêntricos"""
        # Método mais simples: desenha múltiplos retângulos arredondados menores para criar borda
        for i in range(thickness):
            # Desenha contorno externo
            outer_radius = radius
            # Linhas das bordas
            pygame.draw.line(surface, color, (x + outer_radius, y + i), (x + width - outer_radius, y + i), 1)
            pygame.draw.line(surface, color, (x + outer_radius, y + height - 1 - i), (x + width - outer_radius, y + height - 1 - i), 1)
            pygame.draw.line(surface, color, (x + i, y + outer_radius), (x + i, y + height - outer_radius), 1)
            pygame.draw.line(surface, color, (x + width - 1 - i, y + outer_radius), (x + width - 1 - i, y + height - outer_radius), 1)
            
            # Cantos arredondados usando arcos simples
            import math
            # Canto superior esquerdo (0 a 90 graus)
            pygame.draw.arc(surface, color, (x + i, y + i, 2 * outer_radius, 2 * outer_radius), math.pi, 3*math.pi/2, 1)
            # Canto superior direito (90 a 180 graus)  
            pygame.draw.arc(surface, color, (x + width - 2*outer_radius - i, y + i, 2 * outer_radius, 2 * outer_radius), 3*math.pi/2, 2*math.pi, 1)
            # Canto inferior direito (180 a 270 graus)
            pygame.draw.arc(surface, color, (x + width - 2*outer_radius - i, y + height - 2*outer_radius - i, 2 * outer_radius, 2 * outer_radius), 0, math.pi/2, 1)
            # Canto inferior esquerdo (270 a 360 graus)
            pygame.draw.arc(surface, color, (x + i, y + height - 2*outer_radius - i, 2 * outer_radius, 2 * outer_radius), math.pi/2, math.pi, 1)
    
    def _draw_stars_display(self, stars_earned, efficiency, compact=False):
        """Desenha o display de estrelas ganhas"""
        if compact:
            star_y = 150
            star_size = 30
        else:
            star_y = 120
            star_size = 40
        total_width = 3 * star_size + 2 * 20  # 3 estrelas + espaçamento
        start_x = (self.width - total_width) // 2
        
        # Título das estrelas
        star_title = self.font_large.render("Classificação:", True, self.TEXT_COLOR)
        title_rect = star_title.get_rect(center=(self.width // 2, star_y - 30))
        self.screen.blit(star_title, title_rect)
        
        # Desenha as 3 estrelas
        for i in range(3):
            x = start_x + i * (star_size + 20)
            
            if i < stars_earned:
                # Estrela dourada (ganha)
                star_color = (255, 215, 0)  # Dourado
                pygame.draw.polygon(self.screen, star_color, self._get_star_points(x, star_y, star_size // 2))
                pygame.draw.polygon(self.screen, (79, 5, 25), self._get_star_points(x, star_y, star_size // 2), 2)
            else:
                # Estrela cinza (não ganha)
                star_color = (80, 80, 80)
                pygame.draw.polygon(self.screen, star_color, self._get_star_points(x, star_y, star_size // 2))
                pygame.draw.polygon(self.screen, (120, 120, 120), self._get_star_points(x, star_y, star_size // 2), 2)
        
        # Texto explicativo
        star_messages = {
            3: "PERFEITO!",
            2: "⭐ MUITO BOM! ⭐", 
            1: "⭐ BOM TRABALHO ⭐",
            0: "❌ PRECISA MELHORAR"
        }
        
        message = star_messages.get(stars_earned, "")
        if message:
            msg_surface = self.font_large.render(message, True, self.HEALTH_GREEN if stars_earned >= 2 else self.HEALTH_YELLOW if stars_earned == 1 else self.HEALTH_RED)
            msg_rect = msg_surface.get_rect(center=(self.width // 2, star_y + 60))
            self.screen.blit(msg_surface, msg_rect)
        
        # Requisitos para estrelas
        req_text = "Requisitos: 1⭐(60%+)  2⭐(80%+)  3⭐(95%+)"
        req_surface = self.font_small.render(req_text, True, (255, 255, 255))
        req_rect = req_surface.get_rect(center=(self.width // 2, star_y + 90))
        self.screen.blit(req_surface, req_rect)
    
    def _get_star_points(self, cx, cy, radius):
        """Retorna os pontos para desenhar uma estrela de 5 pontas"""
        import math
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                # Pontas externas
                r = radius
            else:
                # Pontas internas
                r = radius * 0.4
            x = cx + r * math.cos(angle - math.pi/2)
            y = cy + r * math.sin(angle - math.pi/2)
            points.append((x, y))
        return points
    
    def _draw_directional_indicators(self, world, player, node_positions):
        """Desenha indicadores direcionais sutis ao redor do jogador"""
        if player.current_node not in node_positions:
            return
            
        current_pos = node_positions[player.current_node]
        neighbors = list(world.graph.neighbors(player.current_node))
        
        if not neighbors:
            return
        
        # Define as direções, seus ícones e teclas
        directions = {
            'up': (0, -1, '↑', 'W'),
            'down': (0, 1, '↓', 'S'), 
            'left': (-1, 0, '←', 'A'),
            'right': (1, 0, '→', 'D'),
            'northwest': (-1, -1, '↖', 'W+A'),
            'northeast': (1, -1, '↗', 'W+D'),
            'southwest': (-1, 1, '↙', 'S+A'),
            'southeast': (1, 1, '↘', 'S+D')
        }
        
        # Verifica quais direções têm nós disponíveis
        available_directions = set()
        
        for neighbor in neighbors:
            neighbor_pos = node_positions[neighbor]
            dx = neighbor_pos[0] - current_pos[0]
            dy = neighbor_pos[1] - current_pos[1]
            
            distance = math.sqrt(dx*dx + dy*dy)
            if distance == 0:
                continue
                
            norm_dx = dx / distance
            norm_dy = dy / distance
            
            # Determina a direção mais próxima
            best_direction = None
            best_similarity = -1
            
            for direction, (target_dx, target_dy, _, _) in directions.items():
                # Normaliza o vetor direção alvo
                target_length = math.sqrt(target_dx*target_dx + target_dy*target_dy)
                if target_length == 0:
                    continue
                target_norm_dx = target_dx / target_length
                target_norm_dy = target_dy / target_length
                
                # Calcula similaridade
                similarity = norm_dx * target_norm_dx + norm_dy * target_norm_dy
                
                if similarity > best_similarity and similarity > 0.5:  # Threshold para considerar a direção
                    best_similarity = similarity
                    best_direction = direction
            
            if best_direction:
                available_directions.add(best_direction)
        
        # Desenha indicadores sutis para direções disponíveis
        indicator_radius = 60
        for direction in available_directions:
            if direction in directions:
                dx, dy, icon, keys = directions[direction]
                
                # Posição do indicador
                indicator_x = current_pos[0] + dx * indicator_radius
                indicator_y = current_pos[1] + dy * indicator_radius
                
                # Cor baseada no tipo de direção
                if direction in ['up', 'down', 'left', 'right']:
                    color = (100, 150, 255)  # Azul para direções cardeais
                    alpha = 120
                    circle_size = 15
                else:
                    color = (255, 150, 100)  # Laranja para direções diagonais
                    alpha = 100
                    circle_size = 18  # Maior para diagonais
                
                # Desenha círculo sutil
                indicator_surf = pygame.Surface((circle_size * 2, circle_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(indicator_surf, (*color, alpha), (circle_size, circle_size), circle_size)
                pygame.draw.circle(indicator_surf, (*color, alpha + 50), (circle_size, circle_size), circle_size, 2)
                
                self.screen.blit(indicator_surf, (indicator_x - circle_size, indicator_y - circle_size))
                
                # Desenha ícone direcional
                icon_surface = self.font_small.render(icon, True, (255, 255, 255))
                icon_rect = icon_surface.get_rect(center=(indicator_x, indicator_y - 5))
                self.screen.blit(icon_surface, icon_rect)
                
                # Desenha teclas embaixo
                keys_surface = pygame.font.Font(None, 16).render(keys, True, (255, 255, 255))
                keys_rect = keys_surface.get_rect(center=(indicator_x, indicator_y + 8))
                self.screen.blit(keys_surface, keys_rect)
    
    def _get_suggested_keys(self, world, player, target_node, node_positions):
        """Calcula qual combinação de teclas usar para alcançar o nó alvo"""
        if player.current_node not in node_positions or target_node not in node_positions:
            return "WASD"
        
        current_pos = node_positions[player.current_node]
        target_pos = node_positions[target_node]
        
        # Calcula direção
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        
        distance = math.sqrt(dx*dx + dy*dy)
        if distance == 0:
            return "WASD"
        
        norm_dx = dx / distance
        norm_dy = dy / distance
        
        # Define as direções e teclas correspondentes
        directions = {
            'up': (0, -1, 'W'),
            'down': (0, 1, 'S'),
            'left': (-1, 0, 'A'),
            'right': (1, 0, 'D'),
            'northwest': (-1, -1, 'W+A'),
            'northeast': (1, -1, 'W+D'),
            'southwest': (-1, 1, 'S+A'),
            'southeast': (1, 1, 'S+D')
        }
        
        # Encontra a direção mais próxima
        best_direction = None
        best_similarity = -1
        
        for direction, (target_dx, target_dy, keys) in directions.items():
            # Normaliza o vetor direção alvo
            target_length = math.sqrt(target_dx*target_dx + target_dy*target_dy)
            if target_length == 0:
                continue
            target_norm_dx = target_dx / target_length
            target_norm_dy = target_dy / target_length
            
            # Calcula similaridade (produto escalar)
            similarity = norm_dx * target_norm_dx + norm_dy * target_norm_dy
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_direction = keys
        
        return best_direction or "WASD"
    
    def _draw_button(self, text, x, y, width, height, color, shortcut, clickable=True, button_id=None):
        """Desenha um botão estilizado com bordas arredondadas reais e efeito hover"""
        # Verificar se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = (clickable and 
                     x <= mouse_pos[0] <= x + width and 
                     y <= mouse_pos[1] <= y + height)
        
        # Atualizar estado do hover
        if is_hovered and button_id:
            self.hovered_button = button_id
        
        # Cor do botão baseada no estado - Estética ninja refinada
        if not clickable:
            button_color = self.NINJA_DARK  # Ninja escuro
            text_color = (120, 120, 120)
            border_color = (80, 80, 80)
            shadow_color = self.NINJA_SHADOW
        elif is_hovered:
            # Efeito hover ninja: vermelho brilhante com ouro
            button_color = self.NINJA_ACCENT  # Vermelho ninja
            text_color = self.NINJA_GOLD  # Texto dourado ninja
            border_color = self.NINJA_GOLD  # Borda dourada
            shadow_color = (60, 15, 30)  # Sombra mais intensa
        else:
            button_color = color
            text_color = self.TEXT_COLOR
            border_color = self.NODE_BORDER_COLOR  # Borda ninja consistente
            shadow_color = self.NINJA_SHADOW
        
        # Desenha sombra primeiro (atrás do botão)
        shadow_offset = 3 if is_hovered else 2
        self._draw_rounded_rect(self.screen, shadow_color, 
                               x + shadow_offset, y + shadow_offset, width, height, 12)
        
        # Desenha fundo do botão com bordas arredondadas reais
        self._draw_rounded_rect(self.screen, button_color, x, y, width, height, 12)
        
        # Borda arredondada
        self._draw_rounded_rect_border(self.screen, border_color, x, y, width, height, 12, 3)
        
        # Texto principal
        text_surface = self.font_medium.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2 - 5))
        self.screen.blit(text_surface, text_rect)
        
        # Atalho de teclado
        shortcut_surface = self.font_small.render(f"({shortcut})", True, (255, 255, 255))
        shortcut_rect = shortcut_surface.get_rect(center=(x + width // 2, y + height // 2 + 15))
        self.screen.blit(shortcut_surface, shortcut_rect)
    
    def draw_game_over(self, player):
        """Desenha a tela de game over"""
        # Reset hover state
        self.hovered_button = None
        
        # Usar background ninja na tela de game over
        self.draw_ninja_background()
        
        # Título
        title = self.font_title.render("GAME OVER", True, (255, 50, 50))
        title_rect = title.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_large.render("Suas vidas acabaram!", True, self.TEXT_COLOR)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Estatísticas finais
        y = 300
        stats_lines = [
            f"Nível Alcançado: {player.level}",
            f"Pontuação Total: {player.points}",
            f"Experiência: {player.experience}"
        ]
        
        for line in stats_lines:
            text = self.font_medium.render(line, True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 40
        
        # Botões
        y += 60
        self._draw_button("Recomeçar", self.width // 2 - 150, y, 300, 50, 
                        self.HEALTH_GREEN, "1 ou ESPAÇO", clickable=True, button_id="restart_game")
        
        y += 70
        self._draw_button("Menu Principal", self.width // 2 - 150, y, 300, 50, 
                        (80, 80, 120), "2 ou ESC", clickable=True, button_id="main_menu_gameover")
    
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
            surface = self.font_small.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (10, self.height - 30))
    
    def load_idle_sprites(self):
        """Carrega os sprites de animação idle (idle0.png até idle4.png)"""
        import os
        import time
        
        self.idle_sprites = []
        self.idle_animation_timer = time.time()
        
        # Tenta carregar idle0.png até idle4.png
        for i in range(5):
            sprite_path = f"idle{i}.png"
            if os.path.exists(sprite_path):
                try:
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    # Redimensiona para tamanho adequado (40x40 pixels)
                    sprite = pygame.transform.scale(sprite, (120, 120))
                    self.idle_sprites.append(sprite)
                    print(f"✅ Sprite carregado: {sprite_path}")
                except pygame.error as e:
                    print(f"❌ Erro ao carregar {sprite_path}: {e}")
            else:
                print(f"⚠️ Arquivo não encontrado: {sprite_path}")
        
        if not self.idle_sprites:
            print("🎨 Nenhum sprite encontrado, usando desenho vetorial")
            self.use_sprites = False
        else:
            print(f"🎬 {len(self.idle_sprites)} sprites carregados para animação idle")
    
    def update_idle_animation(self):
        """Atualiza a animação idle do personagem"""
        if not self.idle_sprites:
            return
            
        import time
        current_time = time.time()
        
        if current_time - self.idle_animation_timer >= self.idle_frame_duration:
            self.current_idle_frame = (self.current_idle_frame + 1) % len(self.idle_sprites)
            self.idle_animation_timer = current_time
    
    def _draw_idle_sprite_character(self, pos):
        """Desenha o personagem usando sprites de idle (parado)"""
        if not self.idle_sprites:
            return
            
        # Efeito de brilho sutil atrás do sprite
        glow_radius = int(25 * self.player_pulse)
        self._draw_glow_circle(pos, glow_radius, self.PLAYER_GLOW, 15)
        
        # Desenha o sprite atual da animação idle
        current_sprite = self.idle_sprites[self.current_idle_frame]
        sprite_rect = current_sprite.get_rect(center=pos)
        self.screen.blit(current_sprite, sprite_rect)
    
    def _draw_run_sprite_character(self, pos):
        """Desenha o personagem usando sprites de corrida (movimento)"""
        if not self.run_sprites:
            return
            
        # Efeito de brilho mais intenso durante movimento
        glow_radius = int(30 * self.player_pulse)
        self._draw_glow_circle(pos, glow_radius, self.PLAYER_GLOW, 20)
        
        # Desenha o sprite atual da animação de corrida
        current_sprite = self.run_sprites[self.current_run_frame]
        sprite_rect = current_sprite.get_rect(center=pos)
        self.screen.blit(current_sprite, sprite_rect)
    
    def _draw_run_left_sprite_character(self, pos):
        """Desenha o personagem usando sprites de corrida para a esquerda"""
        if not self.run_left_sprites:
            return
            
        # Efeito de brilho mais intenso durante movimento
        glow_radius = int(30 * self.player_pulse)
        self._draw_glow_circle(pos, glow_radius, self.PLAYER_GLOW, 20)
        
        # Desenha o sprite atual da animação de corrida para a esquerda
        current_sprite = self.run_left_sprites[self.current_run_left_frame]
        sprite_rect = current_sprite.get_rect(center=pos)
        self.screen.blit(current_sprite, sprite_rect)
    
    def _draw_vector_character(self, pos):
        """Desenha o personagem usando formas geométricas (método original)"""
        # Efeito de brilho pulsante
        glow_radius = int(30 * self.player_pulse)
        self._draw_glow_circle(pos, glow_radius, self.PLAYER_GLOW, 20)
        
        # Corpo do personagem (círculo principal)
        body_radius = int(20 * self.player_pulse)
        pygame.draw.circle(self.screen, self.PLAYER_COLOR, pos, body_radius)
        pygame.draw.circle(self.screen, (79, 5, 25), pos, body_radius, 3)
        
        # Cabeça do personagem
        head_pos = (pos[0], pos[1] - 8)
        pygame.draw.circle(self.screen, (255, 200, 150), head_pos, 8)  # Cor da pele
        pygame.draw.circle(self.screen, (79, 5, 25), head_pos, 8, 2)
        
        # Olhos
        eye_left = (head_pos[0] - 3, head_pos[1] - 2)
        eye_right = (head_pos[0] + 3, head_pos[1] - 2)
        pygame.draw.circle(self.screen, (0, 0, 0), eye_left, 2)
        pygame.draw.circle(self.screen, (0, 0, 0), eye_right, 2)
        
        # Sorriso
        mouth_start = (head_pos[0] - 3, head_pos[1] + 2)
        mouth_end = (head_pos[0] + 3, head_pos[1] + 2)
        pygame.draw.arc(self.screen, (0, 0, 0), 
                       (mouth_start[0], mouth_start[1] - 2, 6, 4), 0, math.pi, 2)
        
        # Braços (linhas animadas)
        arm_offset = math.sin(self.animation_time * 2) * 3
        left_arm_end = (pos[0] - 12, pos[1] + arm_offset)
        right_arm_end = (pos[0] + 12, pos[1] + arm_offset)
        pygame.draw.line(self.screen, (255, 200, 150), pos, left_arm_end, 3)
        pygame.draw.line(self.screen, (255, 200, 150), pos, right_arm_end, 3)
        
        # Pernas
        leg_offset = math.sin(self.animation_time * 2 + 1) * 2
        left_leg_end = (pos[0] - 6, pos[1] + 15 + leg_offset)
        right_leg_end = (pos[0] + 6, pos[1] + 15 - leg_offset)
        pygame.draw.line(self.screen, (255, 200, 150), pos, left_leg_end, 3)
        pygame.draw.line(self.screen, (255, 200, 150), pos, right_leg_end, 3)
    
    def handle_menu_button_click(self, pos):
        """Detecta cliques nos botões de imagem do menu"""
        if not hasattr(self, 'menu_buttons'):
            return None
            
        for button_name, button_rect in self.menu_buttons.items():
            if button_rect.collidepoint(pos):
                print(f"💆 Clique no botão: {button_name}")
                return button_name
                
        return None
    
    def handle_completion_button_click(self, pos):
        """Detecta cliques nos botões de imagem da tela de conclusão"""
        if not hasattr(self, 'completion_buttons'):
            return None
            
        for button_name, button_rect in self.completion_buttons.items():
            if button_rect.collidepoint(pos):
                print(f"🎯 Clique no botão de conclusão: {button_name}")
                return button_name
                
        return None
    
    def load_background(self):
        """Carrega a imagem de fundo ninja"""
        try:
            import os
            background_path = "level1_1.png"
            print(f"🔍 Tentando carregar background: {background_path}")
            print(f"📁 Diretório atual: {os.getcwd()}")
            print(f"📋 Arquivos no diretório: {[f for f in os.listdir('.') if f.endswith('.png')]}")
            
            if os.path.exists(background_path):
                self.background_image = pygame.image.load(background_path).convert()
                # Redimensionar para cobrir toda a tela
                self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
                print(f"✅ Background ninja carregado com sucesso: {background_path}")
                print(f"📏 Dimensões: {self.background_image.get_size()}")
            else:
                print(f"❌ Background não encontrado: {background_path}")
                self.background_image = None
        except Exception as e:
            print(f"❌ Erro ao carregar background: {e}")
            self.background_image = None
    
    def load_level_complete_background(self):
        """Carrega o background de nível completo"""
        try:
            import os
            bg_path = "images/background/nivelcompleto.png"
            if os.path.exists(bg_path):
                original = pygame.image.load(bg_path).convert()
                self.level_complete_bg = pygame.transform.scale(original, (self.width, self.height))
                print(f"✅ Background de nível completo carregado: {bg_path}")
            else:
                print(f"⚠️ Background de nível completo não encontrado: {bg_path}")
                self.level_complete_bg = None
        except Exception as e:
            print(f"❌ Erro ao carregar background de nível completo: {e}")
            self.level_complete_bg = None
    
    def load_star_images(self):
        """Carrega as imagens de estrelas"""
        try:
            import os
            self.star_images = {}
            star_files = {
                1: "images/elements/onestar.png",
                2: "images/elements/twostars.png", 
                3: "images/elements/threestarts.png"
            }
            
            for stars, path in star_files.items():
                if os.path.exists(path):
                    self.star_images[stars] = pygame.image.load(path).convert_alpha()
                    print(f"✅ Imagem de {stars} estrela(s) carregada: {path}")
                else:
                    print(f"⚠️ Imagem de estrelas não encontrada: {path}")
        except Exception as e:
            print(f"❌ Erro ao carregar imagens de estrelas: {e}")
            self.star_images = {}
    
    def load_enemy_images(self):
        """Carrega as imagens dos inimigos"""
        try:
            import os
            oni_path = "images/enemy/oni.png"
            if os.path.exists(oni_path):
                self.oni_image = pygame.image.load(oni_path).convert_alpha()
                # Redimensionar para tamanho adequado (60x60 pixels)
                self.oni_image = pygame.transform.scale(self.oni_image, (60, 60))
                print(f"✅ Imagem do Oni carregada: {oni_path}")
            else:
                print(f"⚠️ Imagem do Oni não encontrada: {oni_path}")
                self.oni_image = None
        except Exception as e:
            print(f"❌ Erro ao carregar imagem do Oni: {e}")
            self.oni_image = None
    
    def load_ninja_sounds(self):
        """Carrega os sons ninja"""
        try:
            # Inicializar mixer do pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            
            import os
            sound_path = "sounds/810736__mokasza__fast-whoosh.mp3"
            print(f"🔊 Tentando carregar som ninja: {sound_path}")
            
            if os.path.exists(sound_path):
                self.whoosh_sound = pygame.mixer.Sound(sound_path)
                self.whoosh_sound.set_volume(0.3)  # Volume moderado
                print(f"🥷 Som ninja carregado com sucesso!")
            else:
                print(f"⚠️ Som ninja não encontrado: {sound_path}")
                self.whoosh_sound = None
            
            # Carregar som de vitória
            victory_path = "sounds/victory.wav"
            if os.path.exists(victory_path):
                self.victory_sound = pygame.mixer.Sound(victory_path)
                self.victory_sound.set_volume(0.5)  # Volume um pouco mais alto para vitória
                print(f"🏆 Som de vitória carregado com sucesso!")
            else:
                print(f"⚠️ Som de vitória não encontrado: {victory_path}")
                self.victory_sound = None
            
            # Carregar e iniciar música de fundo
            background_music_path = "sounds/background-music.mp3"
            if os.path.exists(background_music_path):
                pygame.mixer.music.load(background_music_path)
                pygame.mixer.music.set_volume(0.3)  # Volume baixo para não incomodar
                pygame.mixer.music.play(-1)  # -1 para loop infinito
                print(f"🎵 Música de fundo iniciada em loop!")
            else:
                print(f"⚠️ Música de fundo não encontrada: {background_music_path}")
                
        except Exception as e:
            print(f"❌ Erro ao carregar sons ninja: {e}")
            self.whoosh_sound = None
    
    def play_ninja_whoosh(self):
        """Reproduz o som de movimento ninja"""
        try:
            if hasattr(self, 'whoosh_sound') and self.whoosh_sound:
                # Para o som anterior se ainda estiver tocando
                self.whoosh_sound.stop()
                # Reproduz o som de movimento
                self.whoosh_sound.play()
        except Exception as e:
            # Falha silenciosa para não interromper o jogo
            pass
    
    def play_victory_sound(self):
        """Reproduz o som de vitória"""
        try:
            if hasattr(self, 'victory_sound') and self.victory_sound:
                # Para outros sons que possam estar tocando
                if hasattr(self, 'whoosh_sound') and self.whoosh_sound:
                    self.whoosh_sound.stop()
                # Reproduz o som de vitória
                self.victory_sound.play()
                print("🎵 Som de vitória tocando!")
        except Exception as e:
            # Falha silenciosa para não interromper o jogo
            pass
    
    def play_damage_sound(self):
        """Reproduz som de dano (usando o whoosh em volume mais baixo)"""
        try:
            if hasattr(self, 'whoosh_sound') and self.whoosh_sound:
                # Cria uma cópia temporária do som com volume reduzido para efeito de dano
                self.whoosh_sound.set_volume(0.3)  # Volume mais baixo para efeito de dano
                self.whoosh_sound.play()
                print("💥 Som de dano tocando!")
        except Exception as e:
            # Falha silenciosa para não interromper o jogo
            pass
    
    def pause_background_music(self):
        """Pausa a música de fundo"""
        try:
            pygame.mixer.music.pause()
            print("⏸️ Música de fundo pausada")
        except Exception as e:
            pass
    
    def resume_background_music(self):
        """Resume a música de fundo"""
        try:
            pygame.mixer.music.unpause()
            print("▶️ Música de fundo retomada")
        except Exception as e:
            pass
    
    def stop_background_music(self):
        """Para a música de fundo"""
        try:
            pygame.mixer.music.stop()
            print("⏹️ Música de fundo parada")
        except Exception as e:
            pass
    
    def load_button_images(self):
        """Carrega as imagens dos botões do menu"""
        try:
            import os
            self.button_images = {}
            
            # Definir botões disponíveis (menu e conclusão)
            buttons = {
                'newgame': 'bttns/novojogo (1).png',
                'continue': 'bttns/continuar (1).png',
                'continue_disabled': 'bttns/continuardisabled (1).png',
                'exit': 'bttns/sair (2).png',
                'next_level': 'bttns/nextlevel.png',
                'repeat_level': 'bttns/repeatlevel.png',
                'main_menu': 'bttns/gotomenu.png'
            }
            
            for button_name, button_path in buttons.items():
                if os.path.exists(button_path):
                    # Carregar imagem original
                    original = pygame.image.load(button_path).convert_alpha()
                    
                    # Usar tamanho original das novas imagens menores
                    original = original  # Manter tamanho original
                    
                    # Criar versão hover (dessaturação sutil)
                    hover = original.copy()
                    # Aplicar efeito de dessaturação muito sutil
                    desaturate_overlay = pygame.Surface(hover.get_size(), pygame.SRCALPHA)
                    desaturate_overlay.fill((128, 128, 128, 15))  # Cinza muito sutil para dessaturar
                    hover.blit(desaturate_overlay, (0, 0), special_flags=pygame.BLEND_MULT)
                    
                    self.button_images[button_name] = {
                        'normal': original,
                        'hover': hover,
                        'rect': original.get_rect()
                    }
                    print(f"✅ Botão carregado: {button_name} - {button_path}")
                else:
                    print(f"⚠️ Botão não encontrado: {button_path}")
                    
        except Exception as e:
            print(f"❌ Erro ao carregar botões: {e}")
            self.button_images = {}
    
    def start_fade_transition(self, callback=None, fade_out_first=True):
        """Inicia uma transição fade clássica"""
        self.is_transitioning = True
        self.transition_callback = callback
        self.fade_out_first = fade_out_first
        
        if fade_out_first:
            # Começa transparente e escurece
            self.transition_alpha = 0
            self.fading_out = True
        else:
            # Começa escuro e clareia
            self.transition_alpha = 255
            self.fading_out = False
            
        print(f"🎬 Iniciando transição fade {'out' if fade_out_first else 'in'}")
    
    def update_transition(self):
        """Atualiza a transição fade"""
        if not self.is_transitioning:
            return False
            
        if self.fading_out:
            # Fade out (escurecer)
            self.transition_alpha = min(255, self.transition_alpha + self.transition_speed)
            if self.transition_alpha >= 255:
                # Executar callback quando completamente preto
                if self.transition_callback:
                    self.transition_callback()
                    self.transition_callback = None
                self.fading_out = False
        else:
            # Fade in (clarear)
            self.transition_alpha = max(0, self.transition_alpha - self.transition_speed)
            if self.transition_alpha <= 0:
                self.is_transitioning = False
                return True
        
        return False
    
    def apply_transition_effect(self):
        """Aplica efeito de transição diretamente na tela"""
        if self.is_transitioning and self.transition_alpha > 0:
            # Criar overlay preto com alpha usando SRCALPHA para melhor blending
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.transition_alpha))
            
            # Aplicar diretamente na tela
            self.screen.blit(overlay, (0, 0))
    
    def _draw_health_bar(self, player, y_pos):
        """Desenha a barra de vida do jogador"""
        # Posição e dimensões da barra
        bar_width = 200
        bar_height = 20
        bar_x = self.width - bar_width - 20
        bar_y = y_pos
        
        # Calcula porcentagem de vida
        health_percentage = player.health / player.max_health
        
        # Borda da barra
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2)
        
        # Fundo da barra (vermelho escuro)
        pygame.draw.rect(self.screen, (100, 20, 20), (bar_x, bar_y, bar_width, bar_height))
        
        # Barra de vida (verde para saudável, amarelo para médio, vermelho para crítico)
        if health_percentage > 0.6:
            health_color = (50, 200, 50)  # Verde
        elif health_percentage > 0.3:
            health_color = (200, 200, 50)  # Amarelo
        else:
            health_color = (200, 50, 50)  # Vermelho
            
        health_width = int(bar_width * health_percentage)
        if health_width > 0:
            pygame.draw.rect(self.screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Texto da vida
        health_text = self.font_small.render(f"❤️ {player.health}/{player.max_health}", True, (255, 255, 255))
        self.screen.blit(health_text, (bar_x - 80, bar_y))
    
    def draw_ninja_background(self):
        """Desenha o fundo ninja com efeitos"""
        if hasattr(self, 'background_image') and self.background_image:
            # Desenhar a imagem de fundo
            self.screen.blit(self.background_image, (0, 0))
            
            # Adicionar overlay muito sutil para não escurecer demais
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((self.BG_COLOR[0], self.BG_COLOR[1], self.BG_COLOR[2], 30))
            self.screen.blit(overlay, (0, 0))
        else:
            # Fallback para cor sólida se não houver imagem
            self.screen.fill(self.BG_COLOR)
    
    def _draw_image_stars(self, stars_earned):
        """Desenha estrelas usando imagens (centralizado na tela)"""
        if hasattr(self, 'star_images') and stars_earned in self.star_images:
            star_image = self.star_images[stars_earned]
            # Centralizar a imagem de estrelas na tela
            star_rect = star_image.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(star_image, star_rect)
        else:
            # Fallback para desenho manual se imagens não estiverem disponíveis
            self._draw_stars_display(stars_earned, 0, compact=True)
    
    def _draw_image_stars_at_position(self, stars_earned, y_position):
        """Desenha estrelas usando imagens em uma posição Y específica"""
        if hasattr(self, 'star_images') and stars_earned in self.star_images:
            star_image = self.star_images[stars_earned]
            # Centralizar horizontalmente, posicionar na altura especificada
            star_rect = star_image.get_rect(center=(self.width // 2, y_position))
            self.screen.blit(star_image, star_rect)
        else:
            # Fallback para desenho manual se imagens não estiverem disponíveis
            self._draw_stars_display(stars_earned, 0, compact=True)
    
    def _draw_enemies(self, world, node_positions):
        """Desenha inimigos nos nós que os possuem"""
        if not hasattr(world, 'enemies') or not world.enemies:
            return
            
        if not hasattr(self, 'oni_image') or not self.oni_image:
            return
            
        for node_id in world.enemies:
            if node_id in node_positions:
                node_pos = node_positions[node_id]
                # Posicionar o oni ligeiramente acima do nó
                oni_x = node_pos[0] - 30  # Centralizar horizontalmente
                oni_y = node_pos[1] - 40  # Posicionar acima do nó
                
                # Desenhar uma sombra sutil atrás do oni
                shadow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
                shadow_surf.fill((0, 0, 0, 60))
                self.screen.blit(shadow_surf, (oni_x + 3, oni_y + 3))
                
                # Desenhar o oni
                self.screen.blit(self.oni_image, (oni_x, oni_y))
                
                # Adicionar efeito de brilho vermelho ao redor
                red_glow = pygame.Surface((70, 70), pygame.SRCALPHA)
                pygame.draw.circle(red_glow, (255, 0, 0, 30), (35, 35), 35)
                self.screen.blit(red_glow, (oni_x - 5, oni_y - 5))
