import os
import argparse
from typing import List, Tuple, Dict, Optional

# Tipos para anotação
Grafo = Tuple[int, List[Tuple[int, int, int]]]
Caminho = Optional[List[int]]

def ler_grafo_do_arquivo(caminho_arquivo: str) -> Grafo:
    """
    Lê um grafo direcionado e com pesos de um arquivo de texto.
    O formato esperado é:
    <num_vertices> <num_arestas>
    <vertice_origem> <vertice_destino> <custo>
    ...
    """
    try:
        with open(caminho_arquivo, 'r') as f:
            num_vertices, num_arestas = map(int, f.readline().split())
            arestas = []
            for _ in range(num_arestas):
                origem, destino, custo = map(int, f.readline().split())
                arestas.append((origem, destino, custo))
            return num_vertices, arestas
    except FileNotFoundError:
        print(f"Erro: O arquivo de grafo '{caminho_arquivo}' não foi encontrado.")
        raise
    except Exception as e:
        print(f"Erro ao ler o grafo: {e}")
        raise

def bellman_ford(num_vertices: int, arestas: List[Tuple[int, int, int]], no_inicio: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Executa o algoritmo de Bellman-Ford para encontrar o caminho de menor custo
    a partir de um único nó de origem em um grafo com pesos negativos.
    """
    distancias = {i: float('inf') for i in range(num_vertices)}
    antecessores = {i: None for i in range(num_vertices)}
    distancias[no_inicio] = 0

    # Relaxa as arestas repetidamente (V-1 vezes)
    for _ in range(num_vertices - 1):
        for origem, destino, custo in arestas:
            if distancias[origem] != float('inf') and distancias[origem] + custo < distancias[destino]:
                distancias[destino] = distancias[origem] + custo
                antecessores[destino] = origem

    # Opcional: Verifica por ciclos de peso negativo.
    # Se uma distância ainda puder ser reduzida, um ciclo negativo existe.
    for origem, destino, custo in arestas:
        if distancias[origem] != float('inf') and distancias[origem] + custo < distancias[destino]:
            raise ValueError("O grafo contém um ciclo de peso negativo.")

    return distancias, antecessores

def reconstruir_caminho(antecessores: Dict[int, Optional[int]], no_inicio: int, no_objetivo: int) -> Caminho:
    """
    Reconstrói o caminho do objetivo até o início a partir do dicionário 'antecessores'.
    """
    if antecessores.get(no_objetivo) is None and no_objetivo != no_inicio:
        return None  # Nenhum caminho encontrado

    caminho = []
    atual = no_objetivo
    while atual is not None:
        caminho.append(atual)
        atual = antecessores.get(atual)
    
    # Se o início não foi alcançado, o caminho não é válido
    if caminho[-1] != no_inicio:
        return None

    return caminho[::-1] # Retorna o caminho do início para o fim

def main():
    """
    Função principal para executar o programa para o Cenário 2.
    """
    parser = argparse.ArgumentParser(description="Encontra o caminho de menor custo em um grafo com pesos negativos usando Bellman-Ford.")
    parser.add_argument(
        "caminho_arquivo", 
        nargs='?', 
        default="graph2.txt", 
        help="Caminho para o arquivo de grafo. Padrão: 'graph2.txt'"
    )
    args = parser.parse_args()

    try:
        nome_arquivo_grafo = args.caminho_arquivo
        diretorio_do_script = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.join(diretorio_do_script, nome_arquivo_grafo)
        num_vertices, arestas = ler_grafo_do_arquivo(caminho_completo)
    except (FileNotFoundError, ValueError):
        return

    no_inicio = 0
    no_objetivo = 6

    try:
        distancias, antecessores = bellman_ford(num_vertices, arestas, no_inicio)
        custo_total = distancias.get(no_objetivo)

        if custo_total == float('inf'):
            print(f"Não foi possível encontrar um caminho do vértice {no_inicio} ao {no_objetivo}.")
        else:
            caminho = reconstruir_caminho(antecessores, no_inicio, no_objetivo)
            if caminho:
                print(f"Somatório do custo do caminho: {custo_total}")
                print(f"Caminho mínimo: {' -> '.join(map(str, caminho))}")
            else:
                 print(f"Não foi possível reconstruir um caminho do vértice {no_inicio} ao {no_objetivo}.")

    except ValueError as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()