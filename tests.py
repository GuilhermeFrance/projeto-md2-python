"""
Testes unitários para PathFinder Adventure
Execute com: python tests.py
"""

import sys
sys.path.insert(0, '.')

from player import Player
from pathfinding import dijkstra, bfs, dfs, calculate_path_efficiency
from graph_generator import (
    generate_castle_graph, generate_forest_graph, 
    generate_city_graph, generate_alien_graph, get_level_config
)
import networkx as nx

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test(self, name, condition):
        """Executa um teste"""
        if condition:
            print(f"✅ {name}")
            self.passed += 1
        else:
            print(f"❌ {name}")
            self.failed += 1
    
    def report(self):
        """Exibe relatório final"""
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        print(f"\n{'='*50}")
        print(f"📊 RESULTADOS: {self.passed}/{total} testes passaram ({percentage:.1f}%)")
        print(f"{'='*50}\n")
        return self.failed == 0

def test_player():
    """Testa classe Player"""
    print("\n🧙 TESTANDO PLAYER")
    print("-" * 50)
    
    runner = TestRunner()
    
    # Criar jogador
    player = Player("TestPlayer", starting_node=0)
    runner.test("Criar jogador", player.name == "TestPlayer")
    runner.test("Nó inicial", player.current_node == 0)
    runner.test("Vida máxima", player.max_health == 100)
    runner.test("Nível inicial", player.level == 1)
    
    # Teste de movimento
    player.move_to_node(1)
    runner.test("Mover para nó 1", player.current_node == 1)
    runner.test("Caminho registrado", len(player.path_taken) == 2)
    
    # Teste de pontos
    player.add_points(50)
    runner.test("Adicionar pontos", player.points == 50)
    
    # Teste de experiência
    player.add_experience(100)
    runner.test("Level up", player.level == 2)
    runner.test("XP resetado após level up", player.experience == 0)
    
    # Teste de dano
    player.take_damage(30)
    runner.test("Receber dano", player.health == 80)
    
    # Teste de cura
    player.heal(20)
    runner.test("Curar", player.health == 100)
    
    return runner.report()

def test_pathfinding():
    """Testa algoritmos de busca"""
    print("\n🔍 TESTANDO ALGORITMOS DE BUSCA")
    print("-" * 50)
    
    runner = TestRunner()
    
    # Cria um grafo simples para teste
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3])
    G.add_weighted_edges_from([
        (0, 1, 1),
        (0, 2, 4),
        (1, 3, 2),
        (2, 3, 1),
    ])
    
    # Teste Dijkstra
    path, distance = dijkstra(G, 0, 3)
    runner.test("Dijkstra encontra caminho", path is not None and len(path) > 0)
    runner.test("Dijkstra caminho correto", path == [0, 1, 3])
    runner.test("Dijkstra distância correta", distance == 3)
    
    # Teste BFS
    path_bfs, edges = bfs(G, 0, 3)
    runner.test("BFS encontra caminho", path_bfs is not None and len(path_bfs) > 0)
    runner.test("BFS retorna caminho válido", path_bfs[0] == 0 and path_bfs[-1] == 3)
    
    # Teste DFS
    path_dfs, edges = dfs(G, 0, 3)
    runner.test("DFS encontra caminho", path_dfs is not None and len(path_dfs) > 0)
    runner.test("DFS retorna caminho válido", path_dfs[0] == 0 and path_dfs[-1] == 3)
    
    # Teste eficiência
    efficiency = calculate_path_efficiency(3, 3)
    runner.test("Eficiência 100%", efficiency == 1.0)
    
    efficiency = calculate_path_efficiency(6, 3)
    runner.test("Eficiência 50%", efficiency == 0.5)
    
    efficiency = calculate_path_efficiency(9, 3)
    runner.test("Eficiência 0%", efficiency == 0.0)
    
    return runner.report()

def test_graph_generation():
    """Testa geração de grafos"""
    print("\n🏗️  TESTANDO GERAÇÃO DE GRAFOS")
    print("-" * 50)
    
    runner = TestRunner()
    
    # Teste Castle
    castle, start, end = generate_castle_graph()
    runner.test("Castle tem 4 nós", castle.number_of_nodes() == 4)
    runner.test("Castle tem start e end", start == 0 and end == 3)
    runner.test("Castle é conectado", nx.is_connected(castle))
    
    # Teste Forest
    forest, start, end = generate_forest_graph()
    runner.test("Forest tem 7 nós", forest.number_of_nodes() == 7)
    runner.test("Forest é conectado", nx.is_connected(forest))
    
    # Teste City
    city, start, end = generate_city_graph()
    runner.test("City tem 10 nós", city.number_of_nodes() == 10)
    runner.test("City é conectado", nx.is_connected(city))
    
    # Teste Alien
    alien, start, end = generate_alien_graph()
    runner.test("Alien é um grafo completo", alien.number_of_nodes() == 8)
    runner.test("Alien é altamente conectado", alien.number_of_edges() == 28)
    
    return runner.report()

def test_level_config():
    """Testa configuração de níveis"""
    print("\n⚙️  TESTANDO CONFIGURAÇÃO DE NÍVEIS")
    print("-" * 50)
    
    runner = TestRunner()
    
    for level_id in range(1, 5):
        config = get_level_config(level_id)
        runner.test(f"Level {level_id} existe", config is not None)
        runner.test(f"Level {level_id} tem nome", "name" in config)
        runner.test(f"Level {level_id} tem dificuldade", "difficulty" in config)
        runner.test(f"Level {level_id} tem gerador", "generator" in config)
    
    return runner.report()

def test_integration():
    """Testa integração entre componentes"""
    print("\n🔗 TESTANDO INTEGRAÇÃO")
    print("-" * 50)
    
    runner = TestRunner()
    
    # Simula um nível completo
    from world import World
    
    world = World(1)
    player = Player("TestPlayer", starting_node=world.start_node)
    
    runner.test("World inicializado", world.graph is not None)
    runner.test("Player no nó inicial", player.current_node == world.start_node)
    runner.test("Caminho ótimo encontrado", len(world.optimal_path) > 0)
    
    # Simula movimento do jogador
    start = world.start_node
    neighbors = list(world.graph.neighbors(start))
    if neighbors:
        next_node = neighbors[0]
        player.move_to_node(next_node)
        runner.test("Player pode se mover", player.current_node == next_node)
    
    return runner.report()

def run_all_tests():
    """Executa todos os testes"""
    print("""
    ╔════════════════════════════════════════╗
    ║   🧪 SUITE DE TESTES                  ║
    ║   PathFinder Adventure                 ║
    ╚════════════════════════════════════════╝
    """)
    
    results = []
    results.append(test_player())
    results.append(test_pathfinding())
    results.append(test_graph_generation())
    results.append(test_level_config())
    results.append(test_integration())
    
    # Relatório final
    print("\n" + "="*50)
    print("📋 RELATÓRIO FINAL")
    print("="*50)
    
    all_passed = all(results)
    if all_passed:
        print("✅ TODOS OS TESTES PASSARAM! 🎉")
        print("\nO jogo está pronto para jogar!")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print("\nVerifique os erros acima e corrija antes de jogar.")
    
    print("="*50 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
