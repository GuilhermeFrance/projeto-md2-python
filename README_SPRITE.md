# 🎨 Como Usar Sprites PNG para o Personagem

## 📁 Preparação do Sprite

1. **Crie ou encontre uma imagem PNG**
   - Tamanho recomendado: 64x64 pixels
   - Fundo transparente (para melhor visual)
   - Formato: PNG com canal alpha

2. **Salve com um destes nomes na pasta do projeto:**
   - `player_sprite.png` (preferido)
   - `player.png`
   - `character.png`
   - `boneco.png`
   - `sprites/player.png`
   - `assets/player.png`

## 🎮 Controles no Jogo

- **Tecla T**: Alternar entre sprite PNG e desenho vetorial
- **Tecla SPACE**: Mostrar/ocultar caminho ótimo
- **Tecla R**: Reiniciar nível

## 🛠️ Recursos do Sistema de Sprites

### Efeitos Automáticos:
- ✨ Brilho pulsante ao redor do sprite
- 🔄 Rotação sutil baseada na animação
- 📏 Pulsação de tamanho quando animado
- 🎯 Centralização automática no nó

### Configurações Ajustáveis:
```python
# No visualizer.py, função __init__
self.sprite_size = (40, 40)  # Tamanho do sprite na tela

# Na função _draw_player_sprite
rotation_angle = math.sin(self.animation_time) * 5  # Rotação máxima
glow_radius = int(25 * self.player_pulse)  # Tamanho do brilho
```

## 🎨 Dicas de Design

### Para Sprites Personalizados:
1. **Faça o personagem olhando para frente**
2. **Use cores contrastantes**
3. **Mantenha detalhes simples** (será reduzido para 40x40)
4. **Teste com fundo transparente**

### Ferramentas Recomendadas:
- **GIMP** (gratuito)
- **Photoshop**
- **Paint.NET**
- **Aseprite** (para pixel art)

## 🔧 Personalização Avançada

### Mudar Tamanho do Sprite:
```python
self.sprite_size = (50, 50)  # Maior
self.sprite_size = (30, 30)  # Menor
```

### Desativar Efeitos:
```python
# Sem rotação
rotation_angle = 0

# Sem brilho
# Comentar a linha _draw_glow_circle()

# Sem pulsação de tamanho
# Remover o bloco if self.player_pulse > 1.2
```

### Sprite Animado (múltiplos frames):
Para sprites com animação, você pode:
1. Criar múltiplas imagens: `player_1.png`, `player_2.png`, etc.
2. Modificar o código para alternar entre frames
3. Usar sprite sheets (uma imagem com vários frames)

## 🚀 Exemplo de Implementação de Sprite Sheet

```python
def _load_sprite_sheet(self, file_path, frame_width, frame_height):
    """Carrega um sprite sheet e divide em frames"""
    sheet = pygame.image.load(file_path).convert_alpha()
    frames = []
    
    for y in range(0, sheet.get_height(), frame_height):
        for x in range(0, sheet.get_width(), frame_width):
            frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frames.append(pygame.transform.scale(frame, self.sprite_size))
    
    return frames
```

## ⚡ Fallback Automático

Se nenhum sprite for encontrado, o jogo automaticamente:
- ✅ Usa o desenho vetorial original
- 📝 Mostra mensagem informativa no console
- 🎮 Mantém todas as funcionalidades normais

---

**Dica**: Comece com um sprite simples para testar, depois evolua para versões mais elaboradas!