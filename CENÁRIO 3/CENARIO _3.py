import heapq
import argparse
import os
from typing import List, Tuple, Dict, Optional

CELULA_INICIO = 'S'
CELULA_OBJETIVO = 'G'
CELULA_OBSTACULO = '#'
CELULA_NORMAL = '.'
CELULA_DIFICIL = '~'

GridMap = List[List[str]]
Coordenada = Tuple[int, int]
Caminho = Optional[List[Coordenada]]

def ler_mapa_do_arquivo(caminho_arquivo: str) -> Tuple[GridMap, Optional[Coordenada], Optional[Coordenada]]:
    try:
        with open(caminho_arquivo, 'r') as f:
            num_linhas_esperado, num_colunas_esperado = map(int, f.readline().split())
            linhas = [linha.strip() for linha in f if linha.strip()]
            mapa: GridMap = []
            inicio: Optional[Coordenada] = None
            objetivo: Optional[Coordenada] = None
            for r, linha in enumerate(linhas):
                mapa.append(list(linha))
                if CELULA_INICIO in linha:
                    inicio = (r, linha.find(CELULA_INICIO))
                if CELULA_OBJETIVO in linha:
                    objetivo = (r, linha.find(CELULA_OBJETIVO))
            return mapa, inicio, objetivo
    except FileNotFoundError:
        raise

def dijkstra_no_grid(mapa: GridMap, inicio: Coordenada, objetivo: Coordenada) -> Tuple[Dict[Coordenada, float], Dict[Coordenada, Optional[Coordenada]]]:
    num_linhas, num_colunas = len(mapa), len(mapa[0])
    custos_celula = {
        CELULA_NORMAL: 1, CELULA_DIFICIL: 3,
        CELULA_INICIO: 1, CELULA_OBJETIVO: 1
    }
    distancias = { (r, c): float('inf') for r in range(num_linhas) for c in range(num_colunas) }
    distancias[inicio] = 0
    fila_prioridade = [(0, inicio)]
    anterior = {inicio: None}
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while fila_prioridade:
        custo_atual, (linha_atual, coluna_atual) = heapq.heappop(fila_prioridade)
        if (linha_atual, coluna_atual) == objetivo: break
        if custo_atual > distancias[(linha_atual, coluna_atual)]: continue
        
        for dl, dc in movimentos:
            nova_linha, nova_coluna = linha_atual + dl, coluna_atual + dc
            if 0 <= nova_linha < num_linhas and 0 <= nova_coluna < num_colunas:
                celula_vizinha = mapa[nova_linha][nova_coluna]
                if celula_vizinha == CELULA_OBSTACULO: continue
                
                custo_aresta = custos_celula.get(celula_vizinha, 1)
                novo_custo_total = custo_atual + custo_aresta
                
                if novo_custo_total < distancias[(nova_linha, nova_coluna)]:
                    distancias[(nova_linha, nova_coluna)] = novo_custo_total
                    anterior[(nova_linha, nova_coluna)] = (linha_atual, coluna_atual)
                    heapq.heappush(fila_prioridade, (novo_custo_total, (nova_linha, nova_coluna)))
    return distancias, anterior

def reconstruir_caminho(anterior: Dict, inicio: Coordenada, objetivo: Coordenada) -> Caminho:
    if objetivo not in anterior: return None
    caminho = []
    atual = objetivo
    while atual is not None:
        caminho.append(atual)
        atual = anterior.get(atual)
    return caminho[::-1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("caminho_arquivo", nargs='?', default="grid_example.txt")
    args = parser.parse_args()

    try:
        nome_arquivo_mapa = args.caminho_arquivo
        diretorio_do_script = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.join(diretorio_do_script, nome_arquivo_mapa)
        mapa, inicio, objetivo = ler_mapa_do_arquivo(caminho_completo)
    except (FileNotFoundError, ValueError):
        return

    if inicio is None or objetivo is None:
        return

    distancias, anteriores = dijkstra_no_grid(mapa, inicio, objetivo)
    custo_total = distancias.get(objetivo, float('inf'))

    if custo_total != float('inf'):
        caminho = reconstruir_caminho(anteriores, inicio, objetivo)
        if caminho:
            print(f"Custo total: {int(custo_total)}")
            print(" -> ".join(map(str, caminho)))

if __name__ == "__main__":
    main()