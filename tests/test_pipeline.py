"""
Testes end-to-end do pipeline completo.
"""
import os
import json
import pytest

from src.data.mock_data import DELIVERY_POINTS, VEHICLES
from src.data.distances import haversine, build_distance_matrix, route_total_distance
from src.genetic_algorithm.ga_mock import run_genetic_algorithm
from src.visualization.route_map import create_route_map
from src.visualization.comparison_map import create_comparison_map
from src.visualization.charts import (
    plot_fitness_convergence,
    plot_distance_comparison,
    plot_vehicle_load,
    plot_route_distances,
)


class TestDistances:
    def test_haversine_same_point(self):
        d = haversine(DELIVERY_POINTS[0], DELIVERY_POINTS[0])
        assert d == 0.0

    def test_haversine_positive(self):
        d = haversine(DELIVERY_POINTS[0], DELIVERY_POINTS[1])
        assert d > 0

    def test_distance_matrix_symmetric(self):
        matrix = build_distance_matrix(DELIVERY_POINTS[:5])
        for i in range(5):
            for j in range(5):
                assert abs(matrix[i][j] - matrix[j][i]) < 1e-9

    def test_distance_matrix_diagonal_zero(self):
        matrix = build_distance_matrix(DELIVERY_POINTS[:5])
        for i in range(5):
            assert matrix[i][i] == 0.0

    def test_route_total_distance_empty(self):
        matrix = build_distance_matrix(DELIVERY_POINTS[:5])
        assert route_total_distance([], matrix) == 0.0


class TestGeneticAlgorithm:
    def test_returns_result(self):
        result = run_genetic_algorithm(
            DELIVERY_POINTS, VEHICLES,
            population_size=10, generations=10, seed=42,
        )
        assert result is not None
        assert len(result.routes) == len(VEHICLES)

    def test_all_points_assigned(self):
        result = run_genetic_algorithm(
            DELIVERY_POINTS, VEHICLES,
            population_size=10, generations=10, seed=42,
        )
        all_stops = []
        for route in result.routes:
            all_stops.extend([s.id for s in route.stops])
        expected_ids = {p.id for p in DELIVERY_POINTS if p.id > 0}
        assert set(all_stops) == expected_ids

    def test_optimization_improves(self):
        result = run_genetic_algorithm(
            DELIVERY_POINTS, VEHICLES,
            population_size=30, generations=50, seed=42,
        )
        assert result.optimized_distance <= result.initial_distance

    def test_fitness_history_length(self):
        gens = 20
        result = run_genetic_algorithm(
            DELIVERY_POINTS, VEHICLES,
            population_size=10, generations=gens, seed=42,
        )
        assert len(result.fitness_history) == gens


class TestEndToEnd:
    def test_full_pipeline(self, tmp_path):
        """Testa o pipeline completo: dados → AG → JSON de saída."""
        result = run_genetic_algorithm(
            DELIVERY_POINTS, VEHICLES,
            population_size=10, generations=10, seed=42,
        )
        # Verifica se conseguimos gerar o JSON de resultado
        result_json = {
            "initial_distance_km": round(result.initial_distance, 2),
            "optimized_distance_km": round(result.optimized_distance, 2),
            "vehicles": [
                {
                    "name": r.vehicle.name,
                    "stops": [s.name for s in r.stops],
                    "distance_km": round(r.total_distance, 2),
                }
                for r in result.routes
            ],
        }
        json_path = os.path.join(str(tmp_path), "result.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result_json, f, ensure_ascii=False, indent=2)

        # Verifica se o JSON foi salvo corretamente
        with open(json_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded["initial_distance_km"] > 0
        assert len(loaded["vehicles"]) == len(VEHICLES)


@pytest.fixture(scope="module")
def ga_result():
    """Resultado compartilhado entre testes de visualização."""
    return run_genetic_algorithm(
        DELIVERY_POINTS, VEHICLES,
        population_size=10, generations=10, seed=42,
    )


class TestVisualization:
    def test_route_map_generated(self, ga_result, tmp_path):
        path = os.path.join(str(tmp_path), "route_map.html")
        create_route_map(ga_result, DELIVERY_POINTS, output_path=path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 1000  # HTML deve ter conteúdo relevante

    def test_comparison_map_generated(self, ga_result, tmp_path):
        path = os.path.join(str(tmp_path), "comparison_map.html")
        create_comparison_map(ga_result, DELIVERY_POINTS, output_path=path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 1000

    def test_comparison_map_contains_dual_pane(self, ga_result, tmp_path):
        path = os.path.join(str(tmp_path), "comparison.html")
        create_comparison_map(ga_result, DELIVERY_POINTS, output_path=path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "SEM OTIMIZAÇÃO" in content or "SEM OTIMIZA" in content
        assert "OTIMIZADO" in content

    def test_convergence_chart(self, ga_result, tmp_path):
        path = os.path.join(str(tmp_path), "convergence.png")
        plot_fitness_convergence(ga_result, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 500

    def test_distance_comparison_chart(self, ga_result, tmp_path):
        path = os.path.join(str(tmp_path), "distance_comparison.png")
        plot_distance_comparison(ga_result, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 500

    def test_vehicle_load_chart(self, ga_result, tmp_path):
        path = os.path.join(str(tmp_path), "vehicle_load.png")
        plot_vehicle_load(ga_result, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 500

    def test_route_distances_chart(self, ga_result, tmp_path):
        path = os.path.join(str(tmp_path), "route_distances.png")
        plot_route_distances(ga_result, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 500
