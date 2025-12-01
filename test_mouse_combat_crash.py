"""
Teste específico para simular cliques durante combate que causavam fechamento do jogo
"""
import pygame
import sys
from main import Game

def test_mouse_click_during_combat():
    """Testa cliques do mouse durante combate sem fechar o jogo"""
    print("🧪 Testando cliques durante combate (problema específico)")
    print("=" * 60)
    
    # Inicializar pygame
    pygame.init()
    pygame.display.set_mode((800, 600))  # Criar display mínimo para eventos
    
    try:
        # Criar game
        game = Game()
        
        # Simular um mundo para testes
        from world import World
        game.world = World(1)
        game.current_level = 1
        game.game_state = "playing"
        
        # Colocar jogador em combate
        game.combat_state = "simultaneous_attack"
        game.combat_node = 2
        
        print(f"✅ Estado inicial:")
        print(f"   Game state: {game.game_state}")
        print(f"   Em combate: {game.is_in_combat()}")
        print(f"   Combat state: {game.combat_state}")
        
        # Simular eventos de clique durante combate
        print(f"\n🔧 Simulando eventos de clique durante combate...")
        print("-" * 50)
        
        # Criar eventos de clique simulados
        test_positions = [
            (100, 100),
            (200, 200), 
            (300, 300),
            (400, 400)
        ]
        
        for i, pos in enumerate(test_positions):
            print(f"\n   Teste {i+1}: Clique em posição {pos}")
            
            # Criar evento de clique simulado
            mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)
            
            # Adicionar evento à fila
            pygame.event.post(mouse_event)
            
            # Processar eventos (isso deve bloquear e não fechar o jogo)
            result = game.handle_events()
            
            print(f"      Resultado handle_events(): {result}")
            print(f"      Jogo ainda rodando: {result is not False}")
            
            if result is False:
                print(f"   ❌ ERRO: Jogo foi fechado no clique {i+1}!")
                return False
            
            # Limpar fila de eventos
            pygame.event.clear()
        
        print(f"\n✅ Estado após todos os cliques:")
        print(f"   Game state: {game.game_state}")
        print(f"   Em combate: {game.is_in_combat()}")
        print(f"   Posição do jogador: {game.player.current_node}")
        
        # Teste adicional: teclas durante combate
        print(f"\n🔧 Simulando teclas durante combate...")
        print("-" * 50)
        
        test_keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE]
        
        for key in test_keys:
            print(f"   Testando tecla: {pygame.key.name(key)}")
            
            # Criar evento de tecla simulado
            key_event = pygame.event.Event(pygame.KEYDOWN, key=key)
            pygame.event.post(key_event)
            
            # Processar eventos
            result = game.handle_events()
            
            print(f"      Resultado: {result}")
            
            if result is False:
                print(f"   ❌ ERRO: Jogo foi fechado na tecla {pygame.key.name(key)}!")
                return False
                
            # Limpar fila de eventos
            pygame.event.clear()
        
        print(f"\n🎉 SUCESSO COMPLETO!")
        print(f"✅ Todos os cliques e teclas foram bloqueados sem fechar o jogo")
        print(f"✅ handle_events() sempre retornou True (jogo continua rodando)")
        
        return True
        
    except Exception as e:
        print(f"❌ EXCEÇÃO CAPTURADA: {e}")
        print(f"❌ Tipo de erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        pygame.quit()

def test_event_handling_robustness():
    """Teste de robustez do sistema de eventos"""
    print(f"\n🔧 Teste de robustez do sistema de eventos")
    print("=" * 60)
    
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    try:
        game = Game()
        game.world = World(1)
        game.game_state = "playing"
        game.combat_state = "simultaneous_attack"
        
        # Teste: múltiplos eventos em sequência rápida
        events_to_test = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(150, 150), button=1),
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w),
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(250, 250), button=1),
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a),
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE),
        ]
        
        print(f"Testando {len(events_to_test)} eventos em sequência...")
        
        for i, event in enumerate(events_to_test):
            pygame.event.post(event)
            
        # Processar todos os eventos de uma vez
        result = game.handle_events()
        
        print(f"Resultado final: {result}")
        print(f"Jogo continua rodando: {result is not False}")
        
        return result is not False
        
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("🚀 Iniciando testes de crash durante combate...")
    
    # Teste 1: Cliques individuais
    success1 = test_mouse_click_during_combat()
    
    # Teste 2: Múltiplos eventos
    success2 = test_event_handling_robustness()
    
    print(f"\n🏁 RESULTADOS FINAIS:")
    print(f"   Teste cliques individuais: {'✅ PASSOU' if success1 else '❌ FALHOU'}")
    print(f"   Teste múltiplos eventos: {'✅ PASSOU' if success2 else '❌ FALHOU'}")
    
    if success1 and success2:
        print(f"\n🎉 TODOS OS TESTES PASSARAM!")
        print(f"✅ Problema de fechamento durante combate foi CORRIGIDO!")
    else:
        print(f"\n❌ ALGUNS TESTES FALHARAM!")
        print(f"⚠️ Ainda há problemas a resolver")
        sys.exit(1)