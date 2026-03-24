"""
Análise comparativa dos resultados dos experimentos do AG.

Lê os JSONs gerados por src/experiments/main.py e produz:
  - Tabela comparativa no terminal
  - Gráfico de convergência multi-experimento (output/experiments/convergence_comparison.png)
  - Ranking dos experimentos por melhoria
"""
import os
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


COLORS = ["#2980b9", "#27ae60", "#e67e22"]


def load_results(experiments_dir: str = "output/experiments") -> list[dict]:
    all_path = os.path.join(experiments_dir, "all_experiments.json")
    if not os.path.exists(all_path):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {all_path}\n"
            "Execute src/experiments/main.py primeiro."
        )
    with open(all_path, "r", encoding="utf-8") as f:
        return json.load(f)


def print_comparison_table(results: list[dict]):
    print("\n" + "=" * 80)
    print(" COMPARATIVO DE EXPERIMENTOS — Algoritmo Genético VRP Hospitalar")
    print("=" * 80)
    header = (
        f"{'#':<4} {'Configuração':<40} "
        f"{'Dist. Ini.':<12} {'Dist. Opt.':<12} "
        f"{'Melhoria':<10} {'Conv. Gen.':<12} {'Tempo':<8}"
    )
    print(header)
    print("-" * 80)

    ranked = sorted(results, key=lambda r: -r["metrics"]["improvement_pct"])
    for i, r in enumerate(ranked):
        m = r["metrics"]
        name = r["name"][:40]
        print(
            f"{i+1:<4} {name:<40} "
            f"{m['initial_distance_km']:<12.2f} {m['optimized_distance_km']:<12.2f} "
            f"{m['improvement_pct']:<10.1f} {m['convergence_generation']:<12} "
            f"{m['elapsed_seconds']:<8.1f}s"
        )

    print("=" * 80)
    best = ranked[0]
    print(f"\nMelhor experimento: #{best['id']} — {best['name']}")
    print(f"  Melhoria: {best['metrics']['improvement_pct']:.1f}%")
    print(f"  Distância final: {best['metrics']['optimized_distance_km']:.2f} km")


def plot_convergence_comparison(results: list[dict], output_dir: str = "output/experiments"):
    fig, ax = plt.subplots(figsize=(11, 5))

    for i, r in enumerate(results):
        history = r["fitness_history"]
        gens = list(range(1, len(history) + 1))
        color = COLORS[i % len(COLORS)]
        label = f"Exp {r['id']}: {r['config']['population_size']} ind, "\
                f"mut={r['config']['mutation_rate']}, {r['config']['selection_type']}"
        ax.plot(gens, history, color=color, linewidth=2, label=label)

        # Marca ponto de convergência
        best_val = min(history)
        conv_idx = history.index(best_val)
        ax.scatter([conv_idx + 1], [best_val], color=color, s=80, zorder=5,
                   edgecolors="white", linewidths=1.5)

    ax.set_xlabel("Geração", fontsize=12)
    ax.set_ylabel("Fitness (Distância + Penalidades)", fontsize=12)
    ax.set_title("Convergência Comparativa — 3 Experimentos AG", fontsize=14, fontweight="bold")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = os.path.join(output_dir, "convergence_comparison.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\nGráfico comparativo salvo em: {path}")


def plot_improvement_bar(results: list[dict], output_dir: str = "output/experiments"):
    fig, ax = plt.subplots(figsize=(9, 5))

    names = [f"Exp {r['id']}\n{r['config']['population_size']} ind / "
             f"mut {r['config']['mutation_rate']} / {r['config']['selection_type']}"
             for r in results]
    improvements = [r["metrics"]["improvement_pct"] for r in results]
    colors = [COLORS[i % len(COLORS)] for i in range(len(results))]

    bars = ax.bar(names, improvements, color=colors, width=0.5, edgecolor="white", linewidth=1.5)
    for bar, val in zip(bars, improvements):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=12, fontweight="bold")

    ax.set_ylabel("Melhoria sobre rota inicial (%)", fontsize=12)
    ax.set_title("Melhoria por Configuração do AG", fontsize=13, fontweight="bold")
    ax.set_ylim(0, max(improvements) * 1.3 + 5)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    path = os.path.join(output_dir, "improvement_comparison.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Gráfico de melhoria salvo em: {path}")


def analyze(experiments_dir: str = "output/experiments"):
    results = load_results(experiments_dir)
    print_comparison_table(results)
    plot_convergence_comparison(results, experiments_dir)
    plot_improvement_bar(results, experiments_dir)


if __name__ == "__main__":
    analyze()

