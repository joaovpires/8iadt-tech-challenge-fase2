import random


def generate_vrp_population(num_clients, num_vehicles, population_size):
    population = []

    base_clients = list(range(1, num_clients + 1))

    for _ in range(population_size):
        clients = base_clients[:]
        random.shuffle(clients)

        chunks = [[] for _ in range(num_vehicles)]
        for idx, client in enumerate(clients):
            chunks[idx % num_vehicles].append(client)

        chromosome = []
        for chunk in chunks:
            chromosome.append(0)
            chromosome.extend(chunk)
        chromosome.append(0)

        population.append(chromosome)

    return population