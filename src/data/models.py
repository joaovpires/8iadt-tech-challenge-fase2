"""
Modelos de dados para o sistema de otimização de rotas hospitalares.
Define as estruturas de entregas, veículos e resultados.
"""
from dataclasses import dataclass, field


@dataclass
class DeliveryPoint:
    """Ponto de entrega de medicamento/insumo."""
    id: int
    name: str
    latitude: float
    longitude: float
    priority: str          # "critica", "alta", "media", "baixa"
    demand: float          # peso em kg da carga a entregar
    time_window: tuple = None  # (hora_inicio, hora_fim) opcional


@dataclass
class Vehicle:
    """Veículo disponível para entregas."""
    id: int
    name: str
    capacity: float        # capacidade máxima em kg
    max_distance: float    # autonomia em km


@dataclass
class Route:
    """Rota atribuída a um veículo."""
    vehicle: Vehicle
    stops: list            # lista de DeliveryPoint (em ordem de visita)
    total_distance: float = 0.0
    total_load: float = 0.0
    sequence: list = field(default_factory=list)  # índices dos pontos


@dataclass
class OptimizationResult:
    """Resultado completo da otimização."""
    routes: list                  # lista de Route
    best_fitness: float = 0.0
    generations: int = 0
    fitness_history: list = field(default_factory=list)  # fitness por geração
    initial_distance: float = 0.0
    optimized_distance: float = 0.0
