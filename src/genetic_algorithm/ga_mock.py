"""
Algoritmo Genético simplificado (MOCK) para o VRP.
Este é um placeholder para desenvolvimento e testes.
Será substituído pelo código da Karina (AG core) + Bruna (restrições).
"""
import random

from src.data.models import (
    DeliveryPoint, Vehicle, Route, OptimizationResult,
)
from src.data.distances import build_distance_matrix, route_total_distance


def run_genetic_algorithm(
    points: list[DeliveryPoint],
    vehicles: list[Vehicle],
    population_size: int = 50,
    generations: int = 100,
    mutation_rate: float = 0.1,
    seed: int = 42,
) -> OptimizationResult:
    """
    Executa um AG simplificado para VRP.

    Esse código serve para:
    - Matheus testar visualização e integração
    - João rodar experimentos iniciais

    Depois será substituído pelo AG real da Karina + restrições da Bruna.
    """
    random.seed(seed)
    n_points = len(points) - 1  # exclui o depósito (índice 0)
    dist_matrix = build_distance_matrix(points)

    # --- Atribuir pontos aos veículos por prioridade + capacidade ---
    assignments = _assign_points_to_vehicles(points, vehicles)

    # --- Calcular distância da solução inicial (ordem original) ---
    initial_distance = sum(
        route_total_distance(idxs, dist_matrix) for idxs in assignments.values()
    )

    # --- Otimizar cada rota com AG simples ---
    fitness_history = []
    optimized_assignments = {}

    for vid, point_indices in assignments.items():
        if len(point_indices) <= 1:
            optimized_assignments[vid] = point_indices
            continue

        best_route, history = _optimize_single_route(
            point_indices, dist_matrix, population_size, generations, mutation_rate,
        )
        optimized_assignments[vid] = best_route

        # Acumular histórico (somar fitness de todas as rotas por geração)
        if not fitness_history:
            fitness_history = history[:]
        else:
            for g in range(min(len(fitness_history), len(history))):
                fitness_history[g] += history[g]

    # --- Montar resultado ---
    routes = []
    optimized_distance = 0.0

    for vehicle in vehicles:
        indices = optimized_assignments.get(vehicle.id, [])
        stops = [points[i] for i in indices]
        total_dist = route_total_distance(indices, dist_matrix)
        total_load = sum(points[i].demand for i in indices)
        optimized_distance += total_dist

        routes.append(Route(
            vehicle=vehicle,
            stops=stops,
            total_distance=total_dist,
            total_load=total_load,
            sequence=indices,
        ))

    return OptimizationResult(
        routes=routes,
        best_fitness=optimized_distance,
        generations=generations,
        fitness_history=fitness_history,
        initial_distance=initial_distance,
        optimized_distance=optimized_distance,
    )


def _assign_points_to_vehicles(
    points: list[DeliveryPoint], vehicles: list[Vehicle],
) -> dict[int, list[int]]:
    """
    Atribui pontos de entrega aos veículos respeitando capacidade.
    Prioriza entregas críticas nos veículos com mais capacidade.
    """
    priority_order = {"critica": 0, "alta": 1, "media": 2, "baixa": 3}
    delivery_points = sorted(
        [(i, p) for i, p in enumerate(points) if i > 0],
        key=lambda x: priority_order.get(x[1].priority, 99),
    )

    assignments: dict[int, list[int]] = {v.id: [] for v in vehicles}
    remaining_capacity = {v.id: v.capacity for v in vehicles}

    # Veículos ordenados por capacidade decrescente
    sorted_vehicles = sorted(vehicles, key=lambda v: v.capacity, reverse=True)

    for idx, point in delivery_points:
        assigned = False
        for vehicle in sorted_vehicles:
            if remaining_capacity[vehicle.id] >= point.demand:
                assignments[vehicle.id].append(idx)
                remaining_capacity[vehicle.id] -= point.demand
                assigned = True
                break
        if not assigned:
            # Força atribuição ao veículo com mais espaço restante
            best_v = max(sorted_vehicles, key=lambda v: remaining_capacity[v.id])
            assignments[best_v.id].append(idx)
            remaining_capacity[best_v.id] -= point.demand

    return assignments


def _optimize_single_route(
    point_indices: list[int],
    dist_matrix: list[list[float]],
    pop_size: int,
    generations: int,
    mutation_rate: float,
) -> tuple[list[int], list[float]]:
    """
    AG simples para otimizar a ordem de visita de uma rota.
    Retorna (melhor_rota, histórico_fitness).
    """
    # Gerar população inicial
    population = [random.sample(point_indices, len(point_indices)) for _ in range(pop_size)]
    history = []

    for _ in range(generations):
        # Avaliar fitness (menor distância = melhor)
        fitness = [route_total_distance(ind, dist_matrix) for ind in population]
        best_fitness = min(fitness)
        history.append(best_fitness)

        # Seleção por torneio
        new_pop = []
        for __ in range(pop_size):
            a, b = random.sample(range(pop_size), 2)
            winner = population[a] if fitness[a] < fitness[b] else population[b]
            new_pop.append(winner[:])

        # Crossover (Order Crossover - OX)
        for i in range(0, pop_size - 1, 2):
            if random.random() < 0.8:
                new_pop[i], new_pop[i + 1] = _order_crossover(new_pop[i], new_pop[i + 1])

        # Mutação (swap)
        for ind in new_pop:
            if random.random() < mutation_rate and len(ind) > 1:
                a, b = random.sample(range(len(ind)), 2)
                ind[a], ind[b] = ind[b], ind[a]

        population = new_pop

    # Retornar o melhor
    fitness = [route_total_distance(ind, dist_matrix) for ind in population]
    best_idx = fitness.index(min(fitness))
    return population[best_idx], history


def _order_crossover(parent1: list[int], parent2: list[int]) -> tuple[list[int], list[int]]:
    """Order Crossover (OX) para permutação."""
    size = len(parent1)
    if size < 2:
        return parent1[:], parent2[:]

    a, b = sorted(random.sample(range(size), 2))
    child1 = [None] * size
    child2 = [None] * size

    child1[a:b + 1] = parent1[a:b + 1]
    child2[a:b + 1] = parent2[a:b + 1]

    def fill_child(child, parent):
        pos = (b + 1) % size
        for gene in parent:
            if gene not in child:
                child[pos] = gene
                pos = (pos + 1) % size

    fill_child(child1, parent2)
    fill_child(child2, parent1)
    return child1, child2
