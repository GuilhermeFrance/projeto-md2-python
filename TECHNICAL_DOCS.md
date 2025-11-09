# 📚 Documentação Técnica - PathFinder Adventure

## Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────┐
│              MAIN.PY (Game Loop)                │
│  ┌─────────────┬──────────────┬────────────────┐
│  │             │              │                │
│  ▼             ▼              ▼                ▼
│ PLAYER      WORLD        VISUALIZER      INPUT HANDLER
│   │           │              │
│   ├─ Level    ├─ Graph       └─ Pygame
│   ├─ XP       ├─ Pathfinding
│   └─ Items    └─ Scoring
│
└─────────────────────────────────────────────────┘
```

## Arquivos Principais

### 1. **main.py** - Loop Principal
- Gerencia o estado do jogo (menu, playing, level_complete)
- Processa eventos de input
- Coordena entre Player, World e Visualizer
- Loop de atualização e renderização

### 2. **player.py** - Sistema de Personagem
```python
class Player:
    - name: str
    - health: int (atual/máximo)
    - experience: int
    - level: int
    - points: int
    - current_node: int
    - path_taken: list
    - items: list
```

**Métodos principais:**
- `move_to_node()` - Move o personagem
- `add_experience()` - Adiciona XP e verifica level up
- `add_points()` - Adiciona pontos
- `take_damage()` / `heal()` - Gerencia vida
- `reset_level()` - Reseta para novo nível

### 3. **world.py** - Gerenciamento de Níveis
```python
class World:
    - level_id: int
    - config: dict
    - graph: NetworkX Graph
    - start_node: int
    - end_node: int
    - optimal_path: list
    - optimal_distance: float
```

**Métodos principais:**
- `start_level()` - Inicia cronômetro
- `complete_level()` - Calcula pontuação final
- `get_graph_info()` - Retorna informações do grafo

**Cálculo de Pontuação:**
```
Eficiência = max(0, 1 - (seu_caminho - caminho_ótimo) / caminho_ótimo)
Pontos_Base = Eficiência × 100
Bônus_Tempo = max(0, (tempo_limite - tempo_gasto) / tempo_limite × 50)
Pontos_Total = Pontos_Base + Bônus_Tempo
XP_Ganho = Eficiência × 50 + (Bônus_Tempo / 50) × 25
```

### 4. **graph_generator.py** - Geração de Grafos

Cada nível tem um grafo pré-definido:

| Função | Nós | Tipo | Uso |
|--------|-----|------|-----|
| `generate_castle_graph()` | 4 | Simples | Tutorial |
| `generate_forest_graph()` | 7 | Médio | Nível 2 |
| `generate_city_graph()` | 10 | Complexo | Nível 3 |
| `generate_alien_graph()` | 8 | Completo | Nível 4 |

Cada grafo tem:
- Nós com posições pré-calculadas (`pos` atributo)
- Arestas com pesos (1-10)
- Nó de início (0) e fim (N)

### 5. **pathfinding.py** - Algoritmos de Busca

Implementa três algoritmos clássicos:

#### Dijkstra (Caminho Mais Curto em Grafos Ponderados)
```python
def dijkstra(graph, start, end):
    # Retorna (caminho, distância)
    # Complexidade: O((V + E) log V)
    # Garante: encontra o caminho mais curto
```

**Como funciona:**
1. Inicializa distâncias (start=0, resto=infinito)
2. Usa fila de prioridade (heap)
3. Processa nós em ordem de distância
4. Atualiza vizinhos se encontrar caminho mais curto
5. Reconstrói o caminho ao final

#### BFS (Busca em Largura)
```python
def bfs(graph, start, end):
    # Retorna (caminho, número de arestas)
    # Complexidade: O(V + E)
    # Melhor para: grafos não-ponderados
```

#### DFS (Busca em Profundidade)
```python
def dfs(graph, start, end, visited=None):
    # Retorna (caminho, número de arestas)
    # Complexidade: O(V + E)
    # Útil para: exploração completa, labirintos
```

#### Eficiência
```python
def calculate_path_efficiency(player_path, optimal_path):
    # Retorna valor entre 0 e 1
    # 1.0 = perfeito, 0.0 = ruim
```

### 6. **visualizer.py** - Renderização com Pygame

```python
class Visualizer:
    - width, height: int
    - screen: pygame.Surface
    - font_small, font_medium, font_large: pygame.font.Font
```

**Métodos principais:**
- `draw_graph()` - Renderiza nós, arestas, caminho do jogador
- `draw_menu()` - Tela inicial
- `draw_level_complete()` - Tela de conclusão
- `_calculate_node_positions()` - Layout do grafo na tela
- `_draw_hud()` - Interface do usuário

**Cores Utilizadas:**
```
BG_COLOR = (15, 15, 35)          # Fundo azul escuro
EDGE_COLOR = (100, 120, 180)     # Arestas azuis
NODE_COLOR = (100, 200, 255)     # Nós azuis claros
NODE_HIGHLIGHT = (255, 200, 100) # Nós visitados (laranja)
PATH_COLOR = (200, 255, 100)     # Caminho do jogador (amarelo)
PLAYER_COLOR = (255, 100, 100)   # Jogador (vermelho)
EXIT_COLOR = (100, 255, 100)     # Saída (verde)
```

## Fluxo de Jogo

### Inicialização
```
main() 
  ↓
Game.__init__()
  ├─ pygame.init()
  ├─ Visualizer()
  ├─ Player()
  └─ game_state = "menu"
  ↓
Game.run() → Game Loop
```

### Menu Principal
```
draw_menu()
  ├─ Titulo e opcoes
  └─ Aguarda input (1, 2 ou 3)
    ├─ 1: start_level(1)
    ├─ 2: show_stats()
    └─ 3: exit()
```

### Durante o Jogo
```
handle_events()
  └─ Clique do mouse
    ├─ Verifica nó clicado
    ├─ Valida se é vizinho
    └─ move_to_node() se válido

update()
  └─ (Futuro: atualizar inimigos, powerups)

draw()
  ├─ Limpa tela
  ├─ Desenha grafo
  ├─ Desenha nós
  ├─ Desenha caminho do jogador
  ├─ Desenha HUD
  └─ Mostra caminho ótimo se ESPAÇO

check_win()
  └─ Se current_node == end_node
    ├─ complete_level()
    └─ game_state = "level_complete"
```

### Conclusão do Nível
```
complete_level()
  ├─ Calcula tempo decorrido
  ├─ Calcula eficiência do caminho
  ├─ Gera relatório de pontuação
  ├─ Adiciona XP e pontos ao jogador
  └─ draw_level_complete()
```

## Estrutura de Dados

### Graph (NetworkX)
```python
G = nx.Graph()
G.nodes[node_id] = {
    'pos': (x, y),        # Posição 2D
    'name': 'Nome',       # Nome do nó
}
G[node1][node2] = {
    'weight': 5,          # Peso da aresta
}
```

### Configuração de Nível
```python
config = {
    'name': '🏰 Castelo',
    'description': 'Descrição',
    'difficulty': 'Fácil',
    'time_limit': 120,
    'generator': generate_castle_graph,  # Função
}
```

### Resultados de Nível
```python
results = {
    'level_id': 1,
    'level_name': '🏰 Castelo Encantado',
    'time_taken': 45.2,
    'time_limit': 120,
    'player_distance': 4,        # Arestas percorridas
    'optimal_distance': 3,       # Arestas ótimas
    'efficiency': 0.75,          # 0-1
    'base_score': 75,
    'time_bonus': 30,
    'total_score': 105,
    'xp_gained': 62,
}
```

## Eventos de Input

### Mouse
```python
pygame.MOUSEBUTTONDOWN
  └─ Clique detecta nó através de colisão circular
    └─ get_clicked_node(pos) -> node_id
```

### Teclado
```python
K_ESCAPE      → Volta ao menu
K_SPACE       → Toggle caminho ótimo
K_1           → Start level 1 (menu)
K_2           → Show stats (menu)
K_3           → Exit (menu)
```

## Performance

### Complexidade de Algoritmos
- **Dijkstra**: O((V + E) log V) com heap
- **BFS**: O(V + E)
- **DFS**: O(V + E)

### Otimizações Aplicadas
- Posições de nós pré-calculadas
- Grafos pequenos (≤10 nós)
- Renderização apenas da tela visível
- Cálculos de distância feitos uma vez por nível

## Extensibilidade

### Adicionar Novo Nível
```python
# Em graph_generator.py
def generate_my_graph():
    G = nx.Graph()
    G.add_nodes_from([...])
    G.add_weighted_edges_from([...])
    return G, start_node, end_node

# Em get_level_config
5: {
    "name": "🌟 Meu Mundo",
    "description": "...",
    "difficulty": "...",
    "time_limit": ...,
    "generator": generate_my_graph,
}
```

### Adicionar Feature
1. Criar classe/módulo
2. Integrar em `Game` class
3. Chamar em pontos apropriados (update, draw, handle_events)
4. Testar em `tests.py`

## Debugging

### Print úteis
```python
# Informações do grafo
world.get_graph_info()

# Estatísticas do jogador
player.get_stats()

# Teste de algoritmo
path, dist = dijkstra(G, 0, 3)
print(f"Caminho: {path}, Distância: {dist}")

# Performance
import time
start = time.time()
# ... código ...
print(f"Tempo: {time.time() - start:.2f}s")
```

## Próximas Melhorias

1. **Inimigos** - Movem pelo grafo, causam dano
2. **Power-ups** - Itens especiais nos nós
3. **Múltiplos Modos** - Arcade, Educacional, Infinito
4. **Customização** - Cores, nomes, dificuldade
5. **Sons** - Música ambiente e efeitos
6. **Achievements** - Troféus e distinções
7. **Multiplayer** - Competição local
8. **Estatísticas** - Save de melhores tempos
9. **Análise de Grafo** - Mostrar propriedades
10. **Tutorial Interativo** - Ensinar conceitos

---

**Para perguntas ou sugestões, consulte o README.md ou EXPANSION_IDEAS.py**
