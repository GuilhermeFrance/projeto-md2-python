"""
Sistema de UI moderna ninja
Implementa interfaces elegantes e responsivas para o jogo ninja
"""

import pygame
import math

class ModernNinjaUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Cores ninja modernas
        self.colors = {
            'bg_primary': (34, 34, 42),      # Fundo escuro ninja
            'bg_secondary': (45, 45, 56),     # Fundo cards
            'accent_gold': (245, 203, 105),   # Dourado ninja
            'accent_red': (79, 5, 25),        # Vermelho escuro
            'text_primary': (255, 255, 255),  # Texto principal
            'text_secondary': (200, 200, 200), # Texto secundário
            'shadow': (0, 0, 0, 100),         # Sombras
            'glow_gold': (245, 203, 105, 80), # Brilho dourado
            'ninja_steel': (108, 122, 137),   # Aço ninja
        }
        
        # Elementos da UI
        self.elements = {}
        self.particles = []
        self.animations = {}
        

    
    def create_glass_effect(self, surface, rect, alpha=150):
        """Cria efeito de vidro fosco ninja"""
        glass_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        # Gradiente de vidro
        for y in range(rect.height):
            alpha_val = alpha - (y * alpha // rect.height // 3)
            color = (*self.colors['bg_secondary'], alpha_val)
            pygame.draw.line(glass_surface, color, (0, y), (rect.width, y))
        
        # Borda brilhante
        pygame.draw.rect(glass_surface, (*self.colors['accent_gold'], 100), 
                        glass_surface.get_rect(), 2)
        
        surface.blit(glass_surface, rect)
        
    def create_ninja_particle_system(self, surface, center, count=20):
        """Sistema de partículas ninja (estrelas ninja, fumaça)"""
        current_time = pygame.time.get_ticks()
        
        # Adicionar novas partículas
        if len(self.particles) < count:
            for _ in range(3):
                import random
                particle = {
                    'x': center[0] + (math.cos(current_time * 0.001) * 50),
                    'y': center[1] + (math.sin(current_time * 0.001) * 50),
                    'vx': (random.random() - 0.5) * 2,
                    'vy': (random.random() - 0.5) * 2,
                    'life': 255,
                    'type': 'ninja_star' if random.random() > 0.7 else 'smoke'
                }
                self.particles.append(particle)
        
        # Atualizar e desenhar partículas
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 3
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                continue
                
            alpha = max(0, particle['life'])
            
            if particle['type'] == 'ninja_star':
                # Desenhar estrela ninja
                points = []
                for i in range(8):
                    angle = i * math.pi / 4
                    radius = 3 if i % 2 == 0 else 1.5
                    px = particle['x'] + math.cos(angle) * radius
                    py = particle['y'] + math.sin(angle) * radius
                    points.append((px, py))
                
                star_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.polygon(star_surface, (*self.colors['accent_gold'], alpha), 
                                  [(p[0]-particle['x']+10, p[1]-particle['y']+10) for p in points])
                surface.blit(star_surface, (particle['x']-10, particle['y']-10))
            else:
                # Desenhar fumaça
                smoke_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
                pygame.draw.circle(smoke_surface, (*self.colors['ninja_steel'], alpha//2), 
                                 (5, 5), 5)
                surface.blit(smoke_surface, (particle['x']-5, particle['y']-5))
    
    def draw_ninja_border(self, surface, rect, thickness=3):
        """Desenha borda ninja com efeitos especiais"""
        # Sombra externa
        shadow_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width, rect.height)
        pygame.draw.rect(surface, (*self.colors['shadow'][:3], 100), shadow_rect, thickness)
        
        # Borda principal dourada
        pygame.draw.rect(surface, self.colors['accent_gold'], rect, thickness)
        
        # Brilho interno
        inner_rect = pygame.Rect(rect.x + thickness, rect.y + thickness, 
                               rect.width - thickness*2, rect.height - thickness*2)
        pygame.draw.rect(surface, (*self.colors['glow_gold'][:3], 50), inner_rect, 1)
        
    def create_animated_button(self, rect, text, surface, hover=False):
        """Cria botão animado estilo ninja"""
        # Animação de hover
        scale = 1.05 if hover else 1.0
        anim_rect = pygame.Rect(
            rect.centerx - (rect.width * scale) // 2,
            rect.centery - (rect.height * scale) // 2,
            rect.width * scale,
            rect.height * scale
        )
        
        # Fundo do botão com gradiente
        button_surface = pygame.Surface((anim_rect.width, anim_rect.height), pygame.SRCALPHA)
        
        # Gradiente ninja
        for y in range(anim_rect.height):
            ratio = y / anim_rect.height
            if hover:
                color = self._blend_colors(self.colors['accent_red'], self.colors['accent_gold'], ratio * 0.3)
            else:
                color = self._blend_colors(self.colors['accent_red'], (self.colors['accent_red'][0] + 20, 
                                         self.colors['accent_red'][1] + 5, self.colors['accent_red'][2] + 10), ratio)
            pygame.draw.line(button_surface, color, (0, y), (anim_rect.width, y))
        
        surface.blit(button_surface, anim_rect)
        
        # Borda ninja
        self.draw_ninja_border(surface, anim_rect)
        
        # Texto com sombra
        font = pygame.font.Font(None, 24)
        text_shadow = font.render(text, True, (0, 0, 0))
        text_surface = font.render(text, True, self.colors['text_primary'])
        
        text_rect = text_surface.get_rect(center=anim_rect.center)
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        
        surface.blit(text_shadow, shadow_rect)
        surface.blit(text_surface, text_rect)
        
        return anim_rect
        
    def _blend_colors(self, color1, color2, ratio):
        """Mistura duas cores com base na proporção"""
        return (
            int(color1[0] + (color2[0] - color1[0]) * ratio),
            int(color1[1] + (color2[1] - color1[1]) * ratio),
            int(color1[2] + (color2[2] - color1[2]) * ratio)
        )
    
    def create_info_panel(self, surface, rect, title, info_dict):
        """Cria painel de informações ninja moderno"""
        # Fundo com efeito de vidro
        self.create_glass_effect(surface, rect)
        
        # Título
        font_title = pygame.font.Font(None, 28)
        title_surface = font_title.render(title, True, self.colors['accent_gold'])
        title_rect = title_surface.get_rect(centerx=rect.centerx, y=rect.y + 15)
        surface.blit(title_surface, title_rect)
        
        # Informações
        font_info = pygame.font.Font(None, 20)
        y_offset = title_rect.bottom + 20
        
        for key, value in info_dict.items():
            info_text = f"{key}: {value}"
            info_surface = font_info.render(info_text, True, self.colors['text_primary'])
            info_rect = info_surface.get_rect(x=rect.x + 15, y=y_offset)
            surface.blit(info_surface, info_rect)
            y_offset += 25
            
        # Partículas ninja no painel
        self.create_ninja_particle_system(surface, rect.center, 5)
    
    def create_progress_bar(self, surface, rect, progress, max_value, color=None):
        """Barra de progresso ninja animada"""
        if color is None:
            color = self.colors['accent_gold']
            
        # Fundo da barra
        bg_rect = rect.copy()
        pygame.draw.rect(surface, self.colors['bg_secondary'], bg_rect)
        pygame.draw.rect(surface, self.colors['ninja_steel'], bg_rect, 2)
        
        # Progresso
        progress_ratio = min(progress / max_value, 1.0)
        progress_width = int(rect.width * progress_ratio)
        
        if progress_width > 0:
            progress_rect = pygame.Rect(rect.x, rect.y, progress_width, rect.height)
            
            # Gradiente na barra de progresso
            for x in range(progress_width):
                ratio = x / progress_width if progress_width > 0 else 0
                bar_color = self._blend_colors(color, 
                                             (min(255, color[0] + 50), min(255, color[1] + 50), color[2]), 
                                             ratio)
                pygame.draw.line(surface, bar_color, 
                               (rect.x + x, rect.y), (rect.x + x, rect.y + rect.height))
            
            # Brilho na barra
            glow_rect = progress_rect.copy()
            glow_rect.height = 3
            pygame.draw.rect(surface, (255, 255, 255, 150), glow_rect)
    
    def update(self, dt):
        """Atualiza animações e efeitos"""
        # Atualizar animações de elementos
        for element_id, animation in self.animations.items():
            if 'pulse' in animation:
                animation['pulse'] += dt * 3
                
    def handle_event(self, event):
        """Processa eventos da UI"""
        return False
    
    def draw(self, surface):
        """Desenha todos os elementos da UI"""
        pass

class NinjaMenuSystem:
    """Sistema de menus ninja aprimorado"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ui = ModernNinjaUI(width, height)
        self.current_menu = "main"
        self.buttons = {}
        self.animations = {}
        
    def create_main_menu(self, surface):
        """Menu principal ninja"""
        # Fundo com gradiente ninja
        self._draw_ninja_background(surface)
        
        # Título principal
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("NINJA PATHFINDER", True, self.ui.colors['accent_gold'])
        title_rect = title.get_rect(center=(self.width // 2, 120))
        
        # Sombra do título
        shadow = title_font.render("NINJA PATHFINDER", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(title_rect.centerx + 3, title_rect.centery + 3))
        surface.blit(shadow, shadow_rect)
        surface.blit(title, title_rect)
        
        # Subtítulo
        subtitle_font = pygame.font.Font(None, 24)
        subtitle = subtitle_font.render("Master the Art of Pathfinding", True, self.ui.colors['text_secondary'])
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, title_rect.bottom + 20))
        surface.blit(subtitle, subtitle_rect)
        
        # Botões principais
        button_width = 300
        button_height = 60
        button_spacing = 20
        start_y = 250
        
        buttons_data = [
            ("START GAME", "start"),
            ("LEVEL SELECT", "levels"),
            ("SETTINGS", "settings"),
            ("EXIT", "exit")
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (text, action) in enumerate(buttons_data):
            button_rect = pygame.Rect(
                (self.width - button_width) // 2,
                start_y + i * (button_height + button_spacing),
                button_width,
                button_height
            )
            
            hover = button_rect.collidepoint(mouse_pos)
            self.ui.create_animated_button(button_rect, text, surface, hover)
            self.buttons[action] = button_rect
        
        # Efeitos de partículas
        self.ui.create_ninja_particle_system(surface, (self.width // 2, self.height // 2), 30)
        
    def _draw_ninja_background(self, surface):
        """Desenha fundo ninja com efeitos"""
        # Gradiente de fundo
        for y in range(self.height):
            ratio = y / self.height
            color = self.ui._blend_colors(
                self.ui.colors['bg_primary'],
                (self.ui.colors['bg_primary'][0] + 15, 
                 self.ui.colors['bg_primary'][1] + 15, 
                 self.ui.colors['bg_primary'][2] + 20),
                ratio
            )
            pygame.draw.line(surface, color, (0, y), (self.width, y))
        
        # Padrão ninja sutil
        current_time = pygame.time.get_ticks()
        for i in range(0, self.width, 100):
            for j in range(0, self.height, 100):
                import random
                alpha = int(30 + 20 * math.sin(current_time * 0.001 + i * 0.01 + j * 0.01))
                ninja_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.circle(ninja_surface, (*self.ui.colors['accent_gold'], alpha), (25, 25), 25, 2)
                surface.blit(ninja_surface, (i, j))
    
    def handle_click(self, pos):
        """Processa cliques nos botões"""
        for action, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return action
        return None