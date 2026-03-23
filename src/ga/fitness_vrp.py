import math


def distancia_euclidiana(ponto_a, ponto_b):
    return math.sqrt((ponto_a["x"] - ponto_b["x"]) ** 2 + (ponto_a["y"] - ponto_b["y"]) ** 2)


def calcular_distancia_rota(rota, entregas, deposito=None):
    if not rota:
        return 0

    distancia_total = 0

    if deposito is not None:
        distancia_total += distancia_euclidiana(deposito, entregas[rota[0]])

    for i in range(len(rota) - 1):
        distancia_total += distancia_euclidiana(entregas[rota[i]], entregas[rota[i + 1]])

    if deposito is not None:
        distancia_total += distancia_euclidiana(entregas[rota[-1]], deposito)

    return distancia_total


def calcular_fitness_vrp(
    rotas,
    entregas,
    veiculos,
    deposito=None,
    peso_capacidade=1000,
    peso_autonomia=1000,
    peso_prioridade=10,
):
    distancia_total = 0
    penalidade_capacidade = 0
    penalidade_autonomia = 0
    penalidade_prioridade = 0

    for i, rota in enumerate(rotas):
        veiculo = veiculos[i]

        carga_total = sum(entregas[ponto]["demanda"] for ponto in rota)
        distancia_rota = calcular_distancia_rota(rota, entregas, deposito)

        distancia_total += distancia_rota

        if carga_total > veiculo["capacidade"]:
            penalidade_capacidade += carga_total - veiculo["capacidade"]

        if distancia_rota > veiculo["autonomia_maxima"]:
            penalidade_autonomia += distancia_rota - veiculo["autonomia_maxima"]

        for posicao, ponto in enumerate(rota):
            prioridade = entregas[ponto]["prioridade"]
            penalidade_prioridade += prioridade * (posicao + 1)

    fitness = (
        distancia_total
        + peso_capacidade * penalidade_capacidade
        + peso_autonomia * penalidade_autonomia
        + peso_prioridade * penalidade_prioridade
    )

    return fitness