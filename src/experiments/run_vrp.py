from src.ga.vrp_models import Delivery, Vehicle
from src.ga.vrp_population import generate_vrp_population
from src.ga.vrp_fitness import evaluate_vrp_solution


def main():
    deliveries = [
        Delivery(0, 50, 50, 0, 0),
        Delivery(1, 10, 20, 10, 1),
        Delivery(2, 20, 80, 15, 2),
        Delivery(3, 80, 90, 12, 1),
        Delivery(4, 60, 20, 8, 3),
        Delivery(5, 30, 40, 7, 2),
        Delivery(6, 70, 60, 20, 1),
    ]

    vehicles = [
        Vehicle(1, 30, 180),
        Vehicle(2, 35, 200),
    ]

    population = generate_vrp_population(
        num_clients=len(deliveries) - 1,
        num_vehicles=len(vehicles),
        population_size=5,
    )

    for chromosome in population:
        result = evaluate_vrp_solution(chromosome, deliveries, vehicles)
        print("Cromossomo:", chromosome)
        print("Rotas:", result["routes"])
        print("Distância total:", round(result["total_distance"], 2))
        print("Penalidade total:", round(result["penalty"], 2))
        print("Fitness:", round(result["fitness"], 2))
        print("Clientes faltantes:", result["missing_clients"])
        print("Clientes duplicados:", result["duplicate_clients"])
        print("-" * 60)


if __name__ == "__main__":
    main()