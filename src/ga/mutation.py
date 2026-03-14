# =============================================================================
# mutation.py — Operador de Mutação do Algoritmo Genético
#
# A mutação introduz variação aleatória na população para evitar que
# o algoritmo fique preso em mínimos locais (soluções boas mas não ótimas).
# =============================================================================

import random


def mutate(route, mutation_probability):
    """
    Mutação por inversão de segmento — também conhecida como 2-opt swap.

    Por que inverter um segmento e não trocar duas cidades?
    Trocar duas cidades aleatórias frequentemente cria cruzamentos
    de arestas na rota, tornando-a mais longa. Inverter um segmento
    tende a desfazer esses cruzamentos, gerando soluções melhores
    — é a base do algoritmo 2-opt de otimização local.

    Como funciona:
        1. Com probabilidade mutation_probability, aplica a mutação
        2. Sorteia dois pontos de corte i e j (i < j)
        3. Inverte o segmento entre i e j

    Exemplo:
        Rota original: [0, 1, 2, 3, 4, 5]
        Pontos de corte: i=1, j=4
        Segmento invertido: [1, 2, 3] → [3, 2, 1]
        Rota mutada:   [0, 3, 2, 1, 4, 5]

    Parâmetros:
        route                — lista de índices representando a rota
        mutation_probability — probabilidade de aplicar a mutação (0.0 a 1.0)
            0.0 = nunca muta (convergência rápida, risco de mínimo local)
            1.0 = sempre muta (exploração excessiva, convergência lenta)
            0.1–0.3 = faixa recomendada para o TSP

    Retorna:
        route — rota original (sem mutação) ou rota com segmento invertido
    """
    if random.random() < mutation_probability:
        # Sorteia dois índices distintos e garante i < j
        i, j = sorted(random.sample(range(len(route)), 2))

        # Inverte o segmento entre i (inclusivo) e j (exclusivo)
        route[i:j] = reversed(route[i:j])

    return route
