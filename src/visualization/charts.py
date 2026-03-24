import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.data.models import OptimizationResult


def plot_fitness_convergence(result: OptimizationResult, output_path: str = "output/convergence.png"):
    fig, ax = plt.subplots(figsize=(10, 5))

    generations = list(range(1, len(result.fitness_history) + 1))
    ax.plot(generations, result.fitness_history, color="#2980b9", linewidth=2)
    ax.set_xlabel("Geração", fontsize=12)
    ax.set_ylabel("Fitness (Distância Total - km)", fontsize=12)
    ax.set_title("Convergência do Algoritmo Genético", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)

    # Marcar melhor fitness
    best_gen = result.fitness_history.index(min(result.fitness_history)) + 1
    best_val = min(result.fitness_history)
    ax.annotate(
        f"Melhor: {best_val:.2f} km\n(Geração {best_gen})",
        xy=(best_gen, best_val),
        xytext=(best_gen + len(generations) * 0.1, best_val + (max(result.fitness_history) - best_val) * 0.2),
        arrowprops=dict(arrowstyle="->", color="#e74c3c"),
        fontsize=10, color="#e74c3c",
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Gráfico de convergência salvo em: {output_path}")


def plot_distance_comparison(result: OptimizationResult, output_path: str = "output/distance_comparison.png"):
    fig, ax = plt.subplots(figsize=(8, 5))

    labels = ["Rota Inicial\n(sem otimização)", "Rota Otimizada\n(AG)"]
    values = [result.initial_distance, result.optimized_distance]
    colors = ["#e74c3c", "#27ae60"]

    bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor="white", linewidth=2)

    # Valores em cima das barras
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
            f"{val:.2f} km", ha="center", va="bottom", fontsize=13, fontweight="bold",
        )

    # Percentual de melhoria
    if result.initial_distance > 0:
        improvement = (1 - result.optimized_distance / result.initial_distance) * 100
        ax.set_title(
            f"Comparativo de Distância Total — Melhoria de {improvement:.1f}%",
            fontsize=13, fontweight="bold",
        )
    else:
        ax.set_title("Comparativo de Distância Total", fontsize=13, fontweight="bold")

    ax.set_ylabel("Distância Total (km)", fontsize=12)
    ax.set_ylim(0, max(values) * 1.25)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Gráfico comparativo salvo em: {output_path}")


def plot_vehicle_load(result: OptimizationResult, output_path: str = "output/vehicle_load.png"):
    fig, ax = plt.subplots(figsize=(10, 5))

    names = [r.vehicle.name for r in result.routes]
    loads = [r.total_load for r in result.routes]
    capacities = [r.vehicle.capacity for r in result.routes]
    x = range(len(names))

    # Barras de capacidade (fundo) e carga (frente)
    ax.bar(x, capacities, width=0.5, color="#ecf0f1", edgecolor="#bdc3c7", label="Capacidade Máxima")
    bars = ax.bar(x, loads, width=0.5, color="#3498db", edgecolor="white", label="Carga Atribuída")

    for i, (load, cap) in enumerate(zip(loads, capacities)):
        pct = (load / cap * 100) if cap > 0 else 0
        ax.text(i, load + 0.5, f"{load:.1f} kg\n({pct:.0f}%)", ha="center", fontsize=10)

    ax.set_xticks(list(x))
    ax.set_xticklabels(names, fontsize=10)
    ax.set_ylabel("Peso (kg)", fontsize=12)
    ax.set_title("Utilização de Carga por Veículo", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Gráfico de carga salvo em: {output_path}")


def plot_route_distances(result: OptimizationResult, output_path: str = "output/route_distances.png"):
    fig, ax = plt.subplots(figsize=(10, 5))

    names = [r.vehicle.name for r in result.routes]
    distances = [r.total_distance for r in result.routes]
    max_dists = [r.vehicle.max_distance for r in result.routes]
    x = range(len(names))

    ax.bar(x, max_dists, width=0.5, color="#ecf0f1", edgecolor="#bdc3c7", label="Autonomia Máx.")
    colors = ["#27ae60" if d <= m else "#e74c3c" for d, m in zip(distances, max_dists)]
    ax.bar(x, distances, width=0.5, color=colors, edgecolor="white", label="Distância Percorrida")

    for i, (d, m) in enumerate(zip(distances, max_dists)):
        pct = (d / m * 100) if m > 0 else 0
        ax.text(i, d + 0.5, f"{d:.1f} km\n({pct:.0f}%)", ha="center", fontsize=10)

    ax.set_xticks(list(x))
    ax.set_xticklabels(names, fontsize=10)
    ax.set_ylabel("Distância (km)", fontsize=12)
    ax.set_title("Distância Percorrida vs Autonomia por Veículo", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Gráfico de distância por veículo salvo em: {output_path}")
