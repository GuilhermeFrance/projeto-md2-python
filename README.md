# 🧙 PathFinder Adventure

Um jogo educativo e divertido que ensina conceitos de **Matemática Discreta 2** e **Teoria dos Grafos** através de uma aventura imersiva com um personagem que evolui!

## 📖 Sobre o Projeto

PathFinder Adventure combina educação e entretenimento, permitindo que jogadores aprendam sobre:
- ✅ **Grafos** - estruturas de dados fundamentais
- ✅ **Algoritmos de busca** - Dijkstra, BFS, DFS
- ✅ **Caminhos mais curtos** - encontrando rotas ótimas
- ✅ **Eficiência** - análise de qualidade de soluções

Tudo isso em um ambiente visual e interativo!

## 🎮 Gameplay

### Como Jogar:
1. **Clique em nós vizinhos** para mover seu personagem pelo grafo
2. **Encontre o caminho mais curto** até a saída (nó verde)
3. **Ganhe pontos** baseado em:
   - Eficiência do caminho (quanto mais próximo do ótimo, melhor!)
   - Tempo gasto (quanto mais rápido, mais bônus!)
4. **Acumule experiência** para fazer level up
5. **Desbloqueie novos mundos** conforme progride

### Controles:
- 🖱️ **Clique do mouse** - Mover para nó vizinho
- **ESPAÇO** - Mostrar/esconder o caminho ótimo
- **ESC** - Voltar ao menu
- **1** - Iniciar novo jogo (Menu)
- **2** - Ver estatísticas (Menu)
- **3** - Sair (Menu)

## 🌍 Mundos Disponíveis

| Nível | Nome | Dificuldade | Descrição |
|-------|------|-------------|-----------|
| 1 | 🏰 Castelo Encantado | Fácil | 4 nós, introdução aos grafos |
| 2 | 🌲 Floresta Mágica | Normal | 7 nós, grafos mais complexos |
| 3 | 🏙️ Cidade Futurista | Difícil | 10 nós, múltiplos caminhos |
| 4 | 👽 Dimensão Alienígena | Extremo | Grafo completo, desafio máximo |

## 🛠️ Instalação

### Pré-requisitos:
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos:
1. Clone ou baixe o projeto
2. Navegue até o diretório do projeto:
   ```bash
   cd pathfinder_adventure
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Executando o Jogo

```bash
python main.py
```

O jogo abrirá uma janela com o menu principal. Você pode começar um novo jogo, ver estatísticas ou sair.

## 📊 Sistema de Pontuação

A pontuação é calculada assim:

```
Pontuação Total = Pontuação de Eficiência + Bônus de Tempo

Eficiência = (1 - (seu_caminho - caminho_ótimo) / caminho_ótimo) × 100
Bônus de Tempo = max(0, (tempo_limite - tempo_gasto) / tempo_limite × 50)
XP Ganho = eficiência × 50 + (bônus_tempo / 50) × 25
```

## 💾 Arquivos do Projeto

- **main.py** - Loop principal do jogo
- **player.py** - Sistema do personagem e progressão
- **world.py** - Gerenciamento de níveis e mundos
- **graph_generator.py** - Geração de grafos para cada nível
- **pathfinding.py** - Implementação de algoritmos (Dijkstra, BFS, DFS)
- **visualizer.py** - Renderização visual com Pygame
- **requirements.txt** - Dependências do projeto

## 🎓 Conceitos de Matemática Discreta

### Algoritmo de Dijkstra
Encontra o caminho mais curto em um grafo ponderado. O jogo usa isso para determinar o "caminho ótimo".

### BFS (Busca em Largura)
Útil para encontrar o caminho com menor número de arestas em grafos não-ponderados.

### DFS (Busca em Profundidade)
Explora o grafo sistematicamente, visitando cada nó uma vez.

### Eficiência de Caminho
Medida de quão bom é seu caminho comparado ao ótimo:
- 100% = Você encontrou o caminho ótimo! 🏆
- 50% = Seu caminho é o dobro do ótimo
- 0% = Você não encontrou um caminho válido

## 🎨 Interface Visual

- **Azul claro** - Nós normais
- **Laranja** - Nós que você já visitou
- **Verde** - Nó de saída (objetivo)
- **Vermelho** - Seu personagem
- **Amarelo** - Seu caminho percorrido
- **Ciano** - Caminho ótimo (quando visível com ESPAÇO)

## 📈 Estatísticas do Jogador

O jogo rastreia:
- 💎 Pontos totais
- ⭐ Nível e experiência
- ❤️ Vida (em futuras versões com inimigos)
- 🗝️ Itens coletados
- 🏆 Melhores tempos por nível

## 🔮 Ideias Futuras

- 👻 Inimigos que se movem pelo grafo
- 🎁 Power-ups e itens especiais
- 🎵 Música e efeitos sonoros
- 💾 Sistema de save/load
- 🏆 Ranking online
- 📱 Versão mobile
- 🌈 Mais temas e mundos

## 📝 Exemplos de Uso

### Rodando o jogo:
```python
python main.py
```

### Saída esperada:
```
╔════════════════════════════════════════╗
║   🧙 PathFinder Adventure 🧙          ║
║  Jogo de Grafos e Matemática Discreta ║
╚════════════════════════════════════════╝
```

Então a janela do Pygame abre e você pode começar a jogar!

## 🐛 Troubleshooting

### Pygame não instala:
```bash
# Tente instalar uma versão específica
pip install pygame==2.5.2
```

### Erro de módulo não encontrado:
```bash
# Certifique-se que está no diretório correto
cd pathfinder_adventure
# E que as dependências estão instaladas
pip install -r requirements.txt
```

## 📄 Licença

Este projeto é educacional e livre para usar e modificar.

## 👨‍💻 Desenvolvedor

Criado como um projeto educativo para Matemática Discreta 2.

## 🤝 Contribuições

Sinta-se livre para fazer fork, melhorar e adicionar features! Sugestões:
- Novos algoritmos de busca
- Mais mundos temáticos
- Sistema de combate
- Multiplayer
- Trading de itens

---

**Divirta-se explorando grafos! 🧙✨**
