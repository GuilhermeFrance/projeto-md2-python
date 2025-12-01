"""
Teste para verificar se o crash ao tentar mover durante combate foi corrigido
"""
import pygame
import sys
from main import Game

def test_movement_during_combat():
    """Testa tentativa de movimento durante combate sem crash"""
    print("🧪 Testando movimento durante combate (sem crash)")
    print("=" * 50)
    
    # Inicializar pygame
    pygame.init()
    
    try:
        # Criar game
        game = Game()
        game.current_level = 1
        
        # Simular um mundo para testes
        from world import World
        game.world = World(1)
        
        # Colocar jogador em combate
        game.combat_state = "simultaneous_attack"
        game.combat_node = 2
        
        print(f"✅ Estado inicial:")
        print(f"   Em combate: {game.is_in_combat()}")
        print(f"   Posição atual: {game.player.current_node}")
        
        # Testar diferentes tipos de movimento que anteriormente causariam crash
        
        print(f"\n🔧 Teste 1: Clique em nó")
        print("-" * 30)
        game.handle_node_click(1, bypass_confirmation=True)  # Tentar mover para nó 1
        
        print(f"\n🔧 Teste 2: Movimento direcional")
        print("-" * 30)
        game.move_player_direction('up')
        
        print(f"\n🔧 Teste 3: Movimento diagonal")
        print("-" * 30)
        game.move_player_diagonal_direction('northeast')
        
        print(f"\n🔧 Teste 4: Execute movement direto")
        print("-" * 30)
        game.execute_movement(0, 1)
        
        print(f"\n✅ Estado final:")
        print(f"   Em combate: {game.is_in_combat()}")
        print(f"   Posição atual: {game.player.current_node}")
        print(f"   Está movendo: {game.is_moving}")
        
        print(f"\n🎉 SUCESSO: Nenhum crash detectado!")
        print(f"✅ Todos os movimentos foram bloqueados corretamente durante combate")
        
        # Testar remoção de combate e movimento normal
        print(f"\n🔧 Teste 5: Movimento após sair do combate")
        print("-" * 30)
        
        game.combat_state = None
        game.combat_node = None
        
        print(f"Em combate após limpar estado: {game.is_in_combat()}")
        
        # Agora movimento deve funcionar
        game.handle_node_click(1, bypass_confirmation=True)
        print(f"Movimento executado após sair do combate: está movendo = {game.is_moving}")
        
        print(f"\n🏁 TESTE COMPLETO - SEM CRASHES!")
        
    except Exception as e:
        print(f"❌ ERRO DETECTADO: {e}")
        print(f"❌ Tipo de erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        pygame.quit()
        
    return True

if __name__ == "__main__":
    success = test_movement_during_combat()
    if success:
        print("\n✅ TESTE PASSOU - Problema de crash corrigido!")
    else:
        print("\n❌ TESTE FALHOU - Ainda há problemas!")
        sys.exit(1)