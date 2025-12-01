"""
PathFinder Adventure - Jogo de Grafos e Matemática Discreta
Um jogo educativo que ensina conceitos de teoria dos grafos de forma divertida!
"""
import pygame
import sys
import math
from player import Player
from world import World
from visualizer import Visualizer
from pathfinding import dijkstra, calculate_path_efficiency
import time
from modern_ui import ModernNinjaUI, NinjaMenuSystem
import cv2
import numpy as np

class Game:
    def __init__(self):
        pygame.init()
        self.visualizer = Visualizer()
        
        # Sistema de UI moderna ninja
        self.modern_ui = ModernNinjaUI(1200, 800)
        self.menu_system = NinjaMenuSystem(1200, 800)
        
        # Sistema de transições
        self.pending_state_change = None
        self.pending_level = None
        
        # Sistema de vídeo background
        self.video_cap = None
        self.video_surface = None
        self.video_frame = None
        self.load_video_background()
        
        # Debug: força uso de sprites se disponíveis e recarrega com tamanho atual
        if hasattr(self.visualizer, 'idle_sprites') and self.visualizer.idle_sprites:
            # Limpa sprites antigos e recarrega
            self.visualizer.idle_sprites.clear()
            self.visualizer.run_sprites.clear()
            self.visualizer.load_idle_sprites()
            self.visualizer.load_run_sprites()
            self.visualizer.use_sprites = True
            print(f"🎮 Debug: Sprites recarregados - {len(self.visualizer.idle_sprites)} idle + {len(self.visualizer.run_sprites)} run")
        self.player = Player("Explorador")
        self.current_level = 1
        self.world = None
        self.game_state = "menu"  # menu, playing, level_complete, game_over, game_final
        self.show_optimal_path = False
        self.clicked_nodes = set()
        
        # Sistema de progresso de estrelas
        self.stars_earned = {}  # {level: stars_earned}
        self.max_level = 20  # Total de níveis no jogo
        self.total_possible_stars = self.max_level * 3  # 3 estrelas por nível
        
        # Sistema de combate
        self.enemies_fought = 0  # Contador de inimigos enfrentados no nível atual
        self.load_star_progress()
        self.hovered_node = None  # Nó sobre o qual o mouse está
        self.mouse_pos = (0, 0)  # Posição atual do mouse
        self.last_move_time = 0  # Para controlar o debounce de movimento
        self.move_cooldown = 0.3  # Cooldown entre movimentos (em segundos)
        
        # Sistema de animação de movimento
        self.is_moving = False
        self.move_start_time = 0
        self.move_duration = 0.5  # Duração da animação em segundos
        self.move_from_node = None
        self.move_to_node = None
        
        # Sistema de confirmação de movimento
        self.pending_move = None
        self.move_confirmation_time = 0
        self.confirmation_timeout = 2.0  # Segundos para confirmar movimento
        
        # Sistema de combate
        self.combat_state = None  # None, "player_attack", "enemy_attack", "enemy_dead"
        self.combat_start_time = 0
        self.combat_duration = 1.0  # Duração do combate simultâneo em segundos
        self.combat_node = None
        self.combat_enemy_health = 100  # Vida do inimigo
        self.combat_turn = 0  # Turno atual do combate
        self.combat_max_turns = 4  # Máximo de turnos (2 do jogador + 2 do inimigo)
        self.dead_enemies = set()  # Inimigos mortos (para não redesenhar)
        
    def handle_events(self):
        """Gerencia os eventos do jogo"""
        # Atualizar posição do mouse constantemente
        self.mouse_pos = pygame.mouse.get_pos()
        
        # Gerenciar cursor do mouse baseado no hover
        self.update_cursor()
        
        # Atualizar animação de movimento
        if self.game_state == "playing":
            self.update_movement_animation()
            self.update_combat_animation()
        
        # Detectar combinações de teclas para movimento diagonal
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            self.handle_diagonal_movement(keys)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Processar eventos da UI moderna
            self.modern_ui.handle_event(event)
            
            # Cliques do mouse no menu
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "menu":
                action = self.menu_system.handle_click(event.pos)
                if action == "start":
                    self.start_level_with_transition(1)
                elif action == "exit":
                    return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.goto_menu_with_transition()
                    else:
                        return False
                
                # Menu
                if self.game_state == "menu":
                    if event.key == pygame.K_1:
                        self.start_level_with_transition(1)
                    elif event.key == pygame.K_2:
                        self.show_stats()
                    elif event.key == pygame.K_3:
                        return False
                
                # Durante o jogo
                if self.game_state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.show_optimal_path = not self.show_optimal_path
                    elif event.key == pygame.K_r:
                        # Reiniciar fase (consome uma vida)
                        self.restart_level()
                    elif event.key == pygame.K_t:
                        # Alternar modo do sprite (T = Toggle)
                        if hasattr(self.visualizer, 'idle_sprites') and self.visualizer.idle_sprites:
                            self.visualizer.use_sprites = not self.visualizer.use_sprites
                            mode = "Sprites" if self.visualizer.use_sprites else "Desenho Vetorial"
                            print(f"🎨 Modo alterado para: {mode}")
                        else:
                            print("⚠️ Nenhum sprite encontrado para alternar")
                    
                    # Controles WASD para movimentação individual (apenas se não há diagonal)
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        if not self.is_diagonal_pressed():
                            self.move_player_direction('up')
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if not self.is_diagonal_pressed():
                            self.move_player_direction('down')
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if not self.is_diagonal_pressed():
                            self.move_player_direction('left')
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if not self.is_diagonal_pressed():
                            self.move_player_direction('right')
                
                # Level completo
                if self.game_state == "level_complete":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_1:
                        # Avançar para próximo nível (se tiver pelo menos 2 estrelas)
                        if self.level_results["can_advance"]:
                            if self.current_level < 20:
                                self.start_level(self.current_level + 1)
                            else:
                                self.game_state = "menu"
                        else:
                            print("Voce precisa de pelo menos 2 estrelas para avancar!")
                    elif event.key == pygame.K_2 or event.key == pygame.K_r:
                        # Repetir nível para melhor pontuação
                        self.start_level(self.current_level)
                    elif event.key == pygame.K_3 or event.key == pygame.K_ESCAPE:
                        # Voltar ao menu
                        self.game_state = "menu"
                
                # Game Over
                if self.game_state == "game_over":
                    if event.key == pygame.K_1 or event.key == pygame.K_SPACE:
                        # Recomeçar do nível 1
                        self.player.reset_lives()
                        self.start_level(1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_ESCAPE:
                        # Voltar ao menu
                        self.player.reset_lives()
                        self.game_state = "menu"
                
                # Tela Final (jogo completo)
                if self.game_state == "game_final":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_1 or event.key == pygame.K_ESCAPE:
                        # Voltar ao menu principal
                        self.goto_menu_with_transition()
            
            # Cliques do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if self.game_state == "playing":
                    # Bloquear movimento durante combate
                    if hasattr(self, 'combat_state') and self.combat_state in ["simultaneous_attack", "enemy_dead"]:
                        print("⚡ Movimento bloqueado durante combate!")
                        return
                        
                    clicked_node = self.get_clicked_node(pos)
                    if clicked_node is not None:
                        # Verifica se é um movimento válido antes de tentar
                        current = self.player.current_node
                        print(f"🖱️ Clique detectado no nó {clicked_node} na posição {pos}")
                        if clicked_node in self.world.graph.neighbors(current):
                            print(f"✅ Movendo para no {clicked_node} via clique")
                        else:
                            print(f"❌ No {clicked_node} nao e vizinho de {current}! Vizinhos: {list(self.world.graph.neighbors(current))}")
                        # Cliques diretos sempre bypassam confirmação (usuário foi explícito)
                        self.handle_node_click(clicked_node, bypass_confirmation=True)
                    else:
                        # Clique não atingiu nenhum nó
                        print(f"❌ Clique na posição {pos} não atingiu nenhum nó válido")
                
                elif self.game_state == "menu":
                    if not self.handle_menu_click(pos):
                        return False  # Sair do jogo
                
                elif self.game_state == "level_complete":
                    self.handle_level_complete_click(pos)
                
                elif self.game_state == "player_dead":
                    self.handle_player_death_click(pos)
                
                elif self.game_state == "game_over":
                    self.handle_game_over_click(pos)
                
                elif self.game_state == "game_final":
                    self.handle_game_final_click(pos)
        
        return True
    
    def get_clicked_node(self, pos):
        """Verifica qual nó foi clicado com detecção aprimorada"""
        # Recalcula posições (mesmo código do visualizer)
        node_positions = self.visualizer._calculate_node_positions(self.world.graph)
        
        closest_node = None
        closest_distance = float('inf')
        
        # Encontra o nó mais próximo dentro do raio de clique
        for node, node_pos in node_positions.items():
            distance = math.sqrt((pos[0] - node_pos[0])**2 + (pos[1] - node_pos[1])**2)
            
            # Raio de detecção adaptativo baseado no tipo de nó
            detection_radius = 35  # Raio base aumentado
            if node == self.world.end_node:
                detection_radius = 40  # Nó de saída maior
            elif node in self.clicked_nodes:
                detection_radius = 30  # Nós visitados
            
            if distance < detection_radius and distance < closest_distance:
                closest_distance = distance
                closest_node = node
        
        return closest_node
    
    def handle_node_click(self, node, bypass_confirmation=False):
        """Gerencia o clique em um nó"""
        current = self.player.current_node
        
        # Verifica se já não estamos neste nó (evita movimentos duplicados)
        if node == current:
            return
        
        # Verifica se o nó é vizinho
        if node in self.world.graph.neighbors(current):
            print(f"✅ Movendo de {current} → {node}")
            
            # Verifica se precisa de confirmação para movimento ambíguo (apenas para cliques, não teclas)
            if not bypass_confirmation and self.needs_movement_confirmation(current, node):
                print(f"⚠️ Movimento ambíguo detectado, aguardando confirmação...")
                self.pending_move = (current, node)
                self.move_confirmation_time = time.time()
                return
            
            # Executa movimento com animação
            self.execute_movement(current, node)
            self.clicked_nodes.add(node)
            print(f"🚶 Iniciando movimento para nó {node}, meta é {self.world.end_node}")
        else:
            print(f"O no {node} nao e vizinho de {current}!")
    
    def handle_diagonal_movement(self, keys):
        """Detecta e processa movimento diagonal usando combinações de teclas"""
        import time
        
        # Verifica cooldown para evitar movimentos repetidos
        current_time = time.time()
        if current_time - self.last_move_time < self.move_cooldown:
            return
        
        # Mapeia combinações de teclas para direções diagonais
        diagonal_movements = {
            # W + A = noroeste (up-left)
            (pygame.K_w, pygame.K_a): 'northwest',
            (pygame.K_UP, pygame.K_LEFT): 'northwest',
            
            # W + D = nordeste (up-right)  
            (pygame.K_w, pygame.K_d): 'northeast',
            (pygame.K_UP, pygame.K_RIGHT): 'northeast',
            
            # S + A = sudoeste (down-left)
            (pygame.K_s, pygame.K_a): 'southwest', 
            (pygame.K_DOWN, pygame.K_LEFT): 'southwest',
            
            # S + D = sudeste (down-right)
            (pygame.K_s, pygame.K_d): 'southeast',
            (pygame.K_DOWN, pygame.K_RIGHT): 'southeast'
        }
        
        # Verifica se alguma combinação está sendo pressionada
        for (key1, key2), direction in diagonal_movements.items():
            if keys[key1] and keys[key2]:
                self.move_player_diagonal_direction(direction)
                self.last_move_time = current_time  # Atualiza o tempo do último movimento
                return  # Para evitar múltiplos movimentos simultâneos
    
    def move_player_diagonal_direction(self, direction):
        """Move o jogador na direção diagonal especificada"""
        import time
        current_time = time.time()
        
        current = self.player.current_node
        neighbors = list(self.world.graph.neighbors(current))
        
        if not neighbors:
            return
        
        # Calcula posições dos nós
        node_positions = self.visualizer._calculate_node_positions(self.world.graph)
        current_pos = node_positions[current]
        
        # Vetores direcionais para diagonais
        diagonal_vectors = {
            'northwest': (-1, -1),   # Cima + Esquerda
            'northeast': (1, -1),    # Cima + Direita  
            'southwest': (-1, 1),    # Baixo + Esquerda
            'southeast': (1, 1)      # Baixo + Direita
        }
        
        if direction not in diagonal_vectors:
            return
            
        target_dx, target_dy = diagonal_vectors[direction]
        
        best_node = None
        best_score = -float('inf')
        
        for neighbor in neighbors:
            neighbor_pos = node_positions[neighbor]
            
            # Calcula vetor direção do current para neighbor
            dx = neighbor_pos[0] - current_pos[0]
            dy = neighbor_pos[1] - current_pos[1]
            
            # Normaliza o vetor (evita divisão por zero)
            distance = math.sqrt(dx*dx + dy*dy)
            if distance == 0:
                continue
                
            norm_dx = dx / distance
            norm_dy = dy / distance
            
            # Calcula o produto escalar com a direção diagonal desejada
            dot_product = norm_dx * target_dx + norm_dy * target_dy
            
            # Para diagonais, usamos um threshold menor (mais tolerante)
            if dot_product > 0.3:  # Aproximadamente 72 graus de tolerância
                # Score baseado na proximidade da direção e distância
                score = dot_product * 1000 - distance
                
                if score > best_score:
                    best_score = score
                    best_node = neighbor
        
        # Move para o nó encontrado
        if best_node is not None:
            direction_names = {
                'northwest': 'Noroeste ↖️ (W + A)',
                'northeast': 'Nordeste ↗️ (W + D)', 
                'southwest': 'Sudoeste ↙️ (S + A)',
                'southeast': 'Sudeste ↘️ (S + D)'
            }
            print(f"🎮 Movimento diagonal: {direction_names.get(direction, direction)} → Nó {best_node}")
            print(f"📍 Nó atual: {self.player.current_node}, Destino: {best_node}, Meta: {self.world.end_node}")
            
            self.handle_node_click(best_node, bypass_confirmation=True)
            self.last_move_time = current_time  # Atualiza o tempo do último movimento
        else:
            direction_names = {
                'northwest': 'Noroeste ↖️ (W + A)',
                'northeast': 'Nordeste ↗️ (W + D)',
                'southwest': 'Sudoeste ↙️ (S + A)', 
                'southeast': 'Sudeste ↘️ (S + D)'
            }
            print(f"❌ Nenhum nó disponível na direção {direction_names.get(direction, direction)}")
    
    def is_diagonal_pressed(self):
        """Verifica se alguma combinação diagonal está sendo pressionada"""
        keys = pygame.key.get_pressed()
        
        # Combinações diagonais
        diagonal_combinations = [
            (pygame.K_w, pygame.K_a), (pygame.K_UP, pygame.K_LEFT),      # Northwest
            (pygame.K_w, pygame.K_d), (pygame.K_UP, pygame.K_RIGHT),     # Northeast
            (pygame.K_s, pygame.K_a), (pygame.K_DOWN, pygame.K_LEFT),    # Southwest
            (pygame.K_s, pygame.K_d), (pygame.K_DOWN, pygame.K_RIGHT)    # Southeast
        ]
        
        for key1, key2 in diagonal_combinations:
            if keys[key1] and keys[key2]:
                return True
        return False
    
    def move_player_direction(self, direction):
        """Move o jogador na direção especificada (WASD) com lógica aprimorada"""
        import time
        
        # Verifica cooldown para evitar movimentos repetidos
        current_time = time.time()
        if current_time - self.last_move_time < self.move_cooldown:
            return
        
        current = self.player.current_node
        neighbors = list(self.world.graph.neighbors(current))
        
        if not neighbors:
            return
        
        # Calcula posições dos nós
        node_positions = self.visualizer._calculate_node_positions(self.world.graph)
        current_pos = node_positions[current]
        
        # Encontra o melhor vizinho na direção desejada
        best_node = None
        best_score = -1
        
        for neighbor in neighbors:
            neighbor_pos = node_positions[neighbor]
            
            # Calcula diferença de posição
            dx = neighbor_pos[0] - current_pos[0]
            dy = neighbor_pos[1] - current_pos[1]
            
            # Calcula distância total
            distance = math.sqrt(dx*dx + dy*dy)
            if distance == 0:
                continue
            
            # Normaliza os vetores de direção
            norm_dx = dx / distance
            norm_dy = dy / distance
            
            # Define vetores de direção desejados
            target_vectors = {
                'up': (0, -1),
                'down': (0, 1),
                'left': (-1, 0),
                'right': (1, 0)
            }
            
            if direction not in target_vectors:
                continue
                
            target_dx, target_dy = target_vectors[direction]
            
            # Calcula o produto escalar (coseno do ângulo)
            dot_product = norm_dx * target_dx + norm_dy * target_dy
            
            # Só considera nós que estão na direção correta (ângulo < 60 graus)
            if dot_product > 0.5:  # cos(60°) = 0.5
                # Score baseado na proximidade da direção e distância
                # Quanto maior o dot_product, mais alinhado com a direção
                # Quanto menor a distância, melhor
                score = dot_product * 1000 - distance
                
                if score > best_score:
                    best_score = score
                    best_node = neighbor
        
        # Move para o nó encontrado
        if best_node is not None:
            print(f"⌨️ Movendo para nó {best_node} via tecla {direction.upper()}")
            self.handle_node_click(best_node, bypass_confirmation=True)
            self.last_move_time = current_time  # Atualiza o tempo do último movimento
        else:
            print(f"Nenhum no encontrado na direcao {direction.upper()}!")
    
    def start_level(self, level_id):
        """Inicia um novo nível"""
        # Verifica se pode acessar o nível (exceto o nível 1)
        if level_id > 1:
            previous_level = level_id - 1
            if not self.player.can_advance_level(previous_level):
                print(f"⚠️  Você precisa de pelo menos 2 estrelas no nível {previous_level} para acessar o nível {level_id}!")
                return
        
        self.current_level = level_id
        self.world = World(level_id)
        self.player.reset_level(self.world.start_node)
        self.world.start_level()
        self.game_state = "playing"
        
        # Resetar contador de inimigos enfrentados
        self.enemies_fought = 0
        
        # Salvar checkpoint da fase atual (só após confirmar acesso)
        self.save_star_progress()
        self.show_optimal_path = False
        self.clicked_nodes = set()
        self.last_move_time = 0  # Reset do cooldown de movimento
    
    def restart_level(self):
        """Reinicia o nível atual (consome uma vida)"""
        if self.player.has_lives():
            self.player.lose_life()
            print(f"🔄 Reiniciando fase... Vidas restantes: {self.player.lives}")
            
            if self.player.has_lives():
                # Reinicia o nível atual
                self.start_level(self.current_level)
            else:
                # Game Over
                print("💀 GAME OVER - Sem vidas!")
                self.game_state = "game_over"
        else:
            print("Sem vidas para reiniciar!")
    
    def handle_level_complete_click(self, pos):
        """Gerencia cliques na tela de level complete com botões de imagem"""
        # Usar novo sistema de detecção de botões de imagem
        clicked_button = self.visualizer.handle_completion_button_click(pos)
        
        if clicked_button == "next_level":
            if self.level_results.get("can_advance", False):
                if self.current_level < 20:
                    self.start_level_with_transition(self.current_level + 1)
                else:
                    # Completou todos os níveis - ir para tela final
                    self.goto_final_screen_with_transition()
        elif clicked_button == "repeat_level":
            self.start_level_with_transition(self.current_level)
        elif clicked_button == "main_menu":
            self.goto_menu_with_transition()
    
    def handle_player_death_click(self, pos):
        """Gerencia cliques na tela de morte do jogador"""
        button_clicked = self.visualizer.handle_death_button_click(pos)
        
        if button_clicked == "retry_level":
            # Reiniciar o nível atual
            self.start_level_with_transition(self.current_level)
        elif button_clicked == "main_menu_death":
            # Voltar ao menu principal
            self.goto_menu_with_transition()
    
    def start_combat(self, enemy_node):
        """Inicia o sistema de combate - verifica vida do jogador"""
        self.combat_node = enemy_node
        self.combat_start_time = time.time()
        
        print(f"⚔️ Encontrou inimigo! Vida do jogador: {self.player.health}")
        print(f"🔢 Inimigos enfrentados anteriormente: {self.enemies_fought}")
        
        # Se já enfrentou um inimigo ou tem pouca vida, morre instantaneamente
        if self.enemies_fought >= 1 or self.player.health < 50:
            print("💀 Segundo inimigo ou vida baixa! Morte instantânea!")
            self.player.health = 0
            self.handle_player_death()
            return
        
        # Incrementar contador de inimigos enfrentados
        self.enemies_fought += 1
        
        # Iniciar combate simultâneo se jogador tem vida suficiente
        self.combat_enemy_health = 100
        self.combat_player_initial_health = self.player.health
        
        print(f"⚔️ COMBATE SIMULTÂNEO INICIADO!")
        print(f"🧙 Vida do jogador: {self.player.health}")
        print(f"👹 Vida do inimigo: {self.combat_enemy_health}")
        
        # Combate simultâneo - ambos atacam ao mesmo tempo
        self.combat_state = "simultaneous_attack"
    
    def handle_player_death(self):
        """Lida com a morte do jogador"""
        print("☠️ JOGADOR MORREU!")
        self.game_state = "player_dead"
        self.death_time = time.time()  # Para cronometrar a tela de morte
    
    def update_combat_animation(self):
        """Atualiza a animação de combate simultâneo"""
        if self.combat_state is None:
            return
            
        elapsed = time.time() - self.combat_start_time
        
        if elapsed >= self.combat_duration:
            if self.combat_state == "simultaneous_attack":
                # Combate simultâneo terminou - aplicar danos
                self._apply_combat_damage()
                self._resolve_combat()
                    
            # Estado enemy_dead removido - inimigos desaparecem imediatamente
                
    def _apply_combat_damage(self):
        """Aplica danos durante o combate simultâneo"""
        # Jogador sempre perde METADE da vida ao passar por vértice com inimigo
        player_damage = self.combat_player_initial_health // 2  # Metade da vida
        
        # Se jogador tem mais da metade da vida máxima, mata o inimigo
        if self.combat_player_initial_health > (self.player.max_health // 2):
            enemy_damage = 100  # Inimigo morre
            print(f"⚔️ Jogador tem {self.combat_player_initial_health} vida! Perde metade ({player_damage}) mas mata o inimigo!")
        else:
            # Jogador tem metade ou menos da vida máxima - morre
            player_damage = self.combat_player_initial_health  # Jogador morre
            enemy_damage = 50
            print(f"💀 Jogador tem apenas {self.combat_player_initial_health} vida! Não consegue derrotar o inimigo!")
        
        # Aplicar danos
        self.player.health = max(0, self.player.health - player_damage)
        self.combat_enemy_health = max(0, self.combat_enemy_health - enemy_damage)
        
        print(f"💥 Danos aplicados:")
        print(f"🧙 Jogador: {self.combat_player_initial_health} → {self.player.health} (-{player_damage})")
        print(f"👹 Inimigo: 100 → {self.combat_enemy_health} (-{enemy_damage})")
                
    def _resolve_combat(self):
        """Resolve o resultado final do combate"""
        print(f"🎯 Resolvendo combate - Vida restante: {self.player.health}")
        
        # Determinar vencedor baseado em quem sobreviveu
        if self.combat_enemy_health <= 0 and self.player.health > 0:
            # Jogador venceu - inimigo desaparece imediatamente
            print("🏆 VITÓRIA! Jogador derrotou o inimigo!")
            self.dead_enemies.add(self.combat_node)
            print(f"🗡️ Removendo inimigo do nó {self.combat_node}...")
            self.world.remove_enemy(self.combat_node)
            print(f"📋 Inimigos restantes: {list(self.world.enemies)}")
            # Finalizar combate imediatamente - sem animação de morte
            self.combat_state = None
            self.combat_node = None
            print("✅ Combate finalizado - inimigo removido!")
            
        elif self.player.health <= 0:
            # Jogador morreu
            print("💀 DERROTA! Jogador foi derrotado!")
            self.player.lives -= 1
            
            if self.player.lives <= 0:
                print("☠️ Game Over - Todas as vidas perdidas!")
                self.combat_state = None
                self.handle_game_over()
            else:
                print(f"💔 Vida perdida! Vidas restantes: {self.player.lives}")
                # Resetar jogador para posição inicial do nível
                self.player.current_node = self.world.start_node
                self.player.health = self.player.max_health  # Restaurar vida
                self.combat_state = None
                self.combat_node = None
        
        elif self.combat_enemy_health <= 0:
            # Ambos morreram, mas inimigo morreu primeiro
            print("🏆 Vitória por pouco! Ambos feridos, mas inimigo caiu primeiro!")
            self.dead_enemies.add(self.combat_node)
            print(f"🗡️ Removendo inimigo do nó {self.combat_node}...")
            self.world.remove_enemy(self.combat_node)
            print(f"📋 Inimigos restantes: {list(self.world.enemies)}")
            # Finalizar combate imediatamente
            self.combat_state = None
            self.combat_node = None
            
        else:
            # Ambos sobreviveram ou inimigo venceu - jogador deve morrer ou fugir
            if self.combat_enemy_health > 0:
                print("💀 Inimigo ainda vivo! Jogador foi derrotado!")
                self.player.health = 0  # Forçar morte do jogador
                self.player.lives -= 1
                
                if self.player.lives <= 0:
                    print("☠️ Game Over - Todas as vidas perdidas!")
                    self.combat_state = None
                    self.handle_game_over()
                else:
                    print(f"💔 Vida perdida! Vidas restantes: {self.player.lives}")
                    # Resetar jogador para posição inicial do nível
                    self.player.current_node = self.world.start_node
                    self.player.health = self.player.max_health
                    self.combat_state = None
                    self.combat_node = None
            else:
                # Caso impossível, mas tratando como empate
                print("🤝 Situação inesperada resolvida.")
                self.combat_state = None
                self.combat_node = None
    
    def handle_game_over(self):
        """Gerencia quando o jogador morre"""
        print("💀 Game Over - Transicionando para tela de fim de jogo...")
        self.goto_game_over_with_transition()
    
    def handle_game_over_click(self, pos):
        """Gerencia cliques na tela de game over"""
        # Coordenadas dos botões
        button_width = 300
        button_height = 50
        button_x = self.visualizer.width // 2 - 150
        
        # Botão 1: Recomeçar (y = 420)
        if button_x <= pos[0] <= button_x + button_width and 420 <= pos[1] <= 420 + button_height:
            self.player.reset_lives()
            self.start_level_with_transition(1)
        
        # Botão 2: Menu (y = 490)
        elif button_x <= pos[0] <= button_x + button_width and 490 <= pos[1] <= 490 + button_height:
            self.player.reset_lives()
            self.goto_menu_with_transition()
    
    def handle_game_final_click(self, pos):
        """Gerencia cliques na tela de jogo completo"""
        button_clicked = self.visualizer.handle_final_button_click(pos)
        
        if button_clicked == "main_menu_final":
            self.goto_menu_with_transition()
    
    def handle_menu_click(self, pos):
        """Gerencia cliques no menu principal com botões de imagem"""
        button_clicked = self.visualizer.handle_menu_button_click(pos)
        
        if button_clicked == 'newgame':
            self.start_level_with_transition(1)
        elif button_clicked == 'continue':
            # Usar o checkpoint salvo (current_level já foi validado ao carregar)
            if self.current_level > 0:
                self.start_level_with_transition(self.current_level)
        elif button_clicked == 'exit':
            return False  # Indica para sair do jogo
            
        return True  # Continuar no jogo
    
    def needs_movement_confirmation(self, current_node, target_node):
        """Verifica se o movimento precisa de confirmação"""
        if not hasattr(self.world.graph, 'nodes'):
            return False
            
        # Obtém posições dos nós
        node_positions = self.visualizer._calculate_node_positions(self.world.graph)
        current_pos = node_positions.get(current_node)
        target_pos = node_positions.get(target_node)
        
        if not current_pos or not target_pos:
            return False
        
        # Calcula direção do movimento desejado
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        
        # Normaliza a direção
        import math
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return False
            
        target_dir_x = dx / length
        target_dir_y = dy / length
        
        # Verifica vizinhos disponíveis
        neighbors = list(self.world.graph.neighbors(current_node))
        if len(neighbors) <= 2:  # Só uma opção além do destino
            return False
            
        # Conta quantas opções significativamente diferentes existem
        different_directions = 0
        
        for neighbor in neighbors:
            if neighbor == target_node:
                continue
                
            neighbor_pos = node_positions.get(neighbor)
            if not neighbor_pos:
                continue
                
            # Direção para este vizinho
            ndx = neighbor_pos[0] - current_pos[0]
            ndy = neighbor_pos[1] - current_pos[1]
            nlength = math.sqrt(ndx*ndx + ndy*ndy)
            
            if nlength == 0:
                continue
                
            neighbor_dir_x = ndx / nlength
            neighbor_dir_y = ndy / nlength
            
            # Calcula similaridade (produto escalar)
            dot_product = target_dir_x * neighbor_dir_x + target_dir_y * neighbor_dir_y
            
            # Se a direção é muito diferente (não é direção oposta)
            if dot_product > -0.7:  # Não é direção contrária
                different_directions += 1
        
        # Precisa confirmação se há múltiplas opções
        return different_directions > 0
    
    def execute_movement(self, from_node, to_node):
        """Executa o movimento com animação"""
        self.is_moving = True
        self.move_start_time = time.time()
        self.move_from_node = from_node
        self.move_to_node = to_node
    
    def update_movement_animation(self):
        """Atualiza a animação de movimento"""
        if not self.is_moving:
            # Verifica timeout de confirmação
            if self.pending_move and time.time() - self.move_confirmation_time > self.confirmation_timeout:
                self.pending_move = None
            return
            
        current_time = time.time()
        elapsed = current_time - self.move_start_time
        
        if elapsed >= self.move_duration:
            # Animação completa
            self.player.move_to_node(self.move_to_node)
            self.is_moving = False
            
            # Verifica se há inimigo no nó de destino
            if self.world.has_enemy(self.move_to_node):
                print(f"⚔️ Encontrou um inimigo no nó {self.move_to_node}!")
                self.start_combat(self.move_to_node)
                return
            
            # Verifica se chegou ao destino
            if self.move_to_node == self.world.end_node:
                print(f"🎉 VITÓRIA! Chegou ao nó final {self.move_to_node}! Estado atual: {self.game_state}")
                print(f"🛤️ Caminho percorrido: {self.player.path_taken}")
                
                # Tocar som de vitória
                self.visualizer.play_victory_sound()
                
                if self.game_state == "playing":  # Só completa se ainda estiver jogando
                    self.complete_level()
                else:
                    print(f"⚠️ Tentativa de completar nível mas jogo não está no estado 'playing': {self.game_state}")
    
    def get_animated_player_position(self):
        """Retorna a posição animada do jogador durante o movimento"""
        if not self.is_moving:
            return None
            
        # Calcula interpolação
        elapsed = time.time() - self.move_start_time
        progress = min(1.0, elapsed / self.move_duration)
        
        # Easing function (suaviza a animação)
        import math
        eased_progress = 1 - math.cos(progress * math.pi / 2)  # Ease-out
        
        # Obtém posições dos nós
        node_positions = self.visualizer._calculate_node_positions(self.world.graph)
        from_pos = node_positions.get(self.move_from_node)
        to_pos = node_positions.get(self.move_to_node)
        
        if not from_pos or not to_pos:
            return None
            
        # Interpola posição
        x = from_pos[0] + (to_pos[0] - from_pos[0]) * eased_progress
        y = from_pos[1] + (to_pos[1] - from_pos[1]) * eased_progress
        
        return (x, y)
    
    def get_movement_direction(self):
        """Calcula a direção do movimento atual (left, right, up, down, ou None)"""
        if not self.is_moving:
            return None
            
        # Obtém posições dos nós
        node_positions = self.visualizer._calculate_node_positions(self.world.graph)
        from_pos = node_positions.get(self.move_from_node)
        to_pos = node_positions.get(self.move_to_node)
        
        if not from_pos or not to_pos:
            return None
            
        # Calcula diferenças
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        
        # Determina direção principal (horizontal vs vertical)
        if abs(dx) > abs(dy):
            # Movimento horizontal é dominante
            if dx > 0:
                return "right"
            else:
                return "left"
        else:
            # Movimento vertical é dominante
            if dy > 0:
                return "down"
            else:
                return "up"
    
    def update_cursor(self):
        """Atualiza o cursor do mouse baseado no hover dos botões"""
        if hasattr(self.visualizer, 'hovered_button') and self.visualizer.hovered_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def complete_level(self):
        """Completa o nível atual"""
        print(f"COMPLETE_LEVEL chamado! Estado: {self.game_state}")
        print(f"Posicao atual do jogador: {self.player.current_node}")
        print(f"No final: {self.world.end_node}")
        
        results = self.world.complete_level(self.player.path_taken)
        
        # Calcula estrelas baseado na eficiência
        efficiency = results.get("efficiency", 0)
        stars = self.player.calculate_stars(efficiency)
        
        # Debug: mostra os valores calculados
        print(f"Debug - Eficiencia: {efficiency:.3f} ({efficiency*100:.1f}%) | Estrelas: {stars}")
        
        # Atualiza as estrelas do jogador para este nível
        self.player.update_level_stars(self.current_level, stars)
        
        # Salvar progresso de estrelas
        current_stars = self.stars_earned.get(self.current_level, 0)
        if stars > current_stars:
            self.stars_earned[self.current_level] = stars
            self.save_star_progress()
            print(f"⭐ Novo recorde de estrelas no nível {self.current_level}: {stars} estrelas!")
        
        # Adiciona informações de estrelas aos resultados
        results["stars_earned"] = stars
        results["previous_stars"] = self.player.level_stars.get(self.current_level, 0)
        results["can_advance"] = stars >= 2
        results["level_id"] = self.current_level
        
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
        # Atualizar UI moderna
        dt = pygame.time.get_ticks() * 0.001  # Converter para segundos
        self.modern_ui.update(dt)
        
        # Atualizar vídeo de fundo se estivermos no menu
        if self.game_state == "menu":
            self.update_video_background()
        
        # Atualizar transições
        self.visualizer.update_transition()
        
        # Atualiza animação de movimento se estiver ativa
        if self.is_moving:
            self.update_movement_animation()
        
        # Detectar hover apenas durante o jogo
        if self.game_state == "playing" and self.world:
            self.detect_hovered_node()
    
    def detect_hovered_node(self):
        """Detecta qual nó está sendo 'hovered' pelo mouse"""
        self.hovered_node = None
        # Usa o método do visualizer para calcular posições
        node_positions = self.visualizer._calculate_node_positions(self.world.graph)
        
        for node_id, pos in node_positions.items():
            distance = math.sqrt((self.mouse_pos[0] - pos[0])**2 + (self.mouse_pos[1] - pos[1])**2)
            
            # Raio de detecção adaptativo (mesmo que clique)
            detection_radius = 35
            if node_id == self.world.end_node:
                detection_radius = 40
            elif node_id in self.clicked_nodes:
                detection_radius = 30
            
            if distance <= detection_radius:
                self.hovered_node = node_id
                break
    
    def draw(self):
        """Desenha o estado atual"""
        if self.game_state == "menu":
            # Desenhar vídeo de fundo primeiro
            self.draw_video_background()
            # Depois desenhar o menu por cima
            levels_completed = self.current_level - 1
            self.visualizer.draw_menu(levels_completed, self.player)
            # Desenhar contador de estrelas
            self.draw_star_counter()
        
        elif self.game_state == "playing":
            # Obtém posição animada e direção do jogador se estiver se movendo
            animated_pos = self.get_animated_player_position() if self.is_moving else None
            movement_direction = self.get_movement_direction() if self.is_moving else None
            # Armazena direção no visualizer para uso na função de desenho
            if hasattr(self.visualizer, 'current_movement_direction'):
                self.visualizer.current_movement_direction = movement_direction
            self.visualizer.draw_graph(self.world, self.player, self.clicked_nodes, self.show_optimal_path, self.hovered_node, animated_pos, self)
        
        elif self.game_state == "level_complete":
            self.visualizer.draw_level_complete(self.level_results)
        
        elif self.game_state == "player_dead":
            self.visualizer.draw_player_death()
        
        elif self.game_state == "game_over":
            self.visualizer.draw_game_over(self.player)
        
        elif self.game_state == "game_final":
            self.visualizer.draw_game_final(self.get_final_stats())
        
        # Desenhar UI moderna por cima (temporariamente desabilitado)
        # self.modern_ui.draw(self.visualizer.screen)
        
        # Aplicar efeito de transição se ativo
        self.visualizer.apply_transition_effect()
        
        # Atualizar display apenas uma vez por frame
        pygame.display.flip()
    
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
        
        # Parar música de fundo antes de sair
        self.visualizer.stop_background_music()
        
        # Limpar recursos de vídeo
        if self.video_cap:
            self.video_cap.release()
        
        # Limpar vídeo final
        if hasattr(self.visualizer, 'final_video_cap') and self.visualizer.final_video_cap:
            self.visualizer.final_video_cap.release()
        
        pygame.quit()
        print("\n👋 Obrigado por jogar PathFinder Adventure!\n")
        sys.exit()
    
    # Métodos de transição
    def start_level_with_transition(self, level):
        """Inicia um nível com transição fade"""
        if not self.visualizer.is_transitioning:
            self.pending_level = level
            callback = lambda: self._execute_start_level(level)
            self.visualizer.start_fade_transition(callback)
    
    def goto_menu_with_transition(self):
        """Volta ao menu com transição fade"""
        if not self.visualizer.is_transitioning:
            callback = lambda: self._execute_goto_menu()
            self.visualizer.start_fade_transition(callback)
    
    def next_level_with_transition(self):
        """Avança para o próximo nível com transição"""
        if not self.visualizer.is_transitioning:
            callback = lambda: self._execute_next_level()
            self.visualizer.start_fade_transition(callback)
    
    def goto_game_over_with_transition(self):
        """Vai para game over com transição fade"""
        if not self.visualizer.is_transitioning:
            callback = lambda: self._execute_goto_game_over()
            self.visualizer.start_fade_transition(callback)
    
    def goto_final_screen_with_transition(self):
        """Vai para tela final com transição fade"""
        if not self.visualizer.is_transitioning:
            callback = lambda: self._execute_goto_final_screen()
            self.visualizer.start_fade_transition(callback)
    
    def _execute_start_level(self, level):
        """Executa o início do nível após transição"""
        self.start_level(level)
    
    def _execute_goto_menu(self):
        """Executa volta ao menu após transição"""
        self.game_state = "menu"
        self.clicked_nodes = set()
    
    def _execute_next_level(self):
        """Executa avanço de nível após transição"""
        self.current_level += 1
        if self.current_level > 20:
            print("🎉 PARABÉNS! Você completou todos os níveis!")
            self.game_state = "menu"
        else:
            self.start_level(self.current_level)
            # Salvar progresso após avançar de nível
            self.save_star_progress()
    
    def _execute_goto_game_over(self):
        """Executa ida para game over após transição"""
        self.game_state = "game_over"
        self.clicked_nodes = set()
    
    def _execute_goto_final_screen(self):
        """Executa ida para tela final após transição"""
        self.game_state = "game_final"
        self.clicked_nodes = set()
        print("🎉 PARABÉNS! Você completou todos os 20 níveis!")
    
    def load_video_background(self):
        """Carrega o vídeo de fundo para o menu"""
        try:
            import os
            video_path = "videos/Math.mp4"
            if os.path.exists(video_path):
                self.video_cap = cv2.VideoCapture(video_path)
                print(f"🎥 Vídeo background carregado: {video_path}")
                
                # Configurar loop do vídeo
                self.video_frame_count = int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.video_fps = self.video_cap.get(cv2.CAP_PROP_FPS)
                self.video_current_frame = 0
                
                print(f"🎬 Vídeo: {self.video_frame_count} frames, {self.video_fps} FPS")
            else:
                print(f"⚠️ Vídeo não encontrado: {video_path}")
                self.video_cap = None
        except Exception as e:
            print(f"❌ Erro ao carregar vídeo: {e}")
            self.video_cap = None
    
    def load_star_progress(self):
        """Carrega o progresso de estrelas do arquivo"""
        try:
            import json
            import os
            
            save_file = "star_progress.json"
            if os.path.exists(save_file):
                with open(save_file, 'r') as f:
                    data = json.load(f)
                    self.stars_earned = {int(k): v for k, v in data.get('stars_earned', {}).items()}
                    saved_level = data.get('current_level', 1)
                    
                    # Calcular o maior nível acessível baseado nas estrelas
                    highest_accessible = self.get_highest_accessible_level()
                    
                    # Usar o menor entre: nível salvo ou maior acessível
                    # Isso garante que não tente acessar nível sem estrelas suficientes
                    self.current_level = min(saved_level, highest_accessible)
                        
                print(f"⭐ Progresso carregado: {self.get_total_stars_earned()}/{self.total_possible_stars} estrelas")
                print(f"📍 Checkpoint: Nível {self.current_level}")
            else:
                print("🎮 Novo jogo - progresso zerado")
        except Exception as e:
            print(f"⚠️ Erro ao carregar progresso: {e}")
            self.stars_earned = {}
    
    def save_star_progress(self):
        """Salva o progresso de estrelas no arquivo"""
        try:
            import json
            
            data = {
                'stars_earned': self.stars_earned,
                'current_level': self.current_level
            }
            
            with open("star_progress.json", 'w') as f:
                json.dump(data, f)
            print(f"💾 Progresso salvo: {self.get_total_stars_earned()}/{self.total_possible_stars} estrelas")
        except Exception as e:
            print(f"⚠️ Erro ao salvar progresso: {e}")
    
    def get_total_stars_earned(self):
        """Retorna o total de estrelas conquistadas"""
        return sum(self.stars_earned.values())
    
    def get_final_stats(self):
        """Calcula as estatísticas finais médias para exibir na tela final"""
        total_stars = self.get_total_stars_earned()
        levels_completed = len(self.stars_earned)
        
        # Calcular médias
        avg_stars_per_level = total_stars / max(levels_completed, 1)
        efficiency_sum = 0
        efficiency_count = 0
        
        # Calcular eficiência média (aproximada baseada nas estrelas)
        for level_id, stars in self.stars_earned.items():
            if stars == 3:
                efficiency_sum += 95  # Aproximadamente 95% para 3 estrelas
            elif stars == 2:
                efficiency_sum += 87.5  # Aproximadamente 87.5% para 2 estrelas
            elif stars == 1:
                efficiency_sum += 70  # Aproximadamente 70% para 1 estrela
            efficiency_count += 1
        
        avg_efficiency = efficiency_sum / max(efficiency_count, 1)
        
        return {
            "total_stars": total_stars,
            "max_stars": self.total_possible_stars,
            "levels_completed": levels_completed,
            "avg_stars_per_level": avg_stars_per_level,
            "avg_efficiency": avg_efficiency,
            "player_level": self.player.level,
            "total_points": self.player.points,
            "total_experience": self.player.experience + (self.player.level - 1) * 100
        }
    
    def get_highest_accessible_level(self):
        """Encontra o nível mais alto que o jogador pode acessar"""
        # Sempre pode acessar o nível 1
        highest_level = 1
        
        # Verifica níveis de 2 a 20
        for level in range(2, 21):
            previous_level = level - 1
            stars_in_previous = self.stars_earned.get(previous_level, 0)
            # Verifica se tem pelo menos 2 estrelas no nível anterior
            if stars_in_previous >= 2:
                highest_level = level
            else:
                break  # Para no primeiro nível inacessível
                
        return highest_level

    def update_video_background(self):
        """Atualiza o frame do vídeo de fundo"""
        if self.video_cap is None:
            return
            
        try:
            ret, frame = self.video_cap.read()
            if not ret:
                # Reiniciar vídeo quando chegar ao final
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.video_cap.read()
            
            if ret:
                # Converter BGR (OpenCV) para RGB (Pygame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Redimensionar para o tamanho da tela
                frame = cv2.resize(frame, (self.visualizer.width, self.visualizer.height))
                # Converter para superficie pygame
                self.video_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                
        except Exception as e:
            print(f"❌ Erro ao atualizar vídeo: {e}")
    
    def draw_star_counter(self):
        """Desenha o contador de estrelas no menu principal"""
        total_stars = self.get_total_stars_earned()
        
        # Posição no canto superior direito
        star_x = self.visualizer.width - 200
        star_y = 30
        
        # Fundo do contador
        counter_width = 180
        counter_height = 60
        counter_rect = pygame.Rect(star_x - 10, star_y - 10, counter_width, counter_height)
        
        # Desenhar fundo com transparencia
        counter_surf = pygame.Surface((counter_width, counter_height), pygame.SRCALPHA)
        pygame.draw.rect(counter_surf, (40, 5, 15, 180), (0, 0, counter_width, counter_height), border_radius=15)
        pygame.draw.rect(counter_surf, (255, 215, 0, 200), (0, 0, counter_width, counter_height), width=3, border_radius=15)
        self.visualizer.screen.blit(counter_surf, (star_x - 10, star_y - 10))
        
        # Ícone de estrela
        star_size = 30
        star_points = self._get_star_points(star_x + 20, star_y + 20, star_size//2)
        pygame.draw.polygon(self.visualizer.screen, (255, 215, 0), star_points)
        pygame.draw.polygon(self.visualizer.screen, (255, 255, 100), star_points, 2)
        
        # Texto do contador
        font = self.visualizer.font_large
        counter_text = f"{total_stars}/{self.total_possible_stars}"
        text_surface = font.render(counter_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(star_x + 90, star_y + 20))
        self.visualizer.screen.blit(text_surface, text_rect)
        
        # Texto "Estrelas" removido
    
    def _get_star_points(self, cx, cy, radius):
        """Retorna os pontos para desenhar uma estrela de 5 pontas"""
        import math
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                r = radius
            else:
                r = radius * 0.4
            x = cx + r * math.cos(angle - math.pi/2)
            y = cy + r * math.sin(angle - math.pi/2)
            points.append((x, y))
        return points

    def draw_video_background(self):
        """Desenha o vídeo de fundo sem overlay"""
        if self.video_frame:
            self.visualizer.screen.blit(self.video_frame, (0, 0))
        else:
            # Fallback: usar fundo ninja quando vídeo não está disponível
            self.visualizer.draw_ninja_background()

if __name__ == "__main__":
    game = Game()
    game.run()
