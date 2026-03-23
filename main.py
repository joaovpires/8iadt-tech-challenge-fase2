import os
import json
import argparse

from src.data.mock_data import DELIVERY_POINTS, VEHICLES
from src.data.distances import build_distance_matrix
from src.genetic_algorithm.ga_adapter import run_genetic_algorithm
from src.visualization.route_map import create_route_map
from src.visualization.comparison_map import create_comparison_map
from src.visualization.charts import (
    plot_fitness_convergence,
    plot_distance_comparison,
    plot_vehicle_load,
    plot_route_distances,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Otimização de rotas para distribuição de medicamentos")
    parser.add_argument("--pop-size", type=int, default=50)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--mutation-rate", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=str, default="output")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    points = DELIVERY_POINTS
    vehicles = VEHICLES

    print(f"Pontos de entrega: {len(points) - 1}")
    print(f"Veiculos: {len(vehicles)}")
    for v in vehicles:
        print(f"  {v.name}: {v.capacity} kg, {v.max_distance} km")

    build_distance_matrix(points)

    print(f"\nRodando AG — pop={args.pop_size}, geracoes={args.generations}, mutacao={args.mutation_rate}")

    result = run_genetic_algorithm(
        points=points,
        vehicles=vehicles,
        population_size=args.pop_size,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        seed=args.seed,
    )

    print(f"\nDistancia inicial: {result.initial_distance:.2f} km")
    print(f"Distancia otimizada: {result.optimized_distance:.2f} km")

    if result.initial_distance > 0:
        improvement = (1 - result.optimized_distance / result.initial_distance) * 100
        print(f"Melhoria: {improvement:.1f}%")

    for route in result.routes:
        stop_names = [s.name for s in route.stops]
        print(f"\n{route.vehicle.name}:")
        print(f"  {' -> '.join(stop_names)}")
        print(f"  {route.total_distance:.2f} km | {route.total_load:.1f}/{route.vehicle.capacity} kg")

    print("\nGerando visualizacoes...")
    create_route_map(result, points, output_path=os.path.join(args.output_dir, "route_map.html"))
    create_comparison_map(result, points, output_path=os.path.join(args.output_dir, "comparison_map.html"))
    plot_fitness_convergence(result, os.path.join(args.output_dir, "convergence.png"))
    plot_distance_comparison(result, os.path.join(args.output_dir, "distance_comparison.png"))
    plot_vehicle_load(result, os.path.join(args.output_dir, "vehicle_load.png"))
    plot_route_distances(result, os.path.join(args.output_dir, "route_distances.png"))

    result_json = {
        "initial_distance_km": round(result.initial_distance, 2),
        "optimized_distance_km": round(result.optimized_distance, 2),
        "improvement_pct": round((1 - result.optimized_distance / result.initial_distance) * 100, 1) if result.initial_distance > 0 else 0,
        "generations": result.generations,
        "vehicles": [
            {
                "name": r.vehicle.name,
                "stops": [s.name for s in r.stops],
                "distance_km": round(r.total_distance, 2),
                "load_kg": round(r.total_load, 1),
                "capacity_kg": r.vehicle.capacity,
                "max_distance_km": r.vehicle.max_distance,
            }
            for r in result.routes
        ],
    }
    json_path = os.path.join(args.output_dir, "result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)
    print(f"Resultado salvo em: {json_path}")


if __name__ == "__main__":
    main()
