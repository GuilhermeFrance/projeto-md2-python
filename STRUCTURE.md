# 🏗️ ESTRUTURA DO PROJETO COMPLETA

## 📁 Árvore de Arquivos

```
c:\Users\ribei\Documents\Dev\Projects\md2\pathfinder_adventure\
│
├── 📍 COMECE AQUI
│   └── 00_START_HERE.md          ← Leia isto primeiro!
│
├── 🎮 JOGO (Execute)
│   ├── main.py                   ← python main.py
│   ├── run_game.bat              ← Duplo clique (Windows)
│   └── requirements.txt          ← pip install -r requirements.txt
│
├── 🎓 NÚCLEO DO JOGO
│   ├── player.py                 (Personagem)
│   ├── world.py                  (Níveis)
│   ├── graph_generator.py        (Mundos)
│   ├── pathfinding.py            (Algoritmos)
│   └── visualizer.py             (Gráficos)
│
├── 🧪 TESTES & EXPANSÃO
│   ├── tests.py                  (python tests.py)
│   └── EXPANSION_IDEAS.py        (10 ideias prontas)
│
├── 📚 DOCUMENTAÇÃO RÁPIDA
│   ├── QUICKSTART.md             (5 min)
│   ├── README.md                 (20 min)
│   └── VISUAL_GUIDE.md           (15 min)
│
├── 📖 DOCUMENTAÇÃO TÉCNICA
│   ├── TECHNICAL_DOCS.md         (60 min)
│   ├── SETUP.md                  (Troubleshooting)
│   └── INDEX.md                  (Navegação)
│
├── 📋 RESUMOS
│   └── PROJECT_SUMMARY.md        (Conclusão)
│
└── 📂 DIRETÓRIOS (Futuros)
    ├── assets/                   (Sprites, Sons)
    └── levels/                   (Dados de Níveis)
```

---

## 🎯 Guia de Uso Por Tipo

### 👤 Usuário Final (Quer Jogar)
```
1. Leia: 00_START_HERE.md (2 min)
2. Leia: QUICKSTART.md (3 min)
3. Execute: python main.py (ou run_game.bat)
4. Divirta-se! 🎮
```

### 📚 Estudante (Quer Aprender)
```
1. Leia: 00_START_HERE.md
2. Leia: README.md (explicação completa)
3. Jogue: Todos os 4 mundos
4. Estude: VISUAL_GUIDE.md (diagramas)
5. Aprofunde: TECHNICAL_DOCS.md (1 hora)
```

### 💻 Desenvolvedor (Quer Entender)
```
1. Leia: PROJECT_SUMMARY.md (overview)
2. Estude: TECHNICAL_DOCS.md (arquitetura)
3. Leia código na ordem:
   → main.py (fluxo)
   → player.py (simples)
   → world.py (intermediário)
   → pathfinding.py (algoritmos)
   → visualizer.py (complexo)
4. Execute: python tests.py
5. Veja: EXPANSION_IDEAS.py
```

### 🚀 Contribuidor (Quer Expandir)
```
1. Leia: PROJECT_SUMMARY.md
2. Estude: TECHNICAL_DOCS.md
3. Leia: EXPANSION_IDEAS.py (escolha uma)
4. Modifique: Código conforme ideia
5. Valide: python tests.py
6. Teste: python main.py
```

---

## 📊 Tamanho dos Arquivos

### Código Python
```
main.py              ~200 linhas   (Loop principal)
pathfinding.py       ~100 linhas   (Algoritmos) ⭐ IMPORTANTE
graph_generator.py   ~150 linhas   (Grafos)
visualizer.py        ~250 linhas   (Renderização)
world.py             ~90 linhas    (Lógica)
player.py            ~80 linhas    (Dados)
tests.py             ~300 linhas   (Testes)
───────────────────────────────────────────
TOTAL               ~1.170 linhas  (Código)
```

### Documentação
```
QUICKSTART.md         ~100 linhas
README.md             ~300 linhas
TECHNICAL_DOCS.md     ~400 linhas
VISUAL_GUIDE.md       ~250 linhas
PROJECT_SUMMARY.md    ~200 linhas
SETUP.md              ~100 linhas
INDEX.md              ~350 linhas
00_START_HERE.md      ~200 linhas
───────────────────────────────────────────
TOTAL               ~1.900 linhas  (Documentação)
```

### Total: ~3.000 linhas de código e documentação

---

## 🔗 Dependências Entre Arquivos

```
main.py (INÍCIO)
├─ imports: pygame
├─ imports: Player (player.py)
├─ imports: World (world.py)
├─ imports: Visualizer (visualizer.py)
├─ imports: pathfinding (pathfinding.py)
└─ Loop: handle_events → update → draw
       │
       ├─ handle_events
       │  └─ Clique de mouse/teclado
       │
       ├─ update
       │  └─ (Futuro: inimigos, physics)
       │
       └─ draw
          ├─ visualizer.draw_graph()
          └─ player + world state

player.py (MODELO)
└─ Dados: health, level, xp, points
   Métodos: move, add_xp, heal, etc

world.py (LÓGICA)
├─ imports: graph_generator
├─ imports: pathfinding
├─ Cria: Grafo
├─ Calcula: Caminho ótimo
└─ Pontuação: based em eficiência

graph_generator.py (GRAFOS)
├─ Retorna: 4 grafos (castle, forest, city, alien)
└─ Cada um: 4-10 nós com pesos

pathfinding.py (ALGORITMOS)
├─ dijkstra(): Encontra caminho ótimo
├─ bfs(): Busca em largura
├─ dfs(): Busca em profundidade
└─ efficiency(): Calcula qualidade

visualizer.py (RENDERIZAÇÃO)
├─ imports: pygame, networkx
├─ draw_graph(): Grafo + HUD
├─ draw_menu(): Menu principal
└─ draw_level_complete(): Fim do nível

tests.py (VALIDAÇÃO)
└─ imports: Tudo acima
   ├─ test_player()
   ├─ test_pathfinding()
   ├─ test_graphs()
   ├─ test_levels()
   └─ test_integration()
```

---

## 🎯 Fluxo de Execução

```
INÍCIO: python main.py
   ↓
Game.__init__()
   ├─ pygame.init()
   ├─ Player() → stats iniciais
   ├─ Visualizer() → Pygame window
   └─ game_state = "menu"
   ↓
Game.run() → LOOP INFINITO
   ├─ handle_events()
   │  ├─ Verifica cliques/teclas
   │  └─ Atualiza game_state
   │
   ├─ update()
   │  └─ (Lógica de atualização)
   │
   ├─ draw()
   │  ├─ Limpa tela
   │  ├─ Renderiza estado atual
   │  └─ pygame.display.flip()
   │
   └─ clock.tick(60) → 60 FPS
   
DURANTE O JOGO:
   ├─ handle_events() → Clique no nó
   ├─ Player.move_to_node() → Atualiza posição
   ├─ Verifica: É a saída?
   │  ├─ SIM → World.complete_level()
   │  └─ NÃO → Continua jogando
   │
   └─ draw() → Renderiza grafo + jogador

QUANDO CLICA NA SAÍDA:
   ├─ World.complete_level()
   │  ├─ Calcula tempo
   │  ├─ Calcula eficiência
   │  ├─ Calcula pontuação
   │  └─ Retorna resultados
   │
   ├─ Player.add_points() → Adiciona pontos
   ├─ Player.add_experience() → Adiciona XP + Level up?
   ├─ game_state = "level_complete"
   └─ draw_level_complete()

MENU PRINCIPAL:
   ├─ Pressiona 1 → start_level(1) → game_state = "playing"
   ├─ Pressiona 2 → show_stats()
   └─ Pressiona 3 → exit()

DURANTE NÍVEL COMPLETO:
   ├─ Pressiona ESC → game_state = "menu"
   ├─ Pressiona ESPAÇO (próx) → start_level(2)
   └─ Quando completa todos 4 → Volta ao menu

SAÍDA:
   ├─ ESC no menu
   ├─ pygame.quit()
   └─ sys.exit()
```

---

## 📦 Como Instalar e Rodar

### Primeira Vez
```powershell
# 1. Python (se não tiver)
# Baixe de: https://python.org
# IMPORTANTE: Marque "Add Python to PATH"

# 2. Entre no diretório
cd "c:\Users\ribei\Documents\Dev\Projects\md2\pathfinder_adventure"

# 3. Instale dependências
py -m pip install pygame networkx numpy

# 4. Execute
py main.py
```

### Próximas Vezes
```powershell
cd "c:\Users\ribei\Documents\Dev\Projects\md2\pathfinder_adventure"
py main.py
```

### No Windows (Duplo clique)
```
run_game.bat
```

---

## 🧪 Como Testar

```powershell
# No diretório do projeto
py tests.py

# Saída esperada:
# ✅ Player tests: 8/8 passed
# ✅ Pathfinding tests: 9/9 passed
# ✅ Graphs tests: 4/4 passed
# ✅ Levels tests: 4/4 passed
# ✅ Integration tests: 4/4 passed
# TOTAL: 29/29 PASSED ✨
```

---

## 🎮 Como Jogar

```
1. Execute: py main.py

2. Menu Principal:
   Pressione: 1 (Novo Jogo)
             2 (Estatísticas)
             3 (Sair)

3. Selecione Nível: 1-4

4. Durante o Jogo:
   Clique     → Mover
   ESPAÇO     → Ver caminho ótimo
   ESC        → Menu
   
5. Objetivo:
   Clique no nó verde (saída)
   Maximizando eficiência e velocidade

6. Progresso:
   Nível 1-4 desbloqueados
   XP/Pontos acumulados
   Level up ao atingir 100 XP
```

---

## 📝 Estrutura de Dados Principal

```python
# Player
player = {
    'name': str,
    'health': int,
    'level': int,
    'experience': int,
    'points': int,
    'current_node': int,
    'path_taken': list,
}

# World
world = {
    'level_id': int,
    'graph': networkx.Graph,
    'start_node': int,
    'end_node': int,
    'optimal_path': list,
    'optimal_distance': float,
    'config': dict,
}

# Graph Node
node = {
    'pos': (x, y),
    'name': str,
}

# Graph Edge
edge = {
    'weight': int,
}

# Level Config
config = {
    'name': str,
    'description': str,
    'difficulty': str,
    'time_limit': int,
    'generator': function,
}
```

---

## ⚙️ Configuração do Projeto

### Dependências (requirements.txt)
```
pygame==2.5.2           # Renderização gráfica
networkx==3.2           # Manipulação de grafos
numpy==1.24.3           # Cálculos matemáticos
```

### Python
```
Mínimo: Python 3.8
Recomendado: Python 3.9+
```

### Sistema Operacional
```
Windows:  ✅ Testado (run_game.bat)
macOS:    ✅ Sim (terminal)
Linux:    ✅ Sim (terminal)
```

---

## 📚 Documentação

Cada arquivo .md tem um propósito:

| Arquivo | Para | Tempo |
|---------|------|-------|
| 00_START_HERE.md | Todo mundo | 2 min |
| QUICKSTART.md | Impacientes | 5 min |
| README.md | Todos | 20 min |
| VISUAL_GUIDE.md | Visuais | 15 min |
| TECHNICAL_DOCS.md | Devs | 60 min |
| SETUP.md | Com problemas | 10 min |
| INDEX.md | Navegação | 5 min |
| PROJECT_SUMMARY.md | Resumo | 10 min |

---

## 🎊 Resumo Final

✨ **PathFinder Adventure é um projeto completo!**

Tem:
- ✅ Jogo funcionando
- ✅ Código profissional
- ✅ Documentação total
- ✅ Testes automatizados
- ✅ Ideias de expansão
- ✅ Fácil de usar
- ✅ Fácil de expandir

**Comece aqui:** `00_START_HERE.md`

**Boa sorte! 🧙✨**
