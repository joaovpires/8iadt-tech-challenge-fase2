# =============================================================================
# selection.py — Operadores de Seleção do Algoritmo Genético
#
# A seleção escolhe quais indivíduos da população atual serão os "pais"
# da próxima geração. O objetivo é favorecer os melhores (menor distância)
# sem eliminar completamente os piores — manter pressão seletiva sem
# perder diversidade genética.
#
# Três métodos estão disponíveis, cada um com trade-offs diferentes.
# =============================================================================

import random


# =============================================================================
# MÉTODO 1 — Torneio (recomendado para o TSP)
# =============================================================================
def tournament_selection(population, fitness, k):
    """
    Seleção por torneio: sorteia k indivíduos aleatoriamente e
    retorna o melhor (menor distância) entre eles.

    Vantagens:
        - Controle fácil da pressão seletiva via parâmetro k
          k pequeno (2-3): baixa pressão, mais diversidade
          k grande (10+): alta pressão, converge mais rápido
        - Não é afetado por outliers (indivíduos extremamente bons ou ruins)
        - Funciona bem mesmo com fitness muito próximos entre si

    É o método padrão do projeto (k=3).

    Parâmetros:
        population — lista de rotas (cada rota é uma lista de índices)
        fitness    — lista de distâncias correspondentes a cada rota
        k          — tamanho do torneio (quantos competidores por rodada)

    Retorna:
        A melhor rota entre os k selecionados aleatoriamente
    """
    # Sorteia k pares (rota, distância) sem reposição
    selected = random.sample(list(zip(population, fitness)), k)

    # Ordena pelo fitness (menor distância = melhor)
    selected.sort(key=lambda x: x[1])

    # Retorna apenas a rota do vencedor (sem o fitness)
    return selected[0][0]


# =============================================================================
# MÉTODO 2 — Top 10 (seleção elitista)
# =============================================================================
def top_10_selection(population, fitness):
    """
    Seleção elitista: escolhe aleatoriamente entre os 10 melhores
    indivíduos da população atual.

    Vantagens:
        - Garante que apenas soluções de alta qualidade se reproduzem
        - Converge mais rápido que o torneio

    Desvantagens:
        - Alta pressão seletiva pode reduzir diversidade rapidamente
        - Risco maior de convergência prematura para um mínimo local
        - Pouco escalável: com população de 500, usa sempre só os 10 melhores

    Parâmetros:
        population — lista de rotas ordenada do melhor para o pior
        fitness    — lista de distâncias correspondentes

    Retorna:
        Uma rota escolhida aleatoriamente entre as 10 melhores
    """
    # A população já chega ordenada do melhor para o pior (feito em algorithm.py)
    top10 = list(zip(population, fitness))[:10]

    # Escolhe aleatoriamente entre os 10 (evita sempre pegar o mesmo)
    return random.choice(top10)[0]


# =============================================================================
# MÉTODO 3 — Roleta (seleção proporcional ao fitness)
# =============================================================================
def roulette_selection(population, fitness):
    """
    Seleção por roleta: cada indivíduo tem probabilidade de ser escolhido
    proporcional à sua qualidade (fitness).

    Como o objetivo é minimizar a distância (não maximizar), o fitness
    é invertido (1/distância) antes de calcular as probabilidades —
    rotas mais curtas ficam com probabilidade maior.

    Vantagens:
        - Todos os indivíduos têm chance de se reproduzir
        - Preserva mais diversidade que o top10

    Desvantagens:
        - Se um indivíduo for muito melhor que os demais, domina a roleta
          e reduz diversidade (problema do "super-indivíduo")
        - Sensível à escala dos valores de fitness

    Parâmetros:
        population — lista de rotas
        fitness    — lista de distâncias (valores positivos)

    Retorna:
        Uma rota selecionada com probabilidade proporcional à sua qualidade
    """
    # Inverte o fitness: 1/distância (rotas menores = peso maior)
    inverted = [1 / f for f in fitness]
    total    = sum(inverted)

    # Normaliza para obter probabilidades que somam 1.0
    probs = [f / total for f in inverted]

    # Escolhe uma rota com as probabilidades calculadas
    return random.choices(population, weights=probs, k=1)[0]
