# =============================================================================
# fitness.py — Funções de distância e avaliação de rotas
#
# O fitness de uma rota é a sua distância total — quanto menor, melhor.
# Duas funções de distância são oferecidas:
#   - Euclidiana simples: para pontos aleatórios
#   - ATT (pseudo-euclidiana): para o benchmark att48 da TSPLIB
# =============================================================================

import math


def calculate_distance(city1, city2):
    """
    Calcula a distância euclidiana entre dois pontos no plano.

    Fórmula: √((x2-x1)² + (y2-y1)²)

    Usada para o dataset de pontos aleatórios, onde as coordenadas
    são inteiros entre 0 e 100 sem escala específica.

    Parâmetros:
        city1, city2 — tuplas (x, y) com as coordenadas dos pontos

    Retorna:
        Distância em ponto flutuante
    """
    return math.sqrt(
        (city1[0] - city2[0]) ** 2 +
        (city1[1] - city2[1]) ** 2
    )


def calculate_distance_att(city1, city2):
    """
    Calcula a distância ATT (pseudo-euclidiana) usada no benchmark att48.

    Definida pela TSPLIB para aproximar distâncias reais de rodovias,
    essa fórmula divide a distância euclidiana por √10 e arredonda
    com uma regra especial: se o arredondamento para baixo for menor
    que o valor real, soma 1 (garante que nunca subestima a distância).

    Fórmula:
        rij = √((dx² + dy²) / 10)
        tij = round(rij)
        se tij < rij → retorna tij + 1
        caso contrário → retorna tij

    Parâmetros:
        city1, city2 — tuplas (x, y) com as coordenadas das cidades

    Retorna:
        Distância inteira conforme a convenção ATT da TSPLIB
    """
    dx = city1[0] - city2[0]
    dy = city1[1] - city2[1]

    rij = math.sqrt((dx * dx + dy * dy) / 10.0)
    tij = round(rij)

    # Regra especial da TSPLIB: arredonda para cima se necessário
    if tij < rij:
        return tij + 1
    else:
        return tij


def calculate_fitness(route, cities, distance_function):
    """
    Calcula o fitness de uma rota como a soma das distâncias entre
    todos os pontos consecutivos, incluindo o retorno ao ponto inicial.

    O fitness é a distância total do percurso completo:
        cidade[0] → cidade[1] → ... → cidade[n-1] → cidade[0]

    Quanto menor o fitness, melhor a rota — o algoritmo genético
    busca minimizar esse valor ao longo das gerações.

    Parâmetros:
        route             — lista de índices representando a ordem de visita
        cities            — lista de tuplas (x, y) com as coordenadas
        distance_function — função de distância a usar (euclidiana ou ATT)

    Retorna:
        Distância total do percurso (float ou int dependendo da função usada)
    """
    total_distance = 0

    for i in range(len(route)):
        city1 = cities[route[i]]
        # (i + 1) % len(route) garante que o último ponto retorna ao primeiro
        city2 = cities[route[(i + 1) % len(route)]]
        total_distance += distance_function(city1, city2)

    return total_distance
