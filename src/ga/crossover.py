# =============================================================================
# crossover.py — Operador de Cruzamento do Algoritmo Genético
#
# O cruzamento combina dois pais para gerar um filho que herda
# características de ambos — no TSP, isso significa preservar
# subsequências de cidades visitadas em ordem.
# =============================================================================

import random


def order_crossover(parent1, parent2):
    """
    Cruzamento OX (Order Crossover) — operador clássico para o TSP.

    Combina dois pais preservando a ordem relativa das cidades,
    o que é essencial para o TSP: simplesmente trocar genes como
    em cruzamento binário geraria rotas com cidades repetidas.

    Como funciona:
        1. Sorteia dois pontos de corte aleatórios (start, end)
        2. Copia o segmento parent1[start:end] direto para o filho
        3. Preenche o restante com as cidades do parent2,
           na ordem em que aparecem, pulando as que já estão no filho

    Exemplo com 6 cidades (start=1, end=4):
        parent1: [A, B, C, D, E, F]
        parent2: [C, D, B, F, A, E]

        Passo 1 — copia segmento de parent1:
            filho:  [_, B, C, D, _, _]

        Passo 2 — preenche com parent2 (pula B, C, D que já estão):
            ordem de parent2: C(skip), D(skip), B(skip), F, A, E
            filho:  [F, B, C, D, A, E]  ✓ sem repetições

    Parâmetros:
        parent1 — lista de índices representando a primeira rota pai
        parent2 — lista de índices representando a segunda rota pai

    Retorna:
        child — nova rota (lista de índices) com genes de ambos os pais
    """
    size = len(parent1)

    # Sorteia dois pontos de corte distintos e ordena (start < end)
    start, end = sorted(random.sample(range(size), 2))

    # Inicializa o filho com posições vazias (None)
    child = [None] * size

    # Copia o segmento central do parent1 para o filho
    child[start:end] = parent1[start:end]

    # Preenche as posições restantes com os genes do parent2
    # na ordem em que aparecem, ignorando os que já foram copiados
    pointer = 0
    for gene in parent2:
        if gene not in child:
            # Avança o ponteiro até a próxima posição vazia
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = gene

    return child
