from src.ga.algorithm_vrp import run_ga_vrp
from src.ga.vrp_models import Delivery, Vehicle


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

    history, best_solutions = run_ga_vrp(
        deliveries=deliveries,
        vehicles=vehicles,
        population_size=30,
        mutation_probability=0.2,
        tournament_k=3,
        max_generations=50,
        selection_type="tournament",
    )

    best = best_solutions[-1]

    print("Melhor sequência:", best["sequence"])
    print("Melhor cromossomo VRP:", best["chromosome"])
    print("Rotas:", best["routes"])
    print("Distância total:", round(best["total_distance"], 2))
    print("Penalidade total:", round(best["penalty"], 2))
    print("Fitness:", round(best["fitness"], 2))
    print("Clientes faltantes:", best["missing_clients"])
    print("Clientes duplicados:", best["duplicate_clients"])
    print("Histórico:", [round(x, 2) for x in history])


if __name__ == "__main__":
    main()