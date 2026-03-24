from crossover import order_crossover
from mutation import mutate
from selection import (
    tournament_selection,
    top_10_selection,
    roulette_selection,
)
from vrp_adapter import evaluate_sequence_solution
from vrp_sequence_population import generate_sequence_population


def run_ga_vrp(
    deliveries,
    vehicles,
    population_size=100,
    mutation_probability=0.2,
    tournament_k=3,
    max_generations=100,
    selection_type="tournament",
):
    population = generate_sequence_population(
        num_clients=len(deliveries) - 1,
        population_size=population_size,
    )

    history = []
    best_solutions = []
    all_evaluated = []

    for _ in range(max_generations):
        evaluated = [
            evaluate_sequence_solution(ind, deliveries, vehicles)
            for ind in population
        ]

        ranked = sorted(
            zip(population, evaluated),
            key=lambda x: x[1]["fitness"]
        )

        population = [item[0] for item in ranked]
        evaluated = [item[1] for item in ranked]
        fitness_values = [item["fitness"] for item in evaluated]

        history.append(fitness_values[0])
        best_solutions.append(evaluated[0])
        all_evaluated.append(evaluated)

        new_population = [population[0]]

        while len(new_population) < population_size:
            if selection_type == "tournament":
                parent1 = tournament_selection(population, fitness_values, tournament_k)
                parent2 = tournament_selection(population, fitness_values, tournament_k)
            elif selection_type == "top10":
                parent1 = top_10_selection(population, fitness_values)
                parent2 = top_10_selection(population, fitness_values)
            elif selection_type == "roulette":
                parent1 = roulette_selection(population, fitness_values)
                parent2 = roulette_selection(population, fitness_values)
            else:
                raise ValueError("selection_type inválido")

            child = order_crossover(parent1, parent2)
            child = mutate(child, mutation_probability)
            new_population.append(child)

        population = new_population

    return history, best_solutions, all_evaluated