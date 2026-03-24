from vrp_utils import (
    euclidean,
    split_routes_by_depot,
    build_points,
    count_missing_clients,
    count_duplicate_clients,
)


def evaluate_vrp_solution(
    chromosome,
    deliveries,
    vehicles,
    penalty_capacity=1000,
    penalty_distance=1000,
    penalty_priority=50,
    penalty_missing=5000,
    penalty_duplicate=3000,
    penalty_extra_routes=4000,
):
    points = build_points(deliveries)
    routes = split_routes_by_depot(chromosome)

    total_distance = 0
    penalty = 0

    if len(routes) > len(vehicles):
        penalty += (len(routes) - len(vehicles)) * penalty_extra_routes

    for i, route in enumerate(routes):
        if i >= len(vehicles):
            break

        vehicle = vehicles[i]
        load = 0
        route_distance = 0

        for j in range(len(route) - 1):
            current_id = route[j]
            next_id = route[j + 1]

            current_point = points[current_id]
            next_point = points[next_id]

            route_distance += euclidean(current_point, next_point)

            if current_id != 0:
                load += current_point.demand

                if current_point.priority == 1:
                    penalty += j * penalty_priority
                elif current_point.priority == 2:
                    penalty += j * (penalty_priority / 2)

        total_distance += route_distance

        if load > vehicle.capacity:
            penalty += (load - vehicle.capacity) * penalty_capacity

        if route_distance > vehicle.max_distance:
            penalty += (route_distance - vehicle.max_distance) * penalty_distance

    missing = count_missing_clients(chromosome, deliveries)
    penalty += missing * penalty_missing

    duplicates = count_duplicate_clients(chromosome)
    penalty += duplicates * penalty_duplicate

    fitness = total_distance + penalty

    return {
        "routes": routes,
        "total_distance": total_distance,
        "penalty": penalty,
        "fitness": fitness,
        "missing_clients": missing,
        "duplicate_clients": duplicates,
    }


def calculate_vrp_fitness(
    chromosome,
    deliveries,
    vehicles,
    penalty_capacity=1000,
    penalty_distance=1000,
    penalty_priority=50,
    penalty_missing=5000,
    penalty_duplicate=3000,
    penalty_extra_routes=4000,
):
    result = evaluate_vrp_solution(
        chromosome=chromosome,
        deliveries=deliveries,
        vehicles=vehicles,
        penalty_capacity=penalty_capacity,
        penalty_distance=penalty_distance,
        penalty_priority=penalty_priority,
        penalty_missing=penalty_missing,
        penalty_duplicate=penalty_duplicate,
        penalty_extra_routes=penalty_extra_routes,
    )
    return result["fitness"]