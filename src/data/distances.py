"""
Módulo de cálculo de distâncias entre pontos de entrega.
"""
import math

from src.data.models import DeliveryPoint


def haversine(point_a: DeliveryPoint, point_b: DeliveryPoint) -> float:
    """
    Calcula distância em km entre dois pontos usando a fórmula de Haversine.
    """
    R = 6371.0  # raio da Terra em km

    lat1 = math.radians(point_a.latitude)
    lat2 = math.radians(point_b.latitude)
    dlat = math.radians(point_b.latitude - point_a.latitude)
    dlon = math.radians(point_b.longitude - point_a.longitude)

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def build_distance_matrix(points: list[DeliveryPoint]) -> list[list[float]]:
    """
    Constrói a matriz de distâncias entre todos os pontos.
    """
    n = len(points)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = haversine(points[i], points[j])
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix


def route_total_distance(
    sequence: list[int], distance_matrix: list[list[float]]
) -> float:
    """
    Calcula distância total de uma rota (ida e volta ao depósito).
    sequence: lista de índices dos pontos, sem incluir o depósito (0).
    """
    if not sequence:
        return 0.0
    full = [0] + sequence + [0]
    return sum(distance_matrix[full[i]][full[i + 1]] for i in range(len(full) - 1))
