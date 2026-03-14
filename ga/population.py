# =============================================================================
# population.py — Geração da população inicial do Algoritmo Genético
#
# A qualidade da população inicial impacta diretamente a velocidade
# de convergência. Uma população totalmente aleatória leva mais gerações
# para encontrar boas soluções; uma população com alguma estrutura
# converge mais rápido mas pode perder diversidade.
#
# Solução: população híbrida com três estratégias combinadas.
# =============================================================================

import random
import math
from .fitness import calculate_distance


# =============================================================================
# ESTRATÉGIA 1 — Rota Aleatória (40% da população)
# =============================================================================
def random_route(num_cities):
    """
    Gera uma rota completamente aleatória embaralhando os índices das cidades.

    Papel na população híbrida:
        Garante diversidade genética — sem rotas aleatórias, a população
        inicial seria muito homogênea e o algoritmo convergiria
        prematuramente para um mínimo local.

    Parâmetros:
        num_cities — número total de cidades/pontos de entrega

    Retorna:
        Lista de índices [0, 1, ..., n-1] em ordem aleatória
    """
    route = list(range(num_cities))
    random.shuffle(route)
    return route


# =============================================================================
# ESTRATÉGIA 2 — Nearest Neighbour / Vizinho Mais Próximo (40% da população)
# =============================================================================
def nearest_neighbour(cities):
    """
    Constrói uma rota gulosa partindo de uma cidade aleatória e sempre
    visitando a cidade mais próxima ainda não visitada.

    É um algoritmo heurístico simples que gera soluções razoáveis
    rapidamente, geralmente entre 20-25% acima do ótimo global.

    Limitação conhecida: tende a criar cruzamentos de arestas no final
    da rota, quando restam apenas cidades distantes entre si.
    O algoritmo genético irá corrigir esses cruzamentos ao longo das gerações.

    Parâmetros:
        cities — lista de tuplas (x, y) com as coordenadas

    Retorna:
        Lista de índices representando a rota gulosa
    """
    unvisited = list(range(len(cities)))
    current   = random.choice(unvisited)   # ponto de partida aleatório

    route = [current]
    unvisited.remove(current)

    while unvisited:
        # Encontra a cidade não visitada mais próxima da posição atual
        next_city = min(
            unvisited,
            key=lambda city: calculate_distance(cities[current], cities[city])
        )
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return route


# =============================================================================
# ESTRATÉGIA 3 — Convex Hull Aproximado (20% da população)
# =============================================================================
def convex_hull_approx(cities):
    """
    Gera uma rota ordenando as cidades por ângulo em relação ao centróide,
    aproximando um envoltório convexo (contorno externo do conjunto de pontos).

    Rotas em forma de "círculo" ao redor dos pontos tendem a ter menos
    cruzamentos, o que é uma boa característica para o TSP.

    Para evitar que todos os indivíduos gerados por esse método sejam
    idênticos — o que reduziria a diversidade da população — aplica uma
    pequena perturbação aleatória ao ângulo de cada cidade.

    Parâmetros:
        cities — lista de tuplas (x, y) com as coordenadas

    Retorna:
        Lista de índices ordenados por ângulo em relação ao centróide
    """
    # Calcula o centróide (ponto médio) de todas as cidades
    center_x = sum(c[0] for c in cities) / len(cities)
    center_y = sum(c[1] for c in cities) / len(cities)

    def angle(city):
        # Calcula o ângulo polar em relação ao centróide
        # Adiciona ruído para gerar variação entre indivíduos
        noise = random.uniform(-0.3, 0.3)
        return math.atan2(city[1] - center_y, city[0] - center_x) + noise

    # Ordena as cidades por ângulo (sentido anti-horário a partir de leste)
    indexed       = list(enumerate(cities))
    sorted_cities = sorted(indexed, key=lambda x: angle(x[1]))

    return [i for i, _ in sorted_cities]


# =============================================================================
# POPULAÇÃO HÍBRIDA
# =============================================================================
def generate_population(num_cities, population_size, cities):
    """
    Gera a população inicial combinando três estratégias de construção
    de rotas para equilibrar qualidade e diversidade.

    Composição:
        40% Nearest Neighbour  — rotas gulosas de boa qualidade inicial
        20% Convex Hull        — rotas com estrutura geográfica circular
        40% Aleatório          — rotas diversas para exploração ampla

    Por que misturar estratégias?
        - Só nearest neighbour: população homogênea, converge rápido mas
          pode ficar presa em mínimos locais similares
        - Só aleatório: muita diversidade mas ponto de partida ruim,
          leva mais gerações para convergir
        - Híbrido: aproveita o melhor dos dois mundos

    Parâmetros:
        num_cities      — número de cidades/pontos de entrega
        population_size — tamanho total da população
        cities          — lista de tuplas (x, y) com as coordenadas

    Retorna:
        Lista de population_size rotas (cada rota é uma lista de índices)
    """
    population = []

    # Calcula quantos indivíduos de cada tipo gerar
    n_nn   = int(population_size * 0.4)          # 40% nearest neighbour
    n_ch   = int(population_size * 0.2)          # 20% convex hull
    n_rand = population_size - n_nn - n_ch        # restante aleatório (≈40%)

    # Gera os indivíduos de cada estratégia
    for _ in range(n_nn):
        population.append(nearest_neighbour(cities))

    for _ in range(n_ch):
        population.append(convex_hull_approx(cities))

    for _ in range(n_rand):
        population.append(random_route(num_cities))

    return population
