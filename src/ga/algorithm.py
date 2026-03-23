# =============================================================================
# algorithm.py — Motor principal do Algoritmo Genético
#
# Orquestra todo o ciclo evolutivo: avaliação → seleção → cruzamento → mutação
# Retorna os dados de cada geração para a visualização no app.py
# =============================================================================

from population import generate_population
from fitness import calculate_fitness
from crossover import order_crossover
from mutation import mutate
from selection import tournament_selection, top_10_selection, roulette_selection


def run_ga_visual(
    cities,
    population_size=200,
    mutation_probability=0.2,
    tournament_k=3,
    max_generations=200,
    selection_type="tournament",
    distance_function=None
):
    """
    Executa o Algoritmo Genético para o TSP (Problema do Caixeiro Viajante)
    e retorna os dados de cada geração para animação na interface.

    O algoritmo segue o ciclo evolutivo clássico:
        1. Gera população inicial híbrida
        2. Avalia o fitness (distância total) de cada rota
        3. Ordena do melhor para o pior
        4. Seleciona pais → cruza → muta → forma nova geração
        5. Repete por max_generations gerações

    Parâmetros:
        cities               — lista de tuplas (x, y) com as coordenadas dos pontos
        population_size      — quantas rotas candidatas existem por geração
        mutation_probability — chance de inverter um segmento da rota (0.0 a 1.0)
        tournament_k         — tamanho do grupo no torneio (usado se selection_type="tournament")
        max_generations      — número total de gerações a executar
        selection_type       — método de seleção dos pais: "tournament", "top10" ou "roulette"
        distance_function    — função que calcula a distância entre dois pontos (obrigatória)

    Retorna:
        history      — lista com a melhor distância de cada geração (para o gráfico de convergência)
        best_routes  — lista com a melhor rota de cada geração (para o mapa animado)
        populations  — lista com toda a população de cada geração (para o histograma)
    """
    if distance_function is None:
        raise ValueError("distance_function deve ser fornecida ao GA.")

    # Gera a população inicial com estratégia híbrida:
    # 40% nearest neighbour + 20% convex hull + 40% aleatório
    population = generate_population(len(cities), population_size, cities)

    # Listas que acumulam os dados de cada geração para visualização
    history     = []   # melhor distância por geração
    best_routes = []   # melhor rota por geração
    populations = []   # população completa por geração

    for generation in range(max_generations):

        # ------------------------------------------------------------------
        # AVALIAÇÃO — calcula a distância total de cada rota na população
        # Quanto menor a distância, melhor o indivíduo (fitness inverso)
        # ------------------------------------------------------------------
        fitness = [calculate_fitness(ind, cities, distance_function) for ind in population]

        # ------------------------------------------------------------------
        # ORDENAÇÃO — do melhor (menor distância) para o pior
        # population[0] sempre será o melhor indivíduo da geração
        # ------------------------------------------------------------------
        sorted_pop = sorted(zip(population, fitness), key=lambda x: x[1])

        # Proteção contra população vazia (não deve ocorrer em uso normal)
        if not sorted_pop:
            break

        population, fitness = zip(*sorted_pop)
        population = list(population)
        fitness    = list(fitness)

        # Registra os dados desta geração para a visualização
        history.append(fitness[0])             # menor distância da geração
        best_routes.append(population[0])      # rota com menor distância
        populations.append(population.copy())  # cópia de toda a população

        # ------------------------------------------------------------------
        # NOVA GERAÇÃO — constrói a próxima geração por seleção + cruzamento + mutação
        # ------------------------------------------------------------------
        new_population = []

        # Elitismo: o melhor indivíduo passa direto para a próxima geração
        # sem sofrer cruzamento ou mutação — garante que a solução nunca piora
        new_population.append(population[0])

        # Preenche o resto da população com filhos gerados por cruzamento
        while len(new_population) < population_size:

            # SELEÇÃO — escolhe dois pais conforme o método configurado
            if selection_type == "tournament":
                # Torneio: sorteia k indivíduos e escolhe o melhor entre eles
                p1 = tournament_selection(population, fitness, tournament_k)
                p2 = tournament_selection(population, fitness, tournament_k)

            elif selection_type == "top10":
                # Top 10: escolhe aleatoriamente entre os 10 melhores
                p1 = top_10_selection(population, fitness)
                p2 = top_10_selection(population, fitness)

            elif selection_type == "roulette":
                # Roleta: probabilidade de ser escolhido proporcional à qualidade
                p1 = roulette_selection(population, fitness)
                p2 = roulette_selection(population, fitness)

            # CRUZAMENTO — combina os dois pais para gerar um filho
            # Usa o operador OX (Order Crossover) que preserva a ordem relativa
            child = order_crossover(p1, p2)

            # MUTAÇÃO — com probabilidade mutation_probability, inverte um segmento
            # Introduz variação para escapar de mínimos locais
            child = mutate(child, mutation_probability)

            new_population.append(child)

        population = new_population

    return history, best_routes, populations
