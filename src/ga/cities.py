# =============================================================================
# cities.py — Geração e carregamento dos pontos de entrega
#
# Fornece dois modos de dataset para o algoritmo:
#   1. Aleatório: pontos gerados na hora, útil para testes rápidos
#   2. att48: benchmark real da TSPLIB com solução ótima conhecida (10.628)
# =============================================================================

import random


def generate_cities(n):
    """
    Gera n pontos de entrega com coordenadas aleatórias entre 0 e 100.

    Cada ponto representa um local de entrega de medicamentos.
    As coordenadas são inteiras para simplificar a visualização.

    Parâmetros:
        n — número de pontos a gerar

    Retorna:
        Lista de n tuplas (x, y)
    """
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]


def load_att48():
    """
    Carrega as 48 cidades do benchmark att48 da TSPLIB.

    O att48 é um problema clássico de otimização de rotas baseado
    em coordenadas reais de cidades americanas. É amplamente usado
    para avaliar e comparar algoritmos de TSP.

    Características:
        - 48 cidades com coordenadas em escala maior (0–8000)
        - Distância calculada com fórmula pseudo-euclidiana (ATT)
        - Melhor solução conhecida (ótimo global): 10.628
        - Qualquer solução acima disso é subótima

    A fórmula ATT difere da euclidiana comum: divide por √10 e arredonda,
    o que aproxima distâncias reais de rodovias americanas da época.

    Retorna:
        Lista de 48 tuplas (x, y) com as coordenadas das cidades
    """
    return [
        (6734, 1453), (2233,   10), (5530, 1424), ( 401,  841), (3082, 1644),
        (7608, 4458), (7573, 3716), (7265, 1268), (6898, 1885), (1112, 2049),
        (5468, 2606), (5989, 2873), (4706, 2674), (4612, 2035), (6347, 2683),
        (6107,  669), (7611, 5184), (7462, 3590), (7732, 4723), (5900, 3561),
        (4483, 3369), (6101, 1110), (5199, 2182), (1633, 2809), (4307, 2322),
        ( 675, 1006), (7555, 4819), (7541, 3981), (3177,  756), (7352, 4506),
        (7545, 2801), (3245, 3305), (6426, 3173), (4608, 1198), (  23, 2216),
        (7248, 3779), (7762, 4595), (7392, 2244), (3484, 2829), (6271, 2135),
        (4985,  140), (1916, 1569), (7280, 4899), (7509, 3239), (  10, 2676),
        (6807, 2993), (5185, 3258), (3023, 1942)
    ]
