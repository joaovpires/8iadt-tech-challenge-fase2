from src.ga.vrp_fitness import evaluate_vrp_solution


def sequence_to_vrp_chromosome(sequence, deliveries, vehicles):
    delivery_map = {d.id: d for d in deliveries}

    chromosome = [0]
    vehicle_index = 0
    current_load = 0

    for client_id in sequence:
        if vehicle_index >= len(vehicles):
            chromosome.append(client_id)
            continue

        vehicle = vehicles[vehicle_index]
        demand = delivery_map[client_id].demand

        if current_load + demand <= vehicle.capacity:
            chromosome.append(client_id)
            current_load += demand
        else:
            chromosome.append(0)
            vehicle_index += 1
            chromosome.append(client_id)
            current_load = demand

    chromosome.append(0)
    return chromosome


def evaluate_sequence_solution(sequence, deliveries, vehicles):
    chromosome = sequence_to_vrp_chromosome(sequence, deliveries, vehicles)
    result = evaluate_vrp_solution(chromosome, deliveries, vehicles)
    result["sequence"] = sequence
    result["chromosome"] = chromosome
    return result