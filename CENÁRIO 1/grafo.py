import heapq

#Funções para o Cenário 1: Determinando a estação central
#Implementação de funções para a resolução do problema usando o Algoritmo de Dijkstra.

def criar_grafo_a_partir_de_arquivo(caminho_arquivo):
  
    grafo = {}
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
        if not linhas:
            return {}, 0
        try:
            num_vertices, num_arestas = map(int, linhas[0].split())
        except ValueError:
            print("Erro: A primeira linha do arquivo deve conter o número de vértices e arestas.")
            return {}, 0
        
        for linha in linhas[1:]:
            partes = linha.split()
            if len(partes) != 3:
                continue #ignora linhas mal formatadas
            u, v, custo_str = partes
            try:
                custo = int(custo_str)
            except ValueError:
                print(f"Erro: O custo na linha '{linha.strip()}' não é um número válido.")
                continue

            #adiciona o vértice ao grafo se ele ainda não existir
            if u not in grafo:
                grafo[u] = []
            if v not in grafo:
                grafo[v] = []
            
            #como o grafo é não-direcionado, a aresta é bidirecional
            grafo[u].append((v, custo))
            grafo[v].append((u, custo))
            
    return grafo, num_vertices

def dijkstra(grafo, s):
    
    distancias = {vertice: float('inf') for vertice in grafo}
    distancias[s] = 0
    
    fila_prioridade = [(0, s)]
    
    while fila_prioridade:
        
        dist_atual, u = heapq.heappop(fila_prioridade)

        #se a distância atual é maior do que a ja registrada, ignora
        if dist_atual > distancias[u]:
            continue
            
       
        for v, peso in grafo[u]:
            distancia_nova = distancias[u] + peso
            if distancia_nova < distancias[v]:
                distancias[v] = distancia_nova
                heapq.heappush(fila_prioridade, (distancia_nova, v))
                
    return distancias

#loggica para encontrar o vértice central e gerar os resultados
def encontrar_vertice_central(caminho_arquivo):
    grafo, num_vertices = criar_grafo_a_partir_de_arquivo(caminho_arquivo)
    
    if not grafo:
        return None

    #matriz pra armazenar as distâncias mínimas
    matriz_distancias = {}
    
    #variaveis pra o resultado final
    vertice_central = None
    menor_custo_total = float('inf')
    
    vertices = sorted(list(grafo.keys()))
    
    for candidato in vertices:
        #executa o Dijkstra a partir do vértice candidato
        distancias = dijkstra(grafo, candidato)
        matriz_distancias[candidato] = distancias
        
        #calcula o custo total para este candidato
        custo_total = sum(d for d in distancias.values() if d != float('inf'))
        
        #wncontra o vértice central (com o menor custo total)
        if custo_total < menor_custo_total:
            menor_custo_total = custo_total
            vertice_central = candidato

    distancias_central = matriz_distancias.get(vertice_central, {})
    
    #encontra o vértice mais distante da estação central
    vertice_mais_distante = max(distancias_central, key=distancias_central.get, default=None)
    distancia_mais_distante = distancias_central.get(vertice_mais_distante, float('inf'))

    return {
        "vertice_central": vertice_central,
        "distancias_da_central": distancias_central,
        "vertice_mais_distante": vertice_mais_distante,
        "distancia_mais_distante": distancia_mais_distante,
        "matriz_distancias": matriz_distancias,
        "vertices_ordenados": vertices
    }

if __name__ == "__main__":
    caminho_do_arquivo_exemplo = 'graph1.txt' # O arquivo anexo
    resultados = encontrar_vertice_central(caminho_do_arquivo_exemplo)
    
    if resultados and resultados["vertice_central"]:
        print("Vértice Central:", resultados["vertice_central"])
        print("\nVetor de distâncias da estação central:", resultados["distancias_da_central"])
        print(f"\nVértice mais distante: {resultados['vertice_mais_distante']} com distância {resultados['distancia_mais_distante']}")
        print("\nMatriz de distâncias mínimas:")
    
        vertices_ordenados = resultados["vertices_ordenados"]
        print("Candidato\t" + "\t\t".join(vertices_ordenados))
        for candidato in vertices_ordenados:
            distancias = resultados["matriz_distancias"][candidato]
            linha = [str(distancias[v]) for v in vertices_ordenados]
            print(f"{candidato}\t\t" + "\t\t".join(linha))
    else:
        print("Não foi possível encontrar o vértice central. Verifique o arquivo de entrada.")