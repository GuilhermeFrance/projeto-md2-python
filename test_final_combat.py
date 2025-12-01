"""
Teste final para verificar todas as implementações
"""
import pygame
from main import Game

def test_complete_combat_system():
    """Teste completo do sistema de combate e reset"""
    print("🧪 TESTE COMPLETO - Sistema de Combate e Reset")
    print("=" * 60)
    
    # Inicializar pygame para evitar problemas
    pygame.init()
    
    # Criar game
    game = Game()
    
    # Teste 1: Verificar bloqueio de combate
    print("\n📋 Teste 1: Bloqueio durante combate")
    print("-" * 40)
    
    # Estado normal
    print(f"Estado inicial - Em combate: {game.is_in_combat()}")
    
    # Simular combate
    game.combat_state = "simultaneous_attack"
    game.combat_node = 5
    print(f"Durante combate - Em combate: {game.is_in_combat()}")
    
    # Teste 2: Reset com vida baixa
    print("\n📋 Teste 2: Reset com vida baixa")
    print("-" * 40)
    
    game.player.health = 25  # Vida baixa
    game.player.lives = 3    # Vidas cheias
    print(f"Vida antes do reset: {game.player.health}/{game.player.max_health}")
    print(f"Vidas antes do reset: {game.player.lives}")
    print(f"Em combate antes do reset: {game.is_in_combat()}")
    
    # Executar reset
    game.restart_level()
    
    print(f"Vida após reset: {game.player.health}/{game.player.max_health}")
    print(f"Vidas após reset: {game.player.lives}")
    print(f"Em combate após reset: {game.is_in_combat()}")
    print(f"Estado de combate: {game.combat_state}")
    
    # Teste 3: Verificação de estados limpos
    print("\n📋 Teste 3: Estados limpos após reset")
    print("-" * 40)
    
    print(f"combat_state: {game.combat_state}")
    print(f"combat_node: {game.combat_node}")
    print(f"is_moving: {game.is_moving}")
    print(f"dead_enemies: {game.dead_enemies}")
    
    # Resultado
    print("\n🎯 RESULTADOS:")
    print("=" * 60)
    
    success_checks = []
    
    # Verificar se vida foi restaurada
    vida_ok = game.player.health == game.player.max_health
    success_checks.append(("Vida restaurada", vida_ok))
    
    # Verificar se não está mais em combate
    combate_ok = not game.is_in_combat()
    success_checks.append(("Combate limpo", combate_ok))
    
    # Verificar se estados foram resetados
    estados_ok = (game.combat_state is None and 
                  game.combat_node is None and 
                  not game.is_moving and 
                  len(game.dead_enemies) == 0)
    success_checks.append(("Estados resetados", estados_ok))
    
    # Verificar se vida foi reduzida
    vidas_ok = game.player.lives == 2  # Deveria ter perdido 1 vida
    success_checks.append(("Vida consumida", vidas_ok))
    
    for check_name, passed in success_checks:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{status} - {check_name}")
    
    all_passed = all(passed for _, passed in success_checks)
    final_status = "🎉 TODOS OS TESTES PASSARAM!" if all_passed else "⚠️ ALGUNS TESTES FALHARAM"
    print(f"\n{final_status}")
    
    # Cleanup
    pygame.quit()

if __name__ == "__main__":
    test_complete_combat_system()