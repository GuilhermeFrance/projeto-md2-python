"""
Módulo que gerencia o mundo e os níveis do jogo
"""
from graph_generator import get_level_config
from pathfinding import dijkstra, calculate_path_efficiency
import time
import networkx as nx

class World:
    def __init__(self, level_id=1):
        self.level_id = level_id
        self.config = get_level_config(level_id)
        
        # Gera o grafo do nível
        generator = self.config["generator"]
        self.graph, self.start_node, self.end_node = generator()
        
        # Encontra o caminho ótimo
        self.optimal_path, self.optimal_distance = dijkstra(
            self.graph, self.start_node, self.end_node
        )
        
        # Gerar inimigos a partir do nível médio (nível 4+)
        self.enemies = set()
        if level_id >= 4:
            self._generate_enemies()
            # Recalcular caminho ótimo evitando inimigos para manter 3 estrelas
            self._recalculate_optimal_path_avoiding_enemies()
        
        self.start_time = None
        self.end_time = None
        self.completed = False
        
    def start_level(self):
        """Inicia o nível"""
        self.start_time = time.time()
        
    def complete_level(self, player_path):
        """Marca o nível como completo e calcula a pontuação"""
        self.end_time = time.time()
        self.completed = True
        
        elapsed_time = self.end_time - self.start_time
        path_length = len(player_path) - 1  # Número de arestas
        
        # Calcula a eficiência
        optimal_length = len(self.optimal_path) - 1
        efficiency = calculate_path_efficiency(path_length, optimal_length)
        
        # Calcula a pontuação base (0-100)
        base_score = int(efficiency * 100)
        
        # Bônus por tempo
        time_limit = self.config["time_limit"]
        time_bonus = max(0, int((time_limit - elapsed_time) / time_limit * 50))
        
        total_score = base_score + time_bonus
        
        return {
            "level_id": self.level_id,
            "level_name": self.config["name"],
            "time_taken": elapsed_time,
            "time_limit": time_limit,
            "player_distance": path_length,
            "optimal_distance": len(self.optimal_path) - 1,
            "efficiency": efficiency,
            "base_score": base_score,
            "time_bonus": time_bonus,
            "total_score": total_score,
            "xp_gained": int(efficiency * 50 + (time_bonus / 50) * 25),
        }
    
    def get_graph_info(self):
        """Retorna informações sobre o grafo"""
        return {
            "nodes": list(self.graph.nodes()),
            "edges": list(self.graph.edges(data=True)),
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
        }
    
    def _generate_enemies(self):
        """Gera inimigos em posições estratégicas que realmente atrapalham o jogador"""
        import networkx as nx
        import random
        
        # Calcular caminho ótimo do início ao fim
        try:
            optimal_path = nx.shortest_path(self.graph, self.start_node, self.end_node, weight='weight')
        except nx.NetworkXNoPath:
            # Se não há caminho, usar qualquer nó disponível
            optimal_path = [self.start_node, self.end_node]
        
        print(f"🎯 Caminho ótimo detectado: {optimal_path}")
        
        # Encontrar nós estratégicos
        strategic_nodes = self._find_strategic_nodes(optimal_path)
        
        # Número de inimigos baseado no nível - mais inimigos para dificultar
        if self.level_id < 6:  # Níveis iniciais (4-5) - 2 inimigos
            num_enemies = min(2, len(strategic_nodes))
        elif self.level_id < 10:  # Níveis médios (6-9) - 2-3 inimigos
            num_enemies = min(3, len(strategic_nodes))
        elif self.level_id < 15:  # Níveis difíceis (10-14) - 3-4 inimigos
            num_enemies = min(4, len(strategic_nodes))
        else:  # Níveis extremos (15+) - 4-5 inimigos
            num_enemies = min(5, len(strategic_nodes))
        
        # Selecionar os nós mais estratégicos
        if len(strategic_nodes) >= num_enemies:
            self.enemies = set(strategic_nodes[:num_enemies])
        else:
            # Se não há nós estratégicos suficientes, adicionar nós aleatórios extras
            self.enemies = set(strategic_nodes)
            
            # Adicionar nós aleatórios para completar o número desejado
            all_nodes = list(self.graph.nodes())
            available_extra = [n for n in all_nodes 
                             if n != self.start_node and n != self.end_node and n not in self.enemies]
            
            if available_extra:
                extra_needed = num_enemies - len(self.enemies)
                extra_enemies = random.sample(available_extra, min(extra_needed, len(available_extra)))
                self.enemies.update(extra_enemies)
                print(f"➕ Adicionados {len(extra_enemies)} inimigos extras: {extra_enemies}")
        
        print(f"🧌 Inimigos posicionados estrategicamente no nível {self.level_id}: {list(self.enemies)}")
    
    def _find_strategic_nodes(self, optimal_path):
        """Encontra nós estratégicos que forçam o jogador a enfrentá-los"""
        import networkx as nx
        
        strategic_nodes = []
        
        # 1. Nós que são pontos de estrangulamento (articulation points)
        articulation_points = list(nx.articulation_points(self.graph))
        
        # 2. Nós no meio do caminho ótimo (exceto início e fim)
        middle_optimal_nodes = optimal_path[1:-1]  # Remove primeiro e último
        
        # 3. Nós com alta centralidade (muitas conexões)
        betweenness = nx.betweenness_centrality(self.graph, weight='weight')
        high_centrality_nodes = [node for node, centrality in betweenness.items() 
                               if centrality > 0.1 and node != self.start_node and node != self.end_node]
        
        # 4. Nós que estão em caminhos alternativos importantes
        alternative_critical_nodes = self._find_alternative_path_nodes()
        
        # Priorizar nós por importância estratégica
        priority_list = []
        
        # Prioridade 1: Nós no caminho ótimo (forçam confronto)
        for node in middle_optimal_nodes:
            if node not in priority_list:
                priority_list.append(node)
        
        # Prioridade 2: Pontos de articulação (controlam acesso)
        for node in articulation_points:
            if node not in priority_list and node != self.start_node and node != self.end_node:
                priority_list.append(node)
        
        # Prioridade 3: Nós de alta centralidade
        for node in high_centrality_nodes:
            if node not in priority_list:
                priority_list.append(node)
        
        # Prioridade 4: Nós em caminhos alternativos
        for node in alternative_critical_nodes:
            if node not in priority_list:
                priority_list.append(node)
        
        print(f"🎨 Nós estratégicos encontrados: {priority_list[:5]}")
        return priority_list
    
    def _find_alternative_path_nodes(self):
        """Encontra nós críticos em caminhos alternativos"""
        import networkx as nx
        
        alternative_nodes = []
        
        try:
            # Encontrar múltiplos caminhos curtos
            all_simple_paths = list(nx.all_simple_paths(self.graph, self.start_node, self.end_node, cutoff=6))
            
            # Ordenar por comprimento (peso total)
            weighted_paths = []
            for path in all_simple_paths:
                total_weight = sum(self.graph[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
                weighted_paths.append((path, total_weight))
            
            weighted_paths.sort(key=lambda x: x[1])  # Ordenar por peso
            
            # Pegar os 3 melhores caminhos alternativos
            best_paths = [path for path, weight in weighted_paths[:3]]
            
            # Nós que aparecem em múltiplos caminhos são estratégicos
            node_frequency = {}
            for path in best_paths:
                for node in path[1:-1]:  # Excluir início e fim
                    node_frequency[node] = node_frequency.get(node, 0) + 1
            
            # Nós que aparecem em pelo menos 2 caminhos
            alternative_nodes = [node for node, freq in node_frequency.items() if freq >= 2]
            
        except (nx.NetworkXNoPath, nx.NetworkXError):
            # Se houver erro, usar nós com mais conexões
            degrees = dict(self.graph.degree())
            sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
            alternative_nodes = [node for node, degree in sorted_nodes[:3] 
                               if node != self.start_node and node != self.end_node]
        
        return alternative_nodes
    
    def has_enemy(self, node_id):
        """Verifica se um nó tem inimigo"""
        return node_id in self.enemies
    
    def remove_enemy(self, node_id):
        """Remove um inimigo de um nó (quando derrotado)"""
        if node_id in self.enemies:
            self.enemies.remove(node_id)
            # Recalcular caminho ótimo após remover inimigo
            print(f"🗡️ Inimigo removido do nó {node_id}. Recalculando caminho ótimo...")
            self.dynamic_recalculate_optimal_path()
    
    def dynamic_recalculate_optimal_path(self):
        """Recalcula dinamicamente o caminho ótimo baseado no estado atual dos inimigos"""
        if not self.enemies:
            # Sem inimigos, recalcular caminho mais direto
            self.optimal_path, self.optimal_distance = dijkstra(
                self.graph, self.start_node, self.end_node
            )
            print(f"🏃 Todos os inimigos derrotados! Caminho direto: {self.optimal_path}")
            return
        
        # Verificar se o caminho atual ainda é seguro
        current_enemies = self.count_enemies_in_path(self.optimal_path)
        
        if current_enemies >= 2:
            print(f"⚠️ Caminho atual ainda tem {current_enemies} inimigos. Buscando alternativa...")
            self._recalculate_optimal_path_avoiding_enemies()
        else:
            print(f"✅ Caminho atual é seguro ({current_enemies} inimigos)")
    
    def count_enemies_in_path(self, path):
        """Conta quantos inimigos existem no caminho especificado"""
        if not path or not self.enemies:
            return 0
        
        enemies_in_path = 0
        for node in path:
            if node in self.enemies:
                enemies_in_path += 1
        
        return enemies_in_path
    
    def has_multiple_enemies_in_optimal_path(self):
        """Verifica se há múltiplos inimigos no caminho ótimo atual"""
        return self.count_enemies_in_path(self.optimal_path) >= 2
    
    def find_safe_alternative_path(self):
        """Encontra um caminho alternativo seguro (com no máximo 1 inimigo)"""
        import networkx as nx
        
        try:
            # Encontrar todos os caminhos simples possíveis
            all_paths = list(nx.all_simple_paths(
                self.graph, self.start_node, self.end_node, cutoff=10
            ))
            
            # Avaliar cada caminho baseado em segurança e eficiência
            path_scores = []
            
            for path in all_paths:
                enemies_count = self.count_enemies_in_path(path)
                path_length = len(path) - 1
                
                # Calcular peso total do caminho
                total_weight = 0
                for i in range(len(path) - 1):
                    total_weight += self.graph[path[i]][path[i+1]].get('weight', 1)
                
                # Score: priorizar caminhos com menos inimigos
                # Penalidade severa para múltiplos inimigos
                if enemies_count >= 2:
                    safety_score = -1000  # Muito perigoso
                elif enemies_count == 1:
                    safety_score = -50   # Aceitável
                else:
                    safety_score = 100   # Seguro
                
                # Score total: segurança - comprimento (menor é melhor)
                total_score = safety_score - total_weight
                
                path_scores.append((path, enemies_count, total_weight, total_score))
            
            # Ordenar por score (maior score = melhor)
            path_scores.sort(key=lambda x: x[3], reverse=True)
            
            # Escolher o melhor caminho seguro (com no máximo 1 inimigo)
            for path, enemies_count, weight, score in path_scores:
                if enemies_count <= 1:  # Caminho seguro encontrado
                    print(f"🛡️ Caminho alternativo seguro encontrado:")
                    print(f"   Caminho: {path}")
                    print(f"   Inimigos: {enemies_count}")
                    print(f"   Peso: {weight}")
                    print(f"   Score: {score}")
                    return path, weight
            
            # Se não encontrou caminho seguro, pegar o menos perigoso
            if path_scores:
                best_path, enemies_count, weight, score = path_scores[0]
                print(f"⚠️ Nenhum caminho totalmente seguro. Usando o menos perigoso:")
                print(f"   Caminho: {best_path}")
                print(f"   Inimigos: {enemies_count}")
                print(f"   Peso: {weight}")
                return best_path, weight
            
        except Exception as e:
            print(f"❌ Erro ao buscar caminho alternativo: {e}")
        
        return None, None
    
    def _recalculate_optimal_path_avoiding_enemies(self):
        """Recalcula o caminho ótimo evitando nós com inimigos"""
        if not self.enemies:
            return  # Não há inimigos, caminho atual é válido
        
        # Verificar se o caminho atual tem múltiplos inimigos
        current_enemies = self.count_enemies_in_path(self.optimal_path)
        print(f"🔍 Caminho atual tem {current_enemies} inimigos: {self.optimal_path}")
        
        if current_enemies >= 2:
            print(f"⚠️ PERIGO: {current_enemies} inimigos no caminho ótimo! Recalculando...")
            
            # Buscar caminho alternativo mais seguro
            safe_path, safe_distance = self.find_safe_alternative_path()
            
            if safe_path:
                self.optimal_path = safe_path
                self.optimal_distance = safe_distance
                new_enemies = self.count_enemies_in_path(safe_path)
                print(f"✅ Novo caminho ótimo (com {new_enemies} inimigos): {safe_path}")
                print(f"📏 Nova distância ótima: {safe_distance}")
            else:
                print(f"❌ Não foi possível encontrar caminho alternativo mais seguro")
        
        try:
            # Método original como fallback
            # Criar uma cópia do grafo
            safe_graph = self.graph.copy()
            
            # Remover nós com inimigos (exceto start e end)
            enemies_to_remove = [node for node in self.enemies 
                               if node != self.start_node and node != self.end_node]
            
            for enemy_node in enemies_to_remove:
                if enemy_node in safe_graph:
                    safe_graph.remove_node(enemy_node)
            
            # Tentar encontrar caminho alternativo completamente livre de inimigos
            if nx.has_path(safe_graph, self.start_node, self.end_node):
                new_path = nx.shortest_path(safe_graph, self.start_node, self.end_node, weight='weight')
                new_distance = nx.shortest_path_length(safe_graph, self.start_node, self.end_node, weight='weight')
                
                # Verificar se este caminho é realmente melhor (sem inimigos)
                if self.count_enemies_in_path(new_path) == 0:
                    self.optimal_path = new_path
                    self.optimal_distance = new_distance
                    
                    print(f"🛡️ Caminho ótimo recalculado (100% seguro): {new_path}")
                    print(f"📏 Nova distância ótima: {new_distance}")
            
        except Exception as e:
            print(f"❌ Erro ao recalcular caminho ótimo: {e}")
