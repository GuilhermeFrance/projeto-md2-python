"""
Script de teste para verificar o sistema de recálculo de caminho com inimigos
"""
import networkx as nx
from world import World
from pathfinding import dijkstra

def test_enemy_pathfinding():
    """Testa o sistema de recálculo quando há múltiplos inimigos no caminho"""
    print("🧪 Testando sistema de recálculo de caminho com inimigos...")
    
    # Criar um mundo do nível 4 (primeiro com inimigos)
    world = World(4)
    
    print(f"📍 Nó inicial: {world.start_node}")
    print(f"🏁 Nó final: {world.end_node}")
    print(f"🧌 Inimigos no nível: {list(world.enemies)}")
    print(f"🛤️ Caminho ótimo inicial: {world.optimal_path}")
    print(f"📏 Distância ótima inicial: {world.optimal_distance}")
    
    # Verificar quantos inimigos estão no caminho ótimo
    enemies_in_optimal = world.count_enemies_in_path(world.optimal_path)
    print(f"⚔️ Inimigos no caminho ótimo: {enemies_in_optimal}")
    
    if enemies_in_optimal >= 2:
        print("⚠️ PROBLEMA DETECTADO: Múltiplos inimigos no melhor caminho!")
        
        # Testar o sistema de busca de caminho alternativo
        safe_path, safe_distance = world.find_safe_alternative_path()
        
        if safe_path:
            enemies_in_safe = world.count_enemies_in_path(safe_path)
            print(f"✅ Caminho alternativo encontrado: {safe_path}")
            print(f"📏 Distância do caminho seguro: {safe_distance}")
            print(f"🛡️ Inimigos no caminho seguro: {enemies_in_safe}")
            
            if enemies_in_safe < enemies_in_optimal:
                print("🎉 SUCESSO: Caminho mais seguro encontrado!")
            else:
                print("⚠️ Caminho alternativo não é mais seguro")
        else:
            print("❌ Nenhum caminho alternativo encontrado")
    else:
        print("✅ Caminho ótimo já é seguro (poucos inimigos)")
    
    # Simular remoção de um inimigo
    if world.enemies:
        enemy_to_remove = list(world.enemies)[0]
        print(f"\n🗡️ Simulando remoção do inimigo no nó {enemy_to_remove}...")
        
        world.remove_enemy(enemy_to_remove)
        
        print(f"🛤️ Novo caminho ótimo: {world.optimal_path}")
        print(f"📏 Nova distância ótima: {world.optimal_distance}")
        print(f"🧌 Inimigos restantes: {list(world.enemies)}")

def test_multiple_levels():
    """Testa múltiplos níveis para ver o comportamento do sistema"""
    print("\n🎮 Testando múltiplos níveis...")
    
    for level in range(4, 8):  # Níveis 4-7 (têm inimigos)
        print(f"\n--- Nível {level} ---")
        try:
            world = World(level)
            enemies_count = len(world.enemies)
            enemies_in_optimal = world.count_enemies_in_path(world.optimal_path)
            
            print(f"🧌 Total de inimigos: {enemies_count}")
            print(f"⚔️ Inimigos no caminho ótimo: {enemies_in_optimal}")
            print(f"🛤️ Caminho: {world.optimal_path}")
            
            if enemies_in_optimal >= 2:
                print(f"⚠️ PERIGO: {enemies_in_optimal} inimigos no caminho!")
                
                # Verificar se o sistema consegue encontrar alternativa
                safe_path, _ = world.find_safe_alternative_path()
                if safe_path:
                    safe_enemies = world.count_enemies_in_path(safe_path)
                    print(f"✅ Alternativa encontrada com {safe_enemies} inimigos")
                else:
                    print("❌ Nenhuma alternativa encontrada")
            
        except Exception as e:
            print(f"❌ Erro no nível {level}: {e}")

if __name__ == "__main__":
    test_enemy_pathfinding()
    test_multiple_levels()
    
    print("\n🏁 Teste concluído!")