"""
Script principal de execução do sistema de otimização de rotas hospitalares.
Orquestra: dados → algoritmo genético → visualização → saída.
"""
import os
import json
import argparse

from src.data.mock_data import DELIVERY_POINTS, VEHICLES
from src.data.distances import build_distance_matrix
from src.genetic_algorithm.ga_mock import run_genetic_algorithm
from src.visualization.route_map import create_route_map
from src.visualization.comparison_map import create_comparison_map
from src.visualization.charts import (
    plot_fitness_convergence,
    plot_distance_comparison,
    plot_vehicle_load,
    plot_route_distances,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sistema de Otimização de Rotas para Distribuição de Medicamentos"
    )
    parser.add_argument("--pop-size", type=int, default=50, help="Tamanho da população do AG")
    parser.add_argument("--generations", type=int, default=100, help="Número de gerações")
    parser.add_argument("--mutation-rate", type=float, default=0.1, help="Taxa de mutação (0-1)")
    parser.add_argument("--seed", type=int, default=42, help="Seed para reprodutibilidade")
    parser.add_argument("--output-dir", type=str, default="output", help="Diretório de saída")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 60)
    print("  OTIMIZAÇÃO DE ROTAS — DISTRIBUIÇÃO DE MEDICAMENTOS")
    print("=" * 60)

    # 1. Dados
    points = DELIVERY_POINTS
    vehicles = VEHICLES
    print(f"\n📍 Pontos de entrega: {len(points) - 1}")
    print(f"🚐 Veículos disponíveis: {len(vehicles)}")
    for v in vehicles:
        print(f"   - {v.name}: {v.capacity} kg, autonomia {v.max_distance} km")

    # 2. Matriz de distâncias
    dist_matrix = build_distance_matrix(points)
    print(f"\n📐 Matriz de distâncias calculada ({len(points)}x{len(points)})")

    # 3. Execução do Algoritmo Genético
    print(f"\n🧬 Executando Algoritmo Genético...")
    print(f"   População: {args.pop_size} | Gerações: {args.generations} | Mutação: {args.mutation_rate}")

    result = run_genetic_algorithm(
        points=points,
        vehicles=vehicles,
        population_size=args.pop_size,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        seed=args.seed,
    )

    # 4. Resultados no console
    print(f"\n{'=' * 60}")
    print("  RESULTADOS DA OTIMIZAÇÃO")
    print(f"{'=' * 60}")
    print(f"  Distância inicial (sem otimização): {result.initial_distance:.2f} km")
    print(f"  Distância otimizada (AG):           {result.optimized_distance:.2f} km")

    if result.initial_distance > 0:
        improvement = (1 - result.optimized_distance / result.initial_distance) * 100
        print(f"  Melhoria:                           {improvement:.1f}%")

    print(f"\n  Rotas por veículo:")
    for route in result.routes:
        stop_names = [s.name for s in route.stops]
        print(f"  🚐 {route.vehicle.name}:")
        print(f"     Paradas ({len(route.stops)}): {' → '.join(stop_names)}")
        print(f"     Distância: {route.total_distance:.2f} km / {route.vehicle.max_distance} km (autonomia)")
        print(f"     Carga: {route.total_load:.1f} kg / {route.vehicle.capacity} kg (capacidade)")

    # 5. Gerar visualizações
    print(f"\n📊 Gerando visualizações...")
    map_path = os.path.join(args.output_dir, "route_map.html")
    create_route_map(result, points, output_path=map_path)

    comparison_path = os.path.join(args.output_dir, "comparison_map.html")
    create_comparison_map(result, points, output_path=comparison_path)

    plot_fitness_convergence(result, os.path.join(args.output_dir, "convergence.png"))
    plot_distance_comparison(result, os.path.join(args.output_dir, "distance_comparison.png"))
    plot_vehicle_load(result, os.path.join(args.output_dir, "vehicle_load.png"))
    plot_route_distances(result, os.path.join(args.output_dir, "route_distances.png"))

    # 6. Salvar resultado em JSON
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
    print(f"\n💾 Resultado salvo em: {json_path}")

    print(f"\n{'=' * 60}")
    print("  CONCLUÍDO! Verifique a pasta '{}'".format(args.output_dir))
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
