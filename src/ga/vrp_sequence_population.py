import random


def generate_sequence_population(num_clients, population_size):
    population = []
    base_clients = list(range(1, num_clients + 1))

    for _ in range(population_size):
        individual = base_clients[:]
        random.shuffle(individual)
        population.append(individual)

    return population