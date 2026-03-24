"""
Interface web do Tech Challenge Fase 2 — Otimização de Rotas Hospitalares com AG.

Para rodar:
    streamlit run app.py
"""
import os
import tempfile

import streamlit as st
import streamlit.components.v1 as components

from src.data.mock_data import DELIVERY_POINTS, VEHICLES
from src.data.models import DeliveryPoint, Vehicle
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
from src.experiments.main import EXPERIMENTS, run_experiments
from src.results.main import plot_convergence_comparison, plot_improvement_bar
from src.llm.main import generate_driver_instructions, generate_route_report, ask_question

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="VRP Hospitalar — AG",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar — Parâmetros do AG
# ---------------------------------------------------------------------------

st.sidebar.title("Parâmetros do AG")
st.sidebar.markdown("---")

pop_size = st.sidebar.slider("Tamanho da população", min_value=10, max_value=200, value=80, step=10)
generations = st.sidebar.slider("Gerações", min_value=10, max_value=500, value=100, step=10)
mutation_rate = st.sidebar.slider("Taxa de mutação", min_value=0.01, max_value=0.50, value=0.05, step=0.01, format="%.2f")
seed = st.sidebar.number_input("Seed (reprodutibilidade)", min_value=0, max_value=9999, value=42)

st.sidebar.markdown("---")

with st.sidebar.expander(f"Pontos de Entrega ({len(DELIVERY_POINTS)-1})", expanded=False):
    edited_delivery = []
    for dp in DELIVERY_POINTS[1:]:
        st.markdown(f"**{dp.name}**")
        c1, c2 = st.columns(2)
        demand = c1.number_input(
            "Demanda (kg)", value=float(dp.demand), min_value=0.0, step=1.0, key=f"dp_d_{dp.id}"
        )
        priority = c2.selectbox(
            "Prioridade", ["critica", "alta", "media", "baixa"],
            index=["critica", "alta", "media", "baixa"].index(dp.priority),
            key=f"dp_p_{dp.id}",
        )
        edited_delivery.append(
            DeliveryPoint(dp.id, dp.name, dp.latitude, dp.longitude, priority, demand)
        )

points = [DELIVERY_POINTS[0]] + edited_delivery

with st.sidebar.expander(f"Veiculos ({len(VEHICLES)})", expanded=False):
    edited_vehicles = []
    for v in VEHICLES:
        st.markdown(f"**{v.name}**")
        c1, c2 = st.columns(2)
        capacity = c1.number_input(
            "Capacidade (kg)", value=float(v.capacity), min_value=1.0, step=5.0, key=f"v_c_{v.id}"
        )
        max_dist = c2.number_input(
            "Autonomia (km)", value=float(v.max_distance), min_value=10.0, step=10.0, key=f"v_d_{v.id}"
        )
        edited_vehicles.append(Vehicle(v.id, v.name, capacity, max_dist))

vehicles = edited_vehicles

run_btn = st.sidebar.button("Rodar Otimizacao", type="primary", width="stretch")

# ---------------------------------------------------------------------------
# Título principal
# ---------------------------------------------------------------------------

st.title("Otimização de Rotas Hospitalares — Algoritmo Genético")
st.markdown(
    "Sistema de roteamento de veículos (VRP) para entrega de medicamentos em unidades hospitalares de São Paulo. "
    "Configure os parâmetros na barra lateral e clique em **Rodar Otimizacao**."
)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

tab_opt, tab_exp, tab_llm = st.tabs(["Otimizacao", "Experimentos", "LLM / Relatorio"])

# ===========================================================================
# TAB 1 — Otimização
# ===========================================================================

with tab_opt:
    if run_btn or "result" in st.session_state:

        if run_btn:
            with st.spinner("Rodando Algoritmo Genético..."):
                build_distance_matrix(points)
                result = run_genetic_algorithm(
                    points=points,
                    vehicles=vehicles,
                    population_size=pop_size,
                    generations=generations,
                    mutation_rate=mutation_rate,
                    seed=int(seed),
                )
                st.session_state["result"] = result

        result = st.session_state["result"]

        # --- Métricas principais ---
        improvement = (
            (1 - result.optimized_distance / result.initial_distance) * 100
            if result.initial_distance > 0 else 0.0
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Distância Inicial", f"{result.initial_distance:.2f} km")
        col2.metric(
            "Distância Otimizada", f"{result.optimized_distance:.2f} km",
            delta=f"-{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%",
            delta_color="normal",
        )
        col3.metric("Gerações executadas", result.generations)
        col4.metric("Veículos utilizados", len(result.routes))

        st.markdown("---")

        # --- Rotas detalhadas ---
        st.subheader("Rotas por Veículo")
        for route in result.routes:
            with st.expander(
                f"{route.vehicle.name} — {route.total_distance:.2f} km | "
                f"{route.total_load:.1f}/{route.vehicle.capacity} kg",
                expanded=True,
            ):
                cols = st.columns(len(route.stops)) if route.stops else []
                for i, (stop, col) in enumerate(zip(route.stops, cols)):
                    priority_icon = "CRITICO" if stop.priority == "critica" else ("ALTO" if stop.priority == "alta" else "MEDIO")
                    col.metric(
                        label=f"{i+1}. {stop.name}",
                        value=f"{stop.demand} kg",
                        delta=f"{priority_icon} — {stop.priority}",
                        delta_color="off",
                    )

        st.markdown("---")

        # --- Gráficos ---
        st.subheader("Gráficos")

        with tempfile.TemporaryDirectory() as tmpdir:
            path_conv = os.path.join(tmpdir, "convergence.png")
            path_comp = os.path.join(tmpdir, "distance_comparison.png")
            path_load = os.path.join(tmpdir, "vehicle_load.png")
            path_dist = os.path.join(tmpdir, "route_distances.png")

            plot_fitness_convergence(result, path_conv)
            plot_distance_comparison(result, path_comp)
            plot_vehicle_load(result, path_load)
            plot_route_distances(result, path_dist)

            col_a, col_b = st.columns(2)
            with col_a:
                st.image(path_conv, width="stretch")
                st.image(path_load, width="stretch")
            with col_b:
                st.image(path_comp, width="stretch")
                st.image(path_dist, width="stretch")

        st.markdown("---")

        # --- Mapas ---
        st.subheader("Mapas Interativos")

        map_tab1, map_tab2 = st.tabs(["Mapa de Rotas Otimizadas", "Comparativo Antes / Depois"])

        with tempfile.TemporaryDirectory() as tmpdir:
            route_map_path = os.path.join(tmpdir, "route_map.html")
            comparison_map_path = os.path.join(tmpdir, "comparison_map.html")

            create_route_map(result, points, output_path=route_map_path)
            create_comparison_map(result, points, output_path=comparison_map_path)

            with map_tab1:
                with open(route_map_path, "r", encoding="utf-8") as f:
                    components.html(f.read(), height=520, scrolling=False)

            with map_tab2:
                with open(comparison_map_path, "r", encoding="utf-8") as f:
                    components.html(f.read(), height=520, scrolling=False)

    else:
        st.info("Configure os parâmetros na barra lateral e clique em **Rodar Otimizacao**.")

# ===========================================================================
# TAB 2 — Experimentos
# ===========================================================================

with tab_exp:
    st.subheader("Experimentos Comparativos")
    st.markdown(
        "Compara 3 configurações diferentes do AG para encontrar a melhor combinação de parâmetros."
    )

    # Tabela dos experimentos configurados
    st.markdown("**Configurações testadas:**")
    exp_rows = []
    for e in EXPERIMENTS:
        exp_rows.append({
            "Experimento": f"#{e['id']} — {e['name']}",
            "Descricao": e["description"],
            "Pop.": e["population_size"],
            "Geracoes": e["generations"],
            "Mutacao": e["mutation_rate"],
            "Selecao": e["selection_type"],
        })
    st.dataframe(exp_rows, width="stretch", hide_index=True)

    run_exp_btn = st.button("Rodar os 3 Experimentos", type="primary")

    if run_exp_btn or "exp_results" in st.session_state:
        if run_exp_btn:
            with st.spinner("Rodando experimentos..."):
                exp_output_dir = os.path.join(tempfile.gettempdir(), "vrp_experiments")
                exp_results = run_experiments(output_dir=exp_output_dir)
                st.session_state["exp_results"] = exp_results
                st.session_state["exp_output_dir"] = exp_output_dir

        exp_results = st.session_state["exp_results"]
        exp_output_dir = st.session_state.get("exp_output_dir", "output/experiments")

        st.markdown("---")
        st.subheader("Resultados")

        ranked = sorted(exp_results, key=lambda r: -r["metrics"]["improvement_pct"])
        result_rows = []
        for i, r in enumerate(ranked):
            m = r["metrics"]
            result_rows.append({
                "Rank": f"#{i+1}",
                "Experimento": r["name"],
                "Dist. Inicial (km)": round(m["initial_distance_km"], 2),
                "Dist. Otimizada (km)": round(m["optimized_distance_km"], 2),
                "Melhoria (%)": round(m["improvement_pct"], 1),
                "Convergiu na Geracao": m["convergence_generation"],
                "Tempo (s)": round(m["elapsed_seconds"], 2),
            })
        st.dataframe(result_rows, width="stretch", hide_index=True)

        best = ranked[0]
        st.success(
            f"Melhor configuração: #{best['id']} — {best['name']} "
            f"| Melhoria: {best['metrics']['improvement_pct']:.1f}% "
            f"| Distância final: {best['metrics']['optimized_distance_km']:.2f} km"
        )

        st.markdown("---")
        st.subheader("Gráficos Comparativos")

        with tempfile.TemporaryDirectory() as tmpdir:
            plot_convergence_comparison(exp_results, tmpdir)
            plot_improvement_bar(exp_results, tmpdir)

            col_a, col_b = st.columns(2)
            with col_a:
                st.image(os.path.join(tmpdir, "convergence_comparison.png"), width="stretch")
            with col_b:
                st.image(os.path.join(tmpdir, "improvement_comparison.png"), width="stretch")

    else:
        st.info("Clique em **Rodar os 3 Experimentos** para iniciar a comparação.")

# ===========================================================================
# TAB 3 — LLM / Relatório
# ===========================================================================

with tab_llm:
    st.subheader("LLM — Instruções e Relatório")

    if "result" not in st.session_state:
        st.warning("Execute a otimização primeiro (aba **Otimizacao**).")
    else:
        result = st.session_state["result"]

        llm_tab1, llm_tab2, llm_tab3 = st.tabs(
            ["Instrucoes para Motoristas", "Relatorio Executivo", "Perguntas e Respostas"]
        )

        with llm_tab1:
            if st.button("Gerar Instrucoes para Motoristas", type="primary"):
                with st.spinner("Gerando instruções..."):
                    instructions = generate_driver_instructions(result, points)
                    st.session_state["driver_instructions"] = instructions

            if "driver_instructions" in st.session_state:
                st.code(st.session_state["driver_instructions"], language=None)

        with llm_tab2:
            exp_results_for_report = st.session_state.get("exp_results", None)
            if st.button("Gerar Relatorio Executivo", type="primary"):
                with st.spinner("Gerando relatório..."):
                    report = generate_route_report(result, exp_results_for_report)
                    st.session_state["exec_report"] = report

            if "exec_report" in st.session_state:
                st.code(st.session_state["exec_report"], language=None)

        with llm_tab3:
            st.markdown("Faça uma pergunta sobre as rotas otimizadas:")
            question = st.text_input(
                "Pergunta",
                placeholder="Ex: Quais pontos têm entrega crítica? Qual a distância total?",
                label_visibility="collapsed",
            )
            if st.button("Perguntar", type="primary") and question.strip():
                with st.spinner("Consultando..."):
                    answer = ask_question(question.strip(), result, points)
                    if "qa_history" not in st.session_state:
                        st.session_state["qa_history"] = []
                    st.session_state["qa_history"].append((question.strip(), answer))

            if "qa_history" in st.session_state:
                for q, a in reversed(st.session_state["qa_history"]):
                    with st.chat_message("user"):
                        st.write(q)
                    with st.chat_message("assistant"):
                        st.write(a)
