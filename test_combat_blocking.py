"""
Script de teste para verificar o bloqueio de comandos durante combate e reset correto
"""
from main import Game
import time

def test_combat_blocking():
    """Simula teste de bloqueio durante combate"""
    print("🧪 Testando bloqueio de comandos durante combate...")
    
    game = Game()
    
    # Simular estado de combate
    game.combat_state = "simultaneous_attack"
    game.combat_node = 5
    
    # Verificar se está em combate
    print(f"🎯 Está em combate? {game.is_in_combat()}")
    
    # Simular reset durante combate
    print("🔄 Simulando reset durante combate...")
    
    # Configurar um jogador com vida reduzida (simula combate em andamento)
    game.player.health = 50
    print(f"💚 Vida antes do reset: {game.player.health}")
    
    # Executar restart (deve limpar combate e restaurar vida)
    original_lives = game.player.lives
    game.restart_level()
    
    print(f"⚔️ Estado de combate após reset: {game.combat_state}")
    print(f"💚 Vida após reset: {game.player.health}")
    print(f"❤️ Vidas: {original_lives} → {game.player.lives}")
    
    # Verificar se não está mais em combate
    print(f"🎯 Ainda está em combate após reset? {game.is_in_combat()}")

def test_movement_blocking():
    """Testa se movimentos são bloqueados durante combate"""
    print("\n🚶 Testando bloqueio de movimentos durante combate...")
    
    game = Game()
    
    # Estado normal (sem combate)
    print("Estado normal (sem combate):")
    print(f"   Pode se mover? {not game.is_in_combat()}")
    
    # Estado de combate
    game.combat_state = "simultaneous_attack"
    print("Estado de combate:")
    print(f"   Pode se mover? {not game.is_in_combat()}")
    print(f"   Está em combate? {game.is_in_combat()}")

if __name__ == "__main__":
    test_combat_blocking()
    test_movement_blocking()
    print("\n🏁 Testes concluídos!")