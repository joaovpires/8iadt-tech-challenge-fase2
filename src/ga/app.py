# =============================================================================
# MedRoute — Otimização de Rotas para Entrega de Medicamentos
# Tech Challenge · PosTech IA para Devs
#
# Este arquivo contém a interface visual da aplicação construída com Streamlit.
# O algoritmo genético está nos módulos da pasta /src/ga:
#   - src/ga/algorithm.py     → execução do algoritmo TSP geração a geração
#   - src/ga/algorithm_vrp.py → execução do algoritmo VRP com restrições
#   - src/ga/fitness.py       → cálculo de distância e aptidão de cada rota
#   - src/ga/cities.py        → geração aleatória de pontos ou carregamento do att48
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import random
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
import time

from algorithm import run_ga_visual
from fitness import calculate_distance, calculate_distance_att, calculate_fitness
from cities import generate_cities, load_att48
from algorithm_vrp import run_ga_vrp
from vrp_fitness import evaluate_vrp_solution, calculate_vrp_fitness
from vrp_models import Delivery, Vehicle

# =============================================================================
# PALETA DE CORES — tema escuro inspirado em saúde & logística
# =============================================================================
BG_COLOR     = "#060d1a"
PANEL_COLOR  = "#0d1b2a"
CARD_COLOR   = "#112236"
BORDER_COLOR = "#1a3a5c"
TEXT_COLOR   = "#e8f4f8"
TEXT_MUTED   = "#7a9bb5"
GREEN        = "#00c896"
BLUE         = "#0ea5e9"
AMBER        = "#f59e0b"
TEAL         = "#14b8a6"
POP_CLR      = "#1e4a7a"

VEHICLE_COLORS = ["#00c896", "#0ea5e9", "#f59e0b", "#e05b8b", "#a78bfa", "#34d399"]

PRIORITY_COLOR = {
    0: TEAL,       # normal
    1: "#e05b8b",  # alta
    2: AMBER,      # média
}

# =============================================================================
# CONFIGURAÇÃO GLOBAL DO MATPLOTLIB
# =============================================================================
mpl.rcParams.update({
    "figure.facecolor": PANEL_COLOR,
    "axes.facecolor":   PANEL_COLOR,
    "axes.edgecolor":   BORDER_COLOR,
    "axes.labelcolor":  TEXT_MUTED,
    "axes.titlecolor":  TEXT_MUTED,
    "xtick.color":      TEXT_MUTED,
    "ytick.color":      TEXT_MUTED,
    "grid.color":       BORDER_COLOR,
    "grid.linestyle":   "--",
    "grid.alpha":       0.4,
    "text.color":       TEXT_COLOR,
    "font.family":      "sans-serif",
    "axes.titlesize":   10,
    "axes.labelsize":   8,
    "xtick.labelsize":  7,
    "ytick.labelsize":  7,
})


# =============================================================================
# CONFIGURAÇÃO DA PÁGINA STREAMLIT
# =============================================================================
st.set_page_config(
    page_title="MedRoute — Otimização de Rotas",
    page_icon="💊",
    layout="wide"
)


# =============================================================================
# ESTILOS CSS GLOBAIS
# =============================================================================
st.markdown(f"""
<style>
    .stApp {{ background-color: {BG_COLOR}; }}
    .block-container {{
        padding: 2.8rem 0 0 0 !important;
        max-width: 100% !important;
    }}
    header[data-testid="stHeader"] {{
        background-color: {BG_COLOR} !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {PANEL_COLOR} !important;
        border-right: 1px solid {BORDER_COLOR};
    }}
    section[data-testid="stSidebar"] label {{
        color: {TEXT_MUTED} !important;
        font-size: 0.75rem !important;
    }}
    section[data-testid="stSidebar"] p {{
        color: {TEXT_MUTED} !important;
        font-size: 0.75rem !important;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {GREEN}, #00a878) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        border-radius: 8px !important;
        width: 100% !important;
        padding: 0.6rem !important;
        letter-spacing: 0.05em !important;
        transition: all 0.2s !important;
    }}
    .stButton > button p {{
        color: #ffffff !important;
        font-weight: 700 !important;
    }}
    .stButton > button:hover {{
        box-shadow: 0 0 20px {GREEN}88 !important;
    }}
    [data-testid="stMetric"] {{
        background: {CARD_COLOR};
        border: 1px solid {BORDER_COLOR};
        border-radius: 10px;
        padding: 0.8rem 1rem !important;
    }}
    [data-testid="stMetricLabel"] p {{
        color: {TEXT_MUTED} !important;
        font-size: 0.68rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    [data-testid="stMetricValue"] {{
        color: {TEXT_COLOR} !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }}
    #MainMenu, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HEADER DA APLICAÇÃO
# =============================================================================
st.markdown(f"""
<div style="background:linear-gradient(135deg, {PANEL_COLOR}, {CARD_COLOR});
            border-bottom:1px solid {BORDER_COLOR};
            padding:1rem 2rem; display:flex; align-items:center; gap:1.2rem;">
    <div style="font-size:2.2rem;">💊</div>
    <div>
        <div style="color:{TEXT_COLOR}; font-size:1.5rem; font-weight:700;
                    letter-spacing:-0.02em; line-height:1.1;">MedRoute</div>
        <div style="color:{TEXT_MUTED}; font-size:0.72rem; font-weight:300;
                    letter-spacing:0.06em; text-transform:uppercase;">
            Otimização de Rotas para Entrega de Medicamentos
        </div>
    </div>
    <div style="margin-left:auto; text-align:right;">
        <div style="color:{GREEN}; font-size:0.68rem; font-weight:600; letter-spacing:0.1em;">
            ● Algoritmo Genético + LLM
        </div>
        <div style="color:{TEXT_MUTED}; font-size:0.62rem; font-weight:300;">
            Tech Challenge · PosTech IA para Devs
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# SIDEBAR — PAINEL DE PARÂMETROS
# =============================================================================
st.sidebar.markdown(f"""
<div style="padding:1rem 0 0.8rem 0; border-bottom:1px solid {BORDER_COLOR}; margin-bottom:0.8rem;">
    <div style="color:{GREEN}; font-size:0.68rem; font-weight:600;
                letter-spacing:0.12em; text-transform:uppercase;">⚙️ Parâmetros</div>
</div>
""", unsafe_allow_html=True)

# Seleção do modo de otimização
modo = st.sidebar.radio(
    "Modo de otimização",
    ["TSP — Caixeiro Viajante", "VRP — Com Restrições"],
)

st.sidebar.markdown(
    f"<div style='border-top:1px solid {BORDER_COLOR}; margin:0.5rem 0;'></div>",
    unsafe_allow_html=True,
)

# ---- Parâmetros específicos por modo ----
if modo == "TSP — Caixeiro Viajante":
    dataset_option = st.sidebar.selectbox(
        "Pontos de entrega",
        ["Aleatórios", "att48 (TSPLIB)"],
    )
    if dataset_option == "Aleatórios":
        num_cities = st.sidebar.slider("Nº de pontos", 5, 50, 20, key="num_cities_slider")
    else:
        st.sidebar.caption("48 pontos fixos — benchmark TSPLIB")
        num_cities = 48
    delay = st.sidebar.slider("Delay (s)", 0.0, 0.5, 0.05)

else:  # VRP
    num_deliveries   = st.sidebar.slider("Nº de entregas (clientes)", 5, 30, 10)
    num_vehicles     = st.sidebar.slider("Nº de veículos", 1, 6, 3)
    vehicle_capacity = st.sidebar.slider("Capacidade do veículo", 10, 200, 50)
    vehicle_max_dist = st.sidebar.slider("Autonomia máxima", 100, 1000, 400)
    max_demand       = st.sidebar.slider("Demanda máx. por entrega", 1, 30, 10)

st.sidebar.markdown(
    f"<div style='border-top:1px solid {BORDER_COLOR}; margin:0.5rem 0;'></div>",
    unsafe_allow_html=True,
)

# ---- Parâmetros comuns do algoritmo genético ----
population       = st.sidebar.slider("Tamanho da população", 50, 500, 200)
mutation         = st.sidebar.slider("Taxa de mutação", 0.0, 1.0, 0.2)
generations      = st.sidebar.slider("Gerações", 10, 300, 100)
selection_method = st.sidebar.selectbox("Seleção", ["tournament", "top10", "roulette"])

# Legenda visual
if modo == "TSP — Caixeiro Viajante":
    st.sidebar.markdown(f"""
<div style="margin:0.8rem 0; border-top:1px solid {BORDER_COLOR}; padding-top:0.8rem;">
    <div style="color:{TEXT_MUTED}; font-size:0.65rem; font-weight:600;
                letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.5rem;">Legenda</div>
    <div style="font-size:0.82rem; color:{TEXT_MUTED}; line-height:2;">
        <div><span style="color:{GREEN}; font-size:0.9rem;">━</span> Melhor rota</div>
        <div><span style="color:{POP_CLR}; font-size:0.9rem;">━</span> Rotas alternativas</div>
        <div><span style="color:#e05b8b;">●</span> Ponto de entrega</div>
        <div><span style="color:{AMBER};">●</span> Depósito central</div>
    </div>
</div>
""", unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"""
<div style="margin:0.8rem 0; border-top:1px solid {BORDER_COLOR}; padding-top:0.8rem;">
    <div style="color:{TEXT_MUTED}; font-size:0.65rem; font-weight:600;
                letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.5rem;">Legenda</div>
    <div style="font-size:0.82rem; color:{TEXT_MUTED}; line-height:2;">
        <div><span style="color:{AMBER};">●</span> Depósito central</div>
        <div><span style="color:#e05b8b;">●</span> Prioridade Alta</div>
        <div><span style="color:{AMBER};">●</span> Prioridade Média</div>
        <div><span style="color:{TEAL};">●</span> Prioridade Normal</div>
        <div><span style="font-size:0.9rem;">━</span> Cada cor = 1 veículo</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Botão que dispara a execução
rodar = st.sidebar.button("▶  INICIAR OTIMIZAÇÃO")


# =============================================================================
# TELA DE BOAS-VINDAS
# =============================================================================
if not rodar:
    st.markdown(f"""
<div style="padding:3rem 2rem; text-align:center;">
<div style="font-size:3.5rem; margin-bottom:1rem;">🏥</div>
<div style="color:{TEXT_COLOR}; font-size:1.2rem; font-weight:600; margin-bottom:0.5rem;">Pronto para otimizar</div>
<div style="color:{TEXT_MUTED}; font-size:0.82rem; font-weight:300; max-width:480px; margin:0 auto; line-height:1.7;">
Escolha o modo, configure os parâmetros e clique em
<span style="color:{GREEN}; font-weight:600;">Iniciar Otimização</span>.
</div>
<div style="display:flex; justify-content:center; gap:1.5rem; margin-top:2.5rem; flex-wrap:wrap;">
<div style="background:{CARD_COLOR}; border:1px solid {BORDER_COLOR}; border-radius:12px; padding:1.2rem 1.5rem; text-align:center; min-width:160px;">
<div style="font-size:1.6rem;">🧬</div>
<div style="color:{GREEN}; font-size:0.65rem; font-weight:600; letter-spacing:0.08em; margin-top:0.4rem;">ALGORITMO GENÉTICO</div>
<div style="color:{TEXT_MUTED}; font-size:0.68rem; margin-top:0.3rem;">Seleção · Cruzamento · Mutação</div>
</div>
<div style="background:{CARD_COLOR}; border:1px solid {BORDER_COLOR}; border-radius:12px; padding:1.2rem 1.5rem; text-align:center; min-width:160px;">
<div style="font-size:1.6rem;">🗺️</div>
<div style="color:{BLUE}; font-size:0.65rem; font-weight:600; letter-spacing:0.08em; margin-top:0.4rem;">TSP — CAIXEIRO VIAJANTE</div>
<div style="color:{TEXT_MUTED}; font-size:0.68rem; margin-top:0.3rem;">Minimização de distância total</div>
</div>
<div style="background:{CARD_COLOR}; border:1px solid {BORDER_COLOR}; border-radius:12px; padding:1.2rem 1.5rem; text-align:center; min-width:160px;">
<div style="font-size:1.6rem;">🚚</div>
<div style="color:{GREEN}; font-size:0.65rem; font-weight:600; letter-spacing:0.08em; margin-top:0.4rem;">VRP — COM RESTRIÇÕES</div>
<div style="color:{TEXT_MUTED}; font-size:0.68rem; margin-top:0.3rem;">Capacidade · Prioridade · Autonomia</div>
</div>
<div style="background:{CARD_COLOR}; border:1px solid {BORDER_COLOR}; border-radius:12px; padding:1.2rem 1.5rem; text-align:center; min-width:160px;">
<div style="font-size:1.6rem;">🤖</div>
<div style="color:{AMBER}; font-size:0.65rem; font-weight:600; letter-spacing:0.08em; margin-top:0.4rem;">ANÁLISE COM LLM</div>
<div style="color:{TEXT_MUTED}; font-size:0.68rem; margin-top:0.3rem;">Interpretação dos resultados</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# EXECUÇÃO DO ALGORITMO GENÉTICO
# =============================================================================
if rodar:

    # --------------------------------------------------------------------------
    # MODO TSP — Caixeiro Viajante
    # --------------------------------------------------------------------------
    if modo == "TSP — Caixeiro Viajante":

        if dataset_option == "Aleatórios":
            cities = generate_cities(num_cities)
            distance_function = calculate_distance
        else:
            cities = load_att48()
            distance_function = calculate_distance_att

        history, best_routes, populations = run_ga_visual(
            cities, population, mutation, 3,
            generations, selection_method, distance_function
        )

        st.markdown(f"<div style='padding:0.6rem 1.5rem 0 1.5rem;'>", unsafe_allow_html=True)
        col1, col2 = st.columns([6, 4], vertical_alignment="top")
        st.markdown("</div>", unsafe_allow_html=True)

        route_placeholder  = col1.empty()
        status_placeholder = col1.empty()
        fit_placeholder    = col2.empty()
        hist_placeholder   = col2.empty()

        x_vals, y_vals = zip(*cities)
        padding_x = (max(x_vals) - min(x_vals)) * 0.08 + 5
        padding_y = (max(y_vals) - min(y_vals)) * 0.08 + 5
        x_min, x_max = min(x_vals) - padding_x, max(x_vals) + padding_x
        y_min, y_max = min(y_vals) - padding_y, max(y_vals) + padding_y

        start_time    = time.time()
        distancia_ini = history[0]

        for gen in range(len(history)):

            elapsed = time.time() - start_time
            pct = (gen + 1) / len(history) * 100

            fig, ax = plt.subplots(figsize=(5.5, 3.0))
            fig.patch.set_facecolor(PANEL_COLOR)

            for route in populations[gen]:
                rc = [cities[i] for i in route] + [cities[route[0]]]
                rx, ry = zip(*rc)
                ax.plot(rx, ry, color=POP_CLR, linewidth=0.3, zorder=1, alpha=0.18)

            best_rc = [cities[i] for i in best_routes[gen]] + [cities[best_routes[gen][0]]]
            bx, by  = list(zip(*best_rc))
            n_seg   = len(bx) - 1

            cmap_route = mpl.colors.LinearSegmentedColormap.from_list("rota", [GREEN, TEAL])

            for si in range(n_seg):
                t   = si / max(n_seg - 1, 1)
                cor = cmap_route(t)
                sx, sy = [bx[si], bx[si+1]], [by[si], by[si+1]]
                ax.plot(sx, sy, color=cor, linewidth=6,   zorder=2, alpha=0.04)
                ax.plot(sx, sy, color=cor, linewidth=3,   zorder=2, alpha=0.08)
                ax.plot(sx, sy, color=cor, linewidth=1.6, zorder=3, alpha=0.9)
                mx, my = (bx[si] + bx[si+1]) / 2, (by[si] + by[si+1]) / 2
                dx, dy = bx[si+1] - bx[si], by[si+1] - by[si]
                ax.annotate("", xy=(mx + dx*0.01, my + dy*0.01),
                            xytext=(mx - dx*0.01, my - dy*0.01),
                            arrowprops=dict(arrowstyle="-|>", color=cor,
                                            lw=1.2, mutation_scale=8),
                            zorder=4)

            depot_idx = best_routes[gen][0]

            for idx, (cx, cy) in enumerate(cities):
                if idx == depot_idx:
                    continue
                ax.scatter(cx, cy, s=60, marker="o",
                           facecolor="#1a2f4a", edgecolor="#e05b8b",
                           linewidth=1.2, zorder=5)
                ax.annotate("+", (cx, cy), fontsize=8, color="#e05b8b",
                            ha="center", va="center", fontweight="bold", zorder=6)
                if gen == len(history) - 1:
                    offset = (y_max - y_min) * 0.04
                    ax.text(cx, cy + offset, str(idx),
                            fontsize=6, color=TEXT_COLOR,
                            ha="center", va="bottom", zorder=8)

            depot   = cities[depot_idx]
            depot_r = (x_max - x_min) * 0.025
            ax.add_patch(plt.Circle(depot, depot_r, color=AMBER, zorder=5, alpha=0.9))
            ax.add_patch(plt.Circle(depot, depot_r, fill=False, edgecolor="white",
                                    linewidth=1.5, zorder=6))
            ax.text(depot[0], depot[1], "+", fontsize=12, color="#cc0000",
                    ha="center", va="center", fontweight="bold", zorder=7)

            label_txt = f"Geração {gen+1} / {len(history)}   ·   Melhor rota: "
            ax.text(0.5, 1.03, label_txt,
                    transform=ax.transAxes, ha="right", va="bottom",
                    fontsize=10, color=TEXT_MUTED)
            ax.text(0.5, 1.03, f"{history[gen]:.0f}",
                    transform=ax.transAxes, ha="left", va="bottom",
                    fontsize=10, color=GREEN, fontweight="bold")

            for spine in ax.spines.values():
                spine.set_edgecolor(BORDER_COLOR)
                spine.set_linewidth(1.2)

            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            ax.grid(True, alpha=0.3)
            fig.tight_layout(pad=0.6)
            route_placeholder.pyplot(fig, use_container_width=True)
            plt.close(fig)

            status_placeholder.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.8rem;
                        padding:0.25rem 0.3rem; font-size:0.72rem; color:{TEXT_MUTED};">
                <span>⏱️ <b style="color:{BLUE}">{elapsed:.1f}s</b></span>
                <span>·</span>
                <span><b style="color:{GREEN}">{pct:.0f}%</b> concluído</span>
                <div style="flex:1; background:{BORDER_COLOR}; border-radius:4px; height:3px; overflow:hidden;">
                    <div style="width:{pct}%; background:linear-gradient(90deg,{GREEN},{BLUE});
                                height:100%; border-radius:4px; transition:width 0.3s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            distances = [calculate_fitness(r, cities, distance_function) for r in populations[gen]]

            fig_fit, ax_fit = plt.subplots(figsize=(5, 2.1))
            xs, ys = list(range(gen + 1)), history[:gen + 1]
            ax_fit.plot(xs, ys, color=TEAL, linewidth=2.2,
                        marker="o", markersize=3.5,
                        markerfacecolor=AMBER, markeredgecolor=BG_COLOR,
                        markeredgewidth=0.5, zorder=3)
            ax_fit.fill_between(xs, ys, min(ys), alpha=0.18, color=TEAL, zorder=2)
            margem = (max(ys) - min(ys)) * 0.25 + 1
            ax_fit.set_ylim(min(ys) - margem, max(ys) + margem)
            ax_fit.set_xlim(0, len(history) - 1)
            ax_fit.axhline(min(ys), color=GREEN, linewidth=1.2, linestyle="--",
                           alpha=0.8, label=f"Mín: {min(ys):.0f}")
            if gen > 0 and ys[-1] < ys[-2]:
                ax_fit.scatter([gen], [ys[-1]], color=GREEN, s=40, zorder=5,
                               edgecolors="white", linewidths=0.8)
            ax_fit.legend(fontsize=7, facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR, loc="upper right")
            ax_fit.set_xlabel("Geração")
            ax_fit.set_ylabel("Distância")
            ax_fit.set_title("Convergência — melhor rota por geração")
            for spine in ax_fit.spines.values():
                spine.set_edgecolor(BORDER_COLOR)
            ax_fit.grid(True, alpha=0.3)
            fig_fit.tight_layout(pad=0.5)
            fit_placeholder.pyplot(fig_fit, use_container_width=True)
            plt.close(fig_fit)

            fig_hist, ax_hist = plt.subplots(figsize=(5, 2.1))
            n, bins, patches = ax_hist.hist(distances, bins=15,
                                            edgecolor=BG_COLOR, linewidth=0.4, alpha=0.92)
            cmap = mpl.cm.get_cmap("RdYlGn_r")
            norm = mpl.colors.Normalize(vmin=0, vmax=len(patches) - 1)
            for i, patch in enumerate(patches):
                patch.set_facecolor(cmap(norm(i)))
            ax_hist.axvline(history[gen], color=GREEN, linewidth=1.4,
                            linestyle="--", label=f"Melhor: {history[gen]:.0f}")
            ax_hist.legend(fontsize=7, facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR, loc="upper right")
            ax_hist.set_xlabel("Distância total da rota")
            ax_hist.set_ylabel("Nº de rotas")
            ax_hist.set_title(f"Distribuição da população — Geração {gen+1}")
            ax_hist.grid(True, axis='y')
            fig_hist.tight_layout(pad=0.5)
            hist_placeholder.pyplot(fig_hist, use_container_width=True)
            plt.close(fig_hist)

            time.sleep(delay)

        # Resultado final TSP
        best_found  = round(history[-1], 2)
        melhoria    = ((distancia_ini - best_found) / distancia_ini) * 100
        tempo_total = round(time.time() - start_time, 1)
        dist_media  = round(best_found / len(cities), 2)
        economia    = round(distancia_ini - best_found)
        min_val     = min(history)
        gen_convergiu = next(i + 1 for i, v in enumerate(history) if v == min_val)

        st.markdown(f"""
        <div style="padding:0.8rem 1.5rem 0.4rem 1.5rem;">
            <div style="color:{GREEN}; font-size:0.65rem; font-weight:600;
                        letter-spacing:0.12em; text-transform:uppercase;">
                ✅ Otimização concluída
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric("Rota sem otimização", f"{distancia_ini:.0f}",
                      help="Distância da primeira rota gerada aleatoriamente")
        with c2:
            st.metric("Melhor rota encontrada", f"{round(best_found):.0f}",
                      delta=f"-{economia} ({melhoria:.1f}%)",
                      delta_color="inverse",
                      help="Menor distância encontrada pelo algoritmo genético")
        with c3:
            st.metric("Economia de distância", f"{melhoria:.1f}%",
                      help="Percentual de redução em relação à rota inicial")
        with c4:
            st.metric("Distância média por parada", f"{dist_media:.0f}",
                      help="Distância total dividida pelo número de pontos de entrega")
        with c5:
            st.metric("Solução encontrada na geração", f"{gen_convergiu} / {len(history)}",
                      help="A partir desta geração a rota não melhorou mais")

        best_final = best_routes[-1]
        paradas    = list(best_final) + [best_final[0]]
        n_paradas  = len(best_final) - 1
        itens = []
        for i, idx in enumerate(paradas):
            if i == 0:
                itens.append(f"📍 Depósito #{idx}")
            elif i == len(paradas) - 1:
                itens.append(f"🏁 Depósito #{idx}")
            else:
                itens.append(f"#{idx}")
        seq_linha = "  →  ".join(itens)

        st.markdown(f"""
<div style="margin:0.6rem 0 0 0; background:#112236; border:1px solid #1a3a5c;
            border-radius:10px; padding:1rem 1.2rem;">
    <div style="color:#7a9bb5; font-size:0.65rem; font-weight:600;
                letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.7rem;">
        📦 Sequência de entregas — {n_paradas} paradas
    </div>
    <div style="color:#e8f4f8; font-size:0.8rem; line-height:2.2; word-break:break-word;">
        {seq_linha}
    </div>
</div>
""", unsafe_allow_html=True)

        if dataset_option == "att48 (TSPLIB)":
            best_known = 10628
            error = ((best_found - best_known) / best_known) * 100
            st.markdown(f"""
<div style="margin:0.4rem 0 0 0; color:#7a9bb5; font-size:0.75rem;">
    📌 <b>Benchmark att48</b> — Ótimo conhecido: <b style="color:#e8f4f8">{best_known}</b> · Erro: <b style="color:#f59e0b">{error:.2f}%</b>
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # MODO VRP — Com Restrições
    # --------------------------------------------------------------------------
    else:
        # Gera dados aleatórios
        depot = Delivery(id=0, x=50.0, y=50.0, demand=0, priority=0)
        deliveries = [depot] + [
            Delivery(
                id=i + 1,
                x=random.uniform(5, 95),
                y=random.uniform(5, 95),
                demand=random.randint(1, max_demand),
                priority=random.randint(0, 2),
            )
            for i in range(num_deliveries)
        ]
        vehicles = [
            Vehicle(id=i, capacity=vehicle_capacity, max_distance=vehicle_max_dist)
            for i in range(num_vehicles)
        ]

        start_time = time.time()

        with st.spinner("Executando algoritmo genético VRP..."):
            history, best_solutions = run_ga_vrp(
                deliveries=deliveries,
                vehicles=vehicles,
                population_size=population,
                mutation_probability=mutation,
                max_generations=generations,
                selection_type=selection_method,
            )

        tempo_total = round(time.time() - start_time, 1)
        best = best_solutions[-1]

        st.markdown(f"""
        <div style="padding:0.8rem 1.5rem 0.4rem 1.5rem;">
            <div style="color:{GREEN}; font-size:0.65rem; font-weight:600;
                        letter-spacing:0.12em; text-transform:uppercase;">
                ✅ Otimização VRP concluída
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Métricas
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric("Fitness inicial", f"{history[0]:.0f}",
                      help="Fitness da melhor solução na geração 1")
        with c2:
            melhoria_vrp = ((history[0] - history[-1]) / max(history[0], 1)) * 100
            st.metric("Melhor fitness", f"{history[-1]:.0f}",
                      delta=f"-{history[0]-history[-1]:.0f} ({melhoria_vrp:.1f}%)",
                      delta_color="inverse",
                      help="Menor fitness encontrado (distância + penalidades)")
        with c3:
            st.metric("Distância total", f"{best['total_distance']:.0f}",
                      help="Soma das distâncias percorridas por todos os veículos")
        with c4:
            st.metric("Penalidade", f"{best['penalty']:.0f}",
                      help="Penalidades por violações de capacidade, autonomia e prioridade")
        with c5:
            st.metric("Rotas geradas", f"{len(best['routes'])} / {num_vehicles}",
                      help="Número de rotas na melhor solução vs veículos disponíveis")

        # Layout: mapa | convergência
        col1, col2 = st.columns([6, 4], vertical_alignment="top")

        # --- Mapa VRP ---
        with col1:
            fig, ax = plt.subplots(figsize=(5.5, 4.0))
            fig.patch.set_facecolor(PANEL_COLOR)

            points = {d.id: d for d in deliveries}

            # Desenha cada rota com a cor do veículo correspondente
            for v_idx, route in enumerate(best["routes"]):
                color = VEHICLE_COLORS[v_idx % len(VEHICLE_COLORS)]
                xs_r = [points[g].x for g in route]
                ys_r = [points[g].y for g in route]
                ax.plot(xs_r, ys_r, color=color, linewidth=2.0,
                        zorder=3, alpha=0.85, label=f"Veículo {v_idx + 1}")

                # Setas de direção
                for si in range(len(route) - 1):
                    p1, p2 = points[route[si]], points[route[si + 1]]
                    mx, my = (p1.x + p2.x) / 2, (p1.y + p2.y) / 2
                    dx, dy = p2.x - p1.x, p2.y - p1.y
                    ax.annotate("", xy=(mx + dx * 0.01, my + dy * 0.01),
                                xytext=(mx - dx * 0.01, my - dy * 0.01),
                                arrowprops=dict(arrowstyle="-|>", color=color,
                                                lw=1.0, mutation_scale=7),
                                zorder=4)

            # Desenha os pontos de entrega coloridos por prioridade
            for d in deliveries:
                if d.id == 0:
                    continue
                pcolor = PRIORITY_COLOR.get(d.priority, TEAL)
                ax.scatter(d.x, d.y, s=70, marker="o",
                           facecolor="#1a2f4a", edgecolor=pcolor,
                           linewidth=1.5, zorder=5)
                ax.text(d.x, d.y + 2.5, str(d.id),
                        fontsize=6, color=TEXT_COLOR,
                        ha="center", va="bottom", zorder=8)

            # Depósito
            depot_r = 2.5
            ax.add_patch(plt.Circle((depot.x, depot.y), depot_r,
                                    color=AMBER, zorder=5, alpha=0.9))
            ax.add_patch(plt.Circle((depot.x, depot.y), depot_r,
                                    fill=False, edgecolor="white",
                                    linewidth=1.5, zorder=6))
            ax.text(depot.x, depot.y, "+", fontsize=12, color="#cc0000",
                    ha="center", va="center", fontweight="bold", zorder=7)

            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)
            ax.set_title(f"Melhor solução VRP — {len(best['routes'])} rotas")
            ax.legend(fontsize=7, facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR,
                      loc="upper right", ncol=2)
            ax.grid(True, alpha=0.3)
            for spine in ax.spines.values():
                spine.set_edgecolor(BORDER_COLOR)
            fig.tight_layout(pad=0.6)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        # --- Gráficos de convergência e distribuição ---
        with col2:
            # Convergência
            fig_fit, ax_fit = plt.subplots(figsize=(5, 2.5))
            xs = list(range(len(history)))
            ax_fit.plot(xs, history, color=TEAL, linewidth=2.2,
                        marker="o", markersize=3.0,
                        markerfacecolor=AMBER, markeredgecolor=BG_COLOR,
                        markeredgewidth=0.5, zorder=3)
            ax_fit.fill_between(xs, history, min(history), alpha=0.18, color=TEAL, zorder=2)
            margem = (max(history) - min(history)) * 0.15 + 1
            ax_fit.set_ylim(min(history) - margem, max(history) + margem)
            ax_fit.axhline(min(history), color=GREEN, linewidth=1.2, linestyle="--",
                           alpha=0.8, label=f"Mín: {min(history):.0f}")
            ax_fit.legend(fontsize=7, facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR, loc="upper right")
            ax_fit.set_xlabel("Geração")
            ax_fit.set_ylabel("Fitness")
            ax_fit.set_title("Convergência — melhor fitness por geração")
            ax_fit.grid(True, alpha=0.3)
            for spine in ax_fit.spines.values():
                spine.set_edgecolor(BORDER_COLOR)
            fig_fit.tight_layout(pad=0.5)
            st.pyplot(fig_fit, use_container_width=True)
            plt.close(fig_fit)

            # Detalhe por rota
            fig_bar, ax_bar = plt.subplots(figsize=(5, 2.5))
            route_labels = [f"V{i+1}" for i in range(len(best["routes"]))]
            route_dists  = []
            for v_idx, route in enumerate(best["routes"]):
                import math
                dist = 0
                for si in range(len(route) - 1):
                    p1, p2 = points[route[si]], points[route[si + 1]]
                    dist += math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
                route_dists.append(dist)

            bars = ax_bar.bar(route_labels, route_dists,
                              color=[VEHICLE_COLORS[i % len(VEHICLE_COLORS)]
                                     for i in range(len(route_labels))],
                              edgecolor=BG_COLOR, linewidth=0.5)
            ax_bar.axhline(vehicle_max_dist, color="#e05b8b", linewidth=1.2,
                           linestyle="--", alpha=0.8, label=f"Autonomia: {vehicle_max_dist}")
            ax_bar.legend(fontsize=7, facecolor=PANEL_COLOR, edgecolor=BORDER_COLOR)
            ax_bar.set_xlabel("Veículo")
            ax_bar.set_ylabel("Distância")
            ax_bar.set_title("Distância por veículo")
            ax_bar.grid(True, axis="y", alpha=0.3)
            for spine in ax_bar.spines.values():
                spine.set_edgecolor(BORDER_COLOR)
            fig_bar.tight_layout(pad=0.5)
            st.pyplot(fig_bar, use_container_width=True)
            plt.close(fig_bar)

        # Sequência por veículo
        st.markdown(f"""
<div style="margin:0.6rem 0 0 0; background:{CARD_COLOR}; border:1px solid {BORDER_COLOR};
            border-radius:10px; padding:1rem 1.2rem;">
    <div style="color:{TEXT_MUTED}; font-size:0.65rem; font-weight:600;
                letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.7rem;">
        📦 Rotas por veículo
    </div>
""", unsafe_allow_html=True)

        for v_idx, route in enumerate(best["routes"]):
            color = VEHICLE_COLORS[v_idx % len(VEHICLE_COLORS)]
            stops = [f"📍 Depósito" if g == 0 else f"#{g}(P{points[g].priority},D{points[g].demand})"
                     for g in route]
            seq = "  →  ".join(stops)
            st.markdown(f"""
<div style="font-size:0.78rem; color:{TEXT_COLOR}; margin-bottom:0.5rem; line-height:1.8;">
    <span style="color:{color}; font-weight:700;">Veículo {v_idx + 1}</span>
    &nbsp;·&nbsp;
    {seq}
</div>
""", unsafe_allow_html=True)

        if best["missing_clients"] > 0:
            st.markdown(f"""
<div style="color:#e05b8b; font-size:0.75rem; margin-top:0.5rem;">
    ⚠️ {best['missing_clients']} cliente(s) não atendido(s) na melhor solução.
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
