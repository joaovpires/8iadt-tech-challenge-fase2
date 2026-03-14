# =============================================================================
# experiments/main.py — Experimentos e Análise de Parâmetros do GA
#
# Executa o GA múltiplas vezes com diferentes parâmetros para:
#   1. Encontrar a melhor configuração
#   2. Avaliar estabilidade (variância dos resultados)
#   3. Medir tempo de execução
#   4. Gerar gráficos comparativos
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
import json
import csv
from itertools import product
from datetime import datetime
import numpy as np

from ga.algorithm import run_ga_visual
from ga.fitness import calculate_distance, calculate_distance_att
from ga.cities import generate_cities, load_att48


# =============================================================================
# CONFIGURAÇÃO DOS EXPERIMENTOS
# =============================================================================
EXPERIMENT_RUNS = 3  # quantas vezes rodar cada combinação de parâmetros
NUM_CITIES = 20      # número de cidades para experimento

# Espaço de parâmetros a testar
PARAM_GRID = {
    "population_size": [100, 200, 500],
    "mutation_probability": [0.1, 0.2, 0.5],
    "tournament_k": [2, 3, 5],
    "max_generations": [100, 200],
    "selection_type": ["tournament", "top10", "roulette"],
}

# Limite de tempo por experimento (segundos)
TIME_LIMIT = 600  # 10 minutos


# =============================================================================
# EXECUTAR UM ÚNICO EXPERIMENTO
# =============================================================================
def run_single_experiment(
    cities,
    population_size,
    mutation_probability,
    tournament_k,
    max_generations,
    selection_type,
    distance_function,
    run_number
):
    """
    Executa uma única rodada do GA com os parâmetros especificados.
    
    Retorna:
        dict com métricas: best_distance, avg_distance, worst_distance,
        convergence_rate, execution_time, run_number
    """
    start_time = time.time()
    
    try:
        history, best_routes, populations = run_ga_visual(
            cities,
            population_size=population_size,
            mutation_probability=mutation_probability,
            tournament_k=tournament_k,
            max_generations=max_generations,
            selection_type=selection_type,
            distance_function=distance_function
        )
        
        execution_time = time.time() - start_time
        
        return {
            "best_distance": history[-1],  # distância final (melhor route)
            "worst_distance": max(history),
            "avg_distance": np.mean(history),
            "std_distance": np.std(history),
            "convergence_rate": (history[0] - history[-1]) / history[0],  # % de melhoria
            "execution_time": execution_time,
            "run_number": run_number,
            "success": True,
        }
    
    except Exception as e:
        execution_time = time.time() - start_time
        return {
            "best_distance": None,
            "error": str(e),
            "execution_time": execution_time,
            "run_number": run_number,
            "success": False,
        }


# =============================================================================
# EXECUTAR TODOS OS EXPERIMENTOS
# =============================================================================
def run_all_experiments():
    """
    Itera sobre todas as combinações de parâmetros e executa EXPERIMENT_RUNS
    vezes para cada combinação, compilando estatísticas.
    """
    
    # Gera um conjunto de cidades aleatórias (mesmas para todos os experimentos)
    cities = generate_cities(NUM_CITIES)
    distance_function = calculate_distance
    
    # Lista para armazenar todos os resultados
    all_results = []
    
    # Gera todas as combinações de parâmetros
    param_names = list(PARAM_GRID.keys())
    param_values = list(PARAM_GRID.values())
    param_combinations = list(product(*param_values))
    
    total_combinations = len(param_combinations)
    print(f"\n📊 Total de combinações a testar: {total_combinations}")
    print(f"   Rodadas por combinação: {EXPERIMENT_RUNS}")
    print(f"   Total de execuções: {total_combinations * EXPERIMENT_RUNS}\n")
    
    for combo_idx, params in enumerate(param_combinations, 1):
        # Desempacota os parâmetros
        param_dict = dict(zip(param_names, params))
        
        print(f"[{combo_idx}/{total_combinations}] Testando: {param_dict}")
        
        # Roda EXPERIMENT_RUNS vezes esta combinação
        combo_results = []
        for run in range(1, EXPERIMENT_RUNS + 1):
            result = run_single_experiment(
                cities,
                distance_function=distance_function,
                run_number=run,
                **param_dict
            )
            combo_results.append(result)
            
            if result["success"]:
                print(f"  ✓ Run {run}: {result['best_distance']:.2f} em {result['execution_time']:.2f}s")
            else:
                print(f"  ✗ Run {run}: Erro - {result['error']}")
        
        # Calcula estatísticas agregadas para esta combinação
        successful_runs = [r for r in combo_results if r["success"]]
        
        if successful_runs:
            distances = [r["best_distance"] for r in successful_runs]
            times = [r["execution_time"] for r in successful_runs]
            
            aggregated = {
                **param_dict,
                "avg_best_distance": np.mean(distances),
                "std_best_distance": np.std(distances),
                "min_best_distance": min(distances),
                "max_best_distance": max(distances),
                "avg_execution_time": np.mean(times),
                "successful_runs": len(successful_runs),
                "total_runs": EXPERIMENT_RUNS,
            }
            
            all_results.append(aggregated)
            print(f"  📈 Agregado: {aggregated['avg_best_distance']:.2f} ± {aggregated['std_best_distance']:.2f}")
        
        print()
    
    return all_results


# =============================================================================
# SALVAR RESULTADOS
# =============================================================================
def save_results(results):
    """
    Salva os resultados em arquivo CSV e JSON com timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Cria diretório de resultados se não existir
    results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Salva em CSV
    csv_path = os.path.join(results_dir, f"experiments_{timestamp}.csv")
    if results:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"✅ Resultados salvos em: {csv_path}")
    
    # Salva em JSON (para preservar estrutura)
    json_path = os.path.join(results_dir, f"experiments_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Resultados também salvos em: {json_path}")
    
    return csv_path, json_path


# =============================================================================
# ANALISAR RESULTADOS
# =============================================================================
def analyze_results(results):
    """
    Imprime análise dos resultados.
    """
    if not results:
        print("❌ Nenhum resultado disponível para análise.")
        return
    
    print("\n" + "="*80)
    print("📊 ANÁLISE DOS RESULTADOS")
    print("="*80 + "\n")
    
    # Melhor resultado geral
    best_result = min(results, key=lambda x: x["avg_best_distance"])
    print(f"🏆 MELHOR CONFIGURAÇÃO:")
    print(f"   Distância média: {best_result['avg_best_distance']:.2f}")
    print(f"   Desvio padrão:   {best_result['std_best_distance']:.2f}")
    print(f"   Tempo médio:     {best_result['avg_execution_time']:.2f}s")
    print(f"   Parâmetros:")
    for param in PARAM_GRID.keys():
        if param in best_result:
            print(f"      - {param}: {best_result[param]}")
    
    # Mais rápido
    fastest = min(results, key=lambda x: x["avg_execution_time"])
    print(f"\n⚡ MAIS RÁPIDO:")
    print(f"   Tempo médio: {fastest['avg_execution_time']:.2f}s")
    print(f"   Distância:   {fastest['avg_best_distance']:.2f}")
    
    # Mais estável
    most_stable = min(results, key=lambda x: x["std_best_distance"])
    print(f"\n📈 MAIS ESTÁVEL (menor desvio padrão):")
    print(f"   Desvio padrão: {most_stable['std_best_distance']:.2f}")
    print(f"   Distância:     {most_stable['avg_best_distance']:.2f}")
    
    print("\n" + "="*80)


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    print("\n🚀 Iniciando experimentos do Algoritmo Genético...")
    print(f"   Cidades: {NUM_CITIES}")
    print(f"   Rodadas por combinação: {EXPERIMENT_RUNS}")
    
    # Executa experimentos
    results = run_all_experiments()
    
    # Salva resultados
    csv_path, json_path = save_results(results)
    
    # Analisa resultados
    analyze_results(results)
    
    print("\n✅ Experimentos concluídos!")

