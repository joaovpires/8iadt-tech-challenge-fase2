"""
Adaptador que conecta o VRP da Bruna com as visualizacoes do Matheus.

Converte DeliveryPoint/Vehicle para Delivery/Vehicle (Bruna),
executa o run_ga_vrp e devolve OptimizationResult com distancias reais em km.
"""
import math

from src.data.models import DeliveryPoint, Vehicle, Route, OptimizationResult

PRIORITY_MAP = {"critica": 1, "alta": 2, "media": 3, "baixa": 4, "base": 0}


def run_genetic_algorithm(
    points: list[DeliveryPoint],
    vehicles: list[Vehicle],
    population_size: int = 100,
    generations: int = 200,
    mutation_rate: float = 0.2,
    seed: int = 42,
) -> OptimizationResult:
    from src.ga.vrp_models import Delivery, Vehicle as BrunaVehicle
    from src.ga.algorithm_vrp import run_ga_vrp

    deliveries = [
        Delivery(
            id=p.id,
            x=p.longitude,
            y=p.latitude,
            demand=p.demand,
            priority=PRIORITY_MAP.get(p.priority, 3),
        )
        for p in points
    ]

    bruna_vehicles = [
        BrunaVehicle(id=i + 1, capacity=v.capacity, max_distance=v.max_distance)
        for i, v in enumerate(vehicles)
    ]

    history, best_solutions = run_ga_vrp(
        deliveries=deliveries,
        vehicles=bruna_vehicles,
        population_size=population_size,
        mutation_probability=mutation_rate,
        max_generations=generations,
        selection_type="tournament",
    )

    initial_solution = best_solutions[0]
    best_solution = min(best_solutions, key=lambda s: s["fitness"])

    initial_routes = _build_routes(initial_solution["routes"], points, vehicles)
    initial_distance = sum(r.total_distance for r in initial_routes)

    optimized_routes = _build_routes(best_solution["routes"], points, vehicles)
    optimized_distance = sum(r.total_distance for r in optimized_routes)

    return OptimizationResult(
        routes=optimized_routes,
        initial_distance=initial_distance,
        optimized_distance=optimized_distance,
        fitness_history=history,
        generations=generations,
    )


def _build_routes(
    vrp_routes: list[list[int]],
    points: list[DeliveryPoint],
    vehicles: list[Vehicle],
) -> list[Route]:
    point_map = {p.id: p for p in points}
    base = points[0]
    routes = []

    for i, raw_route in enumerate(vrp_routes):
        if i >= len(vehicles):
            break
        vehicle = vehicles[i]
        stop_ids = [g for g in raw_route if g != 0]
        stops = [point_map[sid] for sid in stop_ids if sid in point_map]
        routes.append(Route(
            vehicle=vehicle,
            stops=stops,
            sequence=[s.id for s in stops],
            total_distance=_calc_route_distance(base, stops),
            total_load=sum(s.demand for s in stops),
        ))

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
    if not stops:
        return 0.0

    def haversine(p1, p2):
        R = 6371
        lat1, lon1 = math.radians(p1.latitude), math.radians(p1.longitude)
        lat2, lon2 = math.radians(p2.latitude), math.radians(p2.longitude)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return R * 2 * math.asin(math.sqrt(a))

    dist = haversine(base, stops[0])
    for i in range(len(stops) - 1):
        dist += haversine(stops[i], stops[i + 1])
    dist += haversine(stops[-1], base)
    return dist