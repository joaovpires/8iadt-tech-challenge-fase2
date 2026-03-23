from typing import List, Dict


def decodificar_cromossomo(cromossomo: List[int], separador: int = -1) -> List[List[int]]:
    """
    Converte um cromossomo linear em múltiplas rotas (uma por veículo).

    Exemplo:
        [0, 1, -1, 2, 3] -> [[0, 1], [2, 3]]
    """
    rotas = []
    rota_atual = []

    for gene in cromossomo:
        if gene == separador:
            rotas.append(rota_atual)
            rota_atual = []
        else:
            rota_atual.append(gene)

    rotas.append(rota_atual)
    return rotas


def criar_entregas_exemplo() -> Dict[int, Dict]:
    """
    Cria um conjunto de entregas com atributos logísticos.
    """
    return {
        0: {"id": 0, "x": 10, "y": 15, "demanda": 8, "prioridade": 3},
        1: {"id": 1, "x": 22, "y": 30, "demanda": 5, "prioridade": 2},
        2: {"id": 2, "x": 18, "y": 12, "demanda": 12, "prioridade": 1},
        3: {"id": 3, "x": 30, "y": 25, "demanda": 4, "prioridade": 3},
    }


def criar_veiculos_exemplo():
    """
    Cria uma lista de veículos com restrições operacionais.
    """
    return [
        {"id": "V1", "capacidade": 15, "autonomia_maxima": 80},
        {"id": "V2", "capacidade": 20, "autonomia_maxima": 100},
    ]