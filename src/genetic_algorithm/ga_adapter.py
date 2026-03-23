"""
Adaptador que conecta o VRP da Bruna com as visualizações do Matheus.

Converte DeliveryPoint/Vehicle → Delivery/Vehicle (Bruna),
executa o AG usando o fitness dela, e devolve OptimizationResult.
"""
import sys
import os
import random
import math

from src.data.models import DeliveryPoint, Vehicle, Route, OptimizationResult

# Mapeamento de prioridade string → int (formato da Bruna)
PRIORITY_MAP = {"critica": 1, "alta": 2, "media": 3, "baixa": 4, "base": 0}


def run_genetic_algorithm(
    points: list[DeliveryPoint],
    vehicles: list[Vehicle],
    population_size: int = 100,
    generations: int = 200,
    mutation_rate: float = 0.2,
    seed: int = 42,
) -> OptimizationResult:
    """
    Ponto de entrada compatível com main.py.
    Usa o modelo VRP da Bruna e devolve OptimizationResult para as visualizações.
    """
    random.seed(seed)

    # Adiciona src/ ao path para importar os módulos da Bruna
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    from src.ga.vrp_models import Delivery, Vehicle as BrunaVehicle
    from src.ga.vrp_population import generate_vrp_population
    from src.ga.vrp_fitness import evaluate_vrp_solution

    # Converte DeliveryPoint → Delivery (Bruna usa x/y e priority int)
    deliveries = []
    for p in points:
        deliveries.append(Delivery(
            id=p.id,
            x=p.longitude,  # longitude como x
            y=p.latitude,   # latitude como y
            demand=p.demand,
            priority=PRIORITY_MAP.get(p.priority, 3),
        ))

    # Converte Vehicle → Vehicle da Bruna
    bruna_vehicles = []
    for i, v in enumerate(vehicles):
        bruna_vehicles.append(BrunaVehicle(
            id=i + 1,
            capacity=v.capacity,
            max_distance=v.max_distance,
        ))

    num_clients = len(deliveries) - 1  # descontando o depósito (id=0)

    # Geração da população inicial
    population = generate_vrp_population(
        num_clients=num_clients,
        num_vehicles=len(bruna_vehicles),
        population_size=population_size,
    )

    # Avalia solução inicial (sem otimização) para o comparativo
    initial_result = evaluate_vrp_solution(population[0], deliveries, bruna_vehicles)
    initial_distance = initial_result["total_distance"]

    # Salva cromossomo inicial antes do loop para o comparativo
    initial_chromosome = population[0][:]

    # Loop do AG usando o fitness da Bruna
    fitness_history = []
    best_chromosome = population[0]
    best_fitness = float("inf")

    for _ in range(generations):
        # Avalia todos
        scored = [
            (chrom, evaluate_vrp_solution(chrom, deliveries, bruna_vehicles)["fitness"])
            for chrom in population
        ]
        scored.sort(key=lambda x: x[1])

        gen_best_fitness = scored[0][1]
        fitness_history.append(gen_best_fitness)

        if gen_best_fitness < best_fitness:
            best_fitness = gen_best_fitness
            best_chromosome = scored[0][0]

        # Elitismo: top 20% passa direto
        elite_size = max(1, population_size // 5)
        new_pop = [c for c, _ in scored[:elite_size]]

        # Preenche o resto com cruzamento + mutação
        while len(new_pop) < population_size:
            p1 = random.choice(scored[:elite_size * 2])[0]
            p2 = random.choice(scored[:elite_size * 2])[0]
            child = _order_crossover(p1, p2)
            child = _mutate(child, mutation_rate)
            new_pop.append(child)

        population = new_pop

    # Converte o melhor cromossomo para OptimizationResult
    best_eval = evaluate_vrp_solution(best_chromosome, deliveries, bruna_vehicles)

    routes = _build_routes(best_eval["routes"], points, vehicles)
    optimized_distance = sum(r.total_distance for r in routes)

    # Distância inicial: cromossomo antes do AG
    initial_eval = evaluate_vrp_solution(initial_chromosome, deliveries, bruna_vehicles)
    initial_routes = _build_routes(initial_eval["routes"], points, vehicles)
    initial_distance = sum(r.total_distance for r in initial_routes)

    return OptimizationResult(
        routes=routes,
        initial_distance=initial_distance,
        optimized_distance=optimized_distance,
        fitness_history=fitness_history,
        generations=generations,
    )


def _order_crossover(p1: list, p2: list) -> list:
    """OX adaptado para cromossomos VRP com depósitos (gene 0)."""
    # Extrai apenas os clientes (sem depósitos)
    clients1 = [g for g in p1 if g != 0]
    clients2 = [g for g in p2 if g != 0]

    if len(clients1) < 2:
        return p1[:]

    a, b = sorted(random.sample(range(len(clients1)), 2))
    segment = clients1[a:b]
    rest = [g for g in clients2 if g not in segment]
    new_clients = rest[:a] + segment + rest[a:]

    # Reconstrói o cromossomo com depósitos nas mesmas posições que p1
    depot_positions = [i for i, g in enumerate(p1) if g == 0]
    result = []
    client_idx = 0
    for i in range(len(p1)):
        if i in depot_positions:
            result.append(0)
        else:
            result.append(new_clients[client_idx])
            client_idx += 1

    return result


def _mutate(chromosome: list, rate: float) -> list:
    """Swap mutation: troca dois clientes aleatórios de posição."""
    chrom = chromosome[:]
    client_positions = [i for i, g in enumerate(chrom) if g != 0]
    if len(client_positions) < 2 or random.random() > rate:
        return chrom
    i, j = random.sample(client_positions, 2)
    chrom[i], chrom[j] = chrom[j], chrom[i]
    return chrom


def _build_routes(
    vrp_routes: list[list[int]],
    points: list[DeliveryPoint],
    vehicles: list[Vehicle],
) -> list[Route]:
    """Converte as rotas do formato da Bruna para Route do Matheus."""
    point_map = {p.id: p for p in points}
    base = points[0]
    routes = []

    for i, raw_route in enumerate(vrp_routes):
        if i >= len(vehicles):
            break

        vehicle = vehicles[i]
        # raw_route é algo como [0, 3, 1, 5, 0] — filtra os depósitos
        stop_ids = [g for g in raw_route if g != 0]
        stops = [point_map[sid] for sid in stop_ids if sid in point_map]

        total_load = sum(s.demand for s in stops)
        total_distance = _calc_route_distance(base, stops)
        sequence = [s.id for s in stops]

        routes.append(Route(
            vehicle=vehicle,
            stops=stops,
            sequence=sequence,
            total_distance=total_distance,
            total_load=total_load,
        ))

    # Se o VRP gerou menos rotas que veículos, preenche as vazias
    while len(routes) < len(vehicles):
        routes.append(Route(
            vehicle=vehicles[len(routes)],
            stops=[],
            sequence=[],
            total_distance=0.0,
            total_load=0.0,
        ))

    return routes


def _calc_route_distance(base: DeliveryPoint, stops: list[DeliveryPoint]) -> float:
    """Haversine: distância real em km para o cálculo das rotas."""
    def haversine(p1, p2):
        R = 6371
        lat1, lon1 = math.radians(p1.latitude), math.radians(p1.longitude)
        lat2, lon2 = math.radians(p2.latitude), math.radians(p2.longitude)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return R * 2 * math.asin(math.sqrt(a))

    if not stops:
        return 0.0

    dist = haversine(base, stops[0])
    for i in range(len(stops) - 1):
        dist += haversine(stops[i], stops[i + 1])
    dist += haversine(stops[-1], base)
    return dist
