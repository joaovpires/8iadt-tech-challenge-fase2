"""
Experimentos comparativos do Algoritmo Genético para o VRP hospitalar.

Roda 3 experimentos com configurações distintas e salva os resultados
em output/experiments/ para análise posterior.

Experimento 1 — Linha de base (baseline)
    pop=30, gerações=50, mutação=0.1, seleção=tournament

Experimento 2 — Alta pressão seletiva
    pop=80, gerações=100, mutação=0.05, seleção=tournament

Experimento 3 — Maior diversidade genética
    pop=50, gerações=100, mutação=0.3, seleção=roulette
"""
import os
import json
import time

from src.data.mock_data import DELIVERY_POINTS, VEHICLES
from src.data.distances import build_distance_matrix
from src.genetic_algorithm.ga_adapter import run_genetic_algorithm


EXPERIMENTS = [
    {
        "id": 1,
        "name": "Baseline (pop=30, mut=0.10, tournament)",
        "description": "Configuração de referência com parâmetros conservadores.",
        "population_size": 30,
        "generations": 50,
        "mutation_rate": 0.10,
        "selection_type": "tournament",
    },
    {
        "id": 2,
        "name": "Alta pressão seletiva (pop=80, mut=0.05, tournament)",
        "description": "Maior população e baixa mutação favorecem exploração local aprofundada.",
        "population_size": 80,
        "generations": 100,
        "mutation_rate": 0.05,
        "selection_type": "tournament",
    },
    {
        "id": 3,
        "name": "Alta diversidade (pop=50, mut=0.30, roulette)",
        "description": "Mutação alta e seleção por roleta ampliam diversidade genética.",
        "population_size": 50,
        "generations": 100,
        "mutation_rate": 0.30,
        "selection_type": "roulette",
    },
]


def run_experiments(output_dir: str = "output/experiments") -> list[dict]:
    os.makedirs(output_dir, exist_ok=True)
    build_distance_matrix(DELIVERY_POINTS)

    results = []

    for exp in EXPERIMENTS:
        print(f"\n{'='*60}")
        print(f"Experimento {exp['id']}: {exp['name']}")
        print(f"  pop={exp['population_size']}, gerações={exp['generations']}, "
              f"mutação={exp['mutation_rate']}, seleção={exp['selection_type']}")
        print(f"{'='*60}")

        start = time.time()
        result = run_genetic_algorithm(
            points=DELIVERY_POINTS,
            vehicles=VEHICLES,
            population_size=exp["population_size"],
            generations=exp["generations"],
            mutation_rate=exp["mutation_rate"],
            seed=42,
        )
        elapsed = time.time() - start

        improvement = 0.0
        if result.initial_distance > 0:
            improvement = (1 - result.optimized_distance / result.initial_distance) * 100

        # Geração em que convergiu (último grande salto de melhoria)
        history = result.fitness_history
        best_val = min(history)
        conv_gen = next((i + 1 for i, v in enumerate(history) if v == best_val), len(history))

        exp_result = {
            "id": exp["id"],
            "name": exp["name"],
            "description": exp["description"],
            "config": {
                "population_size": exp["population_size"],
                "generations": exp["generations"],
                "mutation_rate": exp["mutation_rate"],
                "selection_type": exp["selection_type"],
            },
            "metrics": {
                "initial_distance_km": round(result.initial_distance, 2),
                "optimized_distance_km": round(result.optimized_distance, 2),
                "improvement_pct": round(improvement, 1),
                "convergence_generation": conv_gen,
                "best_fitness": round(best_val, 2),
                "elapsed_seconds": round(elapsed, 2),
            },
            "fitness_history": [round(v, 4) for v in history],
            "routes": [
                {
                    "vehicle": r.vehicle.name,
                    "stops": [s.name for s in r.stops],
                    "distance_km": round(r.total_distance, 2),
                    "load_kg": round(r.total_load, 1),
                    "capacity_kg": r.vehicle.capacity,
                }
                for r in result.routes
            ],
        }

        results.append(exp_result)

        print(f"  Distância inicial:   {result.initial_distance:.2f} km")
        print(f"  Distância otimizada: {result.optimized_distance:.2f} km")
        print(f"  Melhoria:            {improvement:.1f}%")
        print(f"  Convergiu na geração {conv_gen}/{exp['generations']}")
        print(f"  Tempo:               {elapsed:.1f}s")

        # Salva resultado individual
        exp_path = os.path.join(output_dir, f"experiment_{exp['id']}.json")
        with open(exp_path, "w", encoding="utf-8") as f:
            json.dump(exp_result, f, ensure_ascii=False, indent=2)
        print(f"  Salvo em: {exp_path}")

    # Salva todos juntos
    all_path = os.path.join(output_dir, "all_experiments.json")
    with open(all_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nTodos os experimentos salvos em: {all_path}")

    return results


if __name__ == "__main__":
    run_experiments()

