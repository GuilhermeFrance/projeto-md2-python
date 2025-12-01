"""
Teste simplificado para verificar se o problema de crash foi resolvido
"""
import pygame
from main import Game
from world import World

def test_simple_combat_interaction():
    """Teste simples de interação durante combate"""
    print("🧪 Teste simplificado - Interação durante combate")
    print("=" * 50)
    
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    try:
        # Criar game e inicializar corretamente
        game = Game()
        
        # Inicializar um nível real
        game.start_level(1)
        
        print(f"✅ Nível inicializado:")
        print(f"   Game state: {game.game_state}")
        print(f"   Player health: {game.player.health}")
        print(f"   Current node: {game.player.current_node}")
        
        # Simular combate (da forma correta)
        if game.world and hasattr(game.world, 'graph'):
            # Usar um nó válido do grafo
            nodes = list(game.world.graph.nodes())
            if len(nodes) > 1:
                target_node = nodes[1]  # Segundo nó
                
                # Simular início de combate corretamente
                print(f"\n🔧 Simulando combate no nó {target_node}...")
                game.start_combat(target_node)
                
                print(f"   Combat state: {game.combat_state}")
                print(f"   Em combate: {game.is_in_combat()}")
                
                # Agora testar cliques durante combate
                print(f"\n🔧 Testando clique durante combate...")
                
                # Criar evento de clique
                mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(300, 300), button=1)
                pygame.event.post(mouse_event)
                
                # Processar eventos - isso NÃO deve fechar o jogo
                result = game.handle_events()
                
                print(f"   Resultado handle_events(): {result}")
                print(f"   Jogo ainda ativo: {result is not False}")
                
                if result is False:
                    print("❌ ERRO: Jogo foi fechado!")
                    return False
                else:
                    print("✅ SUCESSO: Jogo permaneceu ativo!")
                    return True
            else:
                print("❌ Grafo não tem nós suficientes para teste")
                return False
        else:
            print("❌ Mundo não foi inicializado corretamente")
            return False
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        pygame.quit()

def test_keyboard_during_combat():
    """Teste de teclas durante combate"""
    print(f"\n🧪 Teste de teclas durante combate")
    print("=" * 50)
    
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    try:
        game = Game()
        game.start_level(1)
        
        # Simular combate mal configurado (cenário problemático)
        print("Simulando estado de combate problemático...")
        game.combat_state = "simultaneous_attack"
        # Propositalmente NÃO definir combat_player_initial_health
        
        print(f"Em combate: {game.is_in_combat()}")
        
        # Testar tecla que pode causar problema
        key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
        pygame.event.post(key_event)
        
        # Processar - deve ser bloqueado graciosamente
        result = game.handle_events()
        
        print(f"Resultado: {result}")
        print(f"Combat state após proteção: {game.combat_state}")
        
        return result is not False
        
    except Exception as e:
        print(f"ERRO: {e}")
        return False
        
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("🚀 Iniciando testes simplificados...")
    
    success1 = test_simple_combat_interaction()
    success2 = test_keyboard_during_combat()
    
    print(f"\n🏁 RESULTADOS:")
    print(f"   Teste clique durante combate: {'✅' if success1 else '❌'}")
    print(f"   Teste teclado durante combate: {'✅' if success2 else '❌'}")
    
    if success1 and success2:
        print(f"\n🎉 PROBLEMA CORRIGIDO!")
        print(f"✅ Jogo não fecha mais durante interações em combate")
    else:
        print(f"\n⚠️ Ainda há problemas a corrigir")