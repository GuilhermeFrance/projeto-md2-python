"""
Módulo com algoritmos de busca em grafos
"""
import heapq
from collections import deque

def dijkstra(graph, start, end):
    """
    Algoritmo de Dijkstra para encontrar o caminho mais curto
    Retorna: (caminho, distância)
    """
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0
    previous = {node: None for node in graph.nodes()}
    pq = [(0, start)]
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current_dist > distances[current]:
            continue
            
        if current == end:
            break
            
        for neighbor in graph.neighbors(current):
            weight = graph[current][neighbor].get('weight', 1)
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))
    
    # Reconstrói o caminho
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return path if path[0] == start else [], distances[end]

def bfs(graph, start, end):
    """
    Busca em largura (BFS) para encontrar o caminho mais curto
    (em termos de número de arestas)
    Retorna: (caminho, número de arestas)
    """
    queue = deque([[start]])
    visited = {start}
    
    while queue:
        path = queue.popleft()
        current = path[-1]
        
        if current == end:
            return path, len(path) - 1
            
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append(new_path)
    
    return [], float('inf')

def dfs(graph, start, end, visited=None):
    """
    Busca em profundidade (DFS)
    Retorna: (caminho, número de arestas)
    """
    if visited is None:
        visited = set()
    
    visited.add(start)
    
    if start == end:
        return [start], 0
    
    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            path, distance = dfs(graph, neighbor, end, visited)
            if path:
                return [start] + path, distance + 1
    
    return [], float('inf')

def calculate_path_efficiency(player_path_length, optimal_path_length):
    """
    Calcula a eficiência do caminho do jogador
    Retorna um valor de 0 a 1 (1 = perfeito)
    """
    if optimal_path_length == 0:
        return 1.0
    return max(0, 1 - (player_path_length - optimal_path_length) / optimal_path_length)
