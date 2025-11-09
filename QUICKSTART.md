# 🚀 QUICKSTART - PathFinder Adventure

## ⚡ Começo Rápido (5 minutos)

### 1. **Instale Python**
- Windows: Baixe em https://www.python.org/downloads/
- **IMPORTANTE**: Marque "Add Python to PATH" na instalação!

### 2. **Abra PowerShell neste diretório**
```powershell
cd "c:\Users\ribei\Documents\Dev\Projects\md2\pathfinder_adventure"
```

### 3. **Instale as dependências**
```powershell
py -m pip install pygame==2.5.2 networkx==3.2 numpy==1.24.3
```

### 4. **Execute o jogo!**
```powershell
py main.py
```

---

## 🎮 Como Jogar em 30 segundos

1. **Menu Principal** abre → Pressione `1` para começar
2. **Você vê um grafo** com nós azuis e uma saída verde
3. **Clique nos nós vizinhos** para mover seu personagem (ponto vermelho)
4. **Encontre o caminho mais curto** até a saída verde
5. **Ganhe pontos** por eficiência e velocidade
6. **Desbloqueie 4 mundos** com dificuldade crescente

---

## 🎯 Controles

```
🖱️  CLIQUE       → Mover para nó vizinho
⎵  ESPAÇO       → Ver caminho ótimo (dica!)
ESC            → Voltar ao menu
1              → Novo jogo (no menu)
2              → Ver estatísticas (no menu)
3              → Sair (no menu)
```

---

## 📊 Mundos Disponíveis

| # | Nome | Nós | Dificuldade |
|---|------|-----|-------------|
| 1 | 🏰 Castelo | 4 | ⭐ Fácil |
| 2 | 🌲 Floresta | 7 | ⭐⭐ Normal |
| 3 | 🏙️  Cidade | 10 | ⭐⭐⭐ Difícil |
| 4 | 👽 Alienígena | 8 | ⭐⭐⭐⭐ Extremo |

---

## 🎓 O que você aprende

- **Grafos** - Estruturas de dados com nós e arestas
- **Caminhos mais curtos** - Algoritmo de Dijkstra
- **Busca em grafos** - BFS, DFS
- **Eficiência** - Encontrar soluções ótimas
- **Programação** - Como jogos são construídos

---

## 📂 Arquivos Importantes

```
📁 pathfinder_adventure/
├── 🎮 main.py           ← Execute isto!
├── 🧙 player.py         ← Sistema de personagem
├── 🌍 world.py          ← Gerenciamento de níveis
├── 📊 pathfinding.py    ← Algoritmos de busca
├── 🏗️  graph_generator.py ← Criação de mundos
├── 🎨 visualizer.py     ← Renderização
├── 📖 README.md         ← Documentação completa
├── 📚 TECHNICAL_DOCS.md ← Para desenvolvedores
└── 🧪 tests.py          ← Testes automáticos
```

---

## 🐛 Problemas Comuns

### "Python não é reconhecido"
→ Instale novamente e marque "Add Python to PATH"

### "Pygame não instala"
→ Tente: `py -m pip install --upgrade pygame`

### "Janela não abre"
→ Verifique se todas as dependências estão instaladas:
```powershell
py -c "import pygame, networkx, numpy; print('✅ OK')"
```

---

## 🎉 Próximos Passos

### Iniciante:
1. Jogue os 4 mundos
2. Tente conseguir 100% em cada nível
3. Desbloqueie todos os troféus

### Intermediário:
1. Leia `TECHNICAL_DOCS.md`
2. Entenda o código em `pathfinding.py`
3. Experimente mudar os grafos em `graph_generator.py`

### Avançado:
1. Adicione novas features (veja `EXPANSION_IDEAS.py`)
2. Crie seus próprios mundos
3. Implemente inimigos ou power-ups

---

## 🛠️ Personalize Seu Jogo

### Mudar nome do personagem:
```python
# Em main.py, mude:
self.player = Player("Seu Nome Aqui")
```

### Mudar cores:
```python
# Em visualizer.py, procure por:
self.NODE_COLOR = (100, 200, 255)  # Experimente RGB!
```

### Criar novo mundo:
```python
# Em graph_generator.py:
def generate_my_world():
    G = nx.Graph()
    # ... adicione nós e arestas ...
    return G, start_node, end_node
```

---

## 📞 Ajuda

- **Leia**: `README.md` (instruções completas)
- **Entenda**: `TECHNICAL_DOCS.md` (como funciona)
- **Expanda**: `EXPANSION_IDEAS.py` (ideias de features)
- **Teste**: `python tests.py` (verificar se tudo funciona)

---

## 🎯 Meta Final

```
Complete todos os 4 mundos com 100% em cada um!
Você dominará Grafos e Matemática Discreta 2! 🏆
```

---

**Divirta-se! 🧙✨**

Qualquer dúvida, abra o `README.md` ou veja o código nos arquivos .py
