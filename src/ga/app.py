# =============================================================================
# MedRoute — Otimização de Rotas para Entrega de Medicamentos
# Tech Challenge · PosTech IA para Devs
#
# Este arquivo contém a interface visual da aplicação construída com Streamlit.
# O algoritmo genético está nos módulos da pasta /src/ga:
#   - src/ga/algorithm.py  → execução do algoritmo geração a geração
#   - src/ga/fitness.py    → cálculo de distância e aptidão de cada rota
#   - src/ga/cities.py     → geração aleatória de pontos ou carregamento do att48
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
import time

from algorithm import run_ga_visual
from fitness import calculate_distance, calculate_distance_att, calculate_fitness
from cities import generate_cities, load_att48


# =============================================================================
# PALETA DE CORES — tema escuro inspirado em saúde & logística
# Todas as cores são definidas aqui para facilitar manutenção e consistência
# =============================================================================
BG_COLOR     = "#060d1a"   # fundo geral da página
PANEL_COLOR  = "#0d1b2a"   # fundo dos painéis e gráficos
CARD_COLOR   = "#112236"   # fundo dos cards de métricas
BORDER_COLOR = "#1a3a5c"   # cor das bordas e separadores
TEXT_COLOR   = "#e8f4f8"   # texto principal (quase branco)
TEXT_MUTED   = "#7a9bb5"   # texto secundário (azul acinzentado)
GREEN        = "#00c896"   # cor de destaque: melhor rota, métricas positivas
BLUE         = "#0ea5e9"   # cor de destaque: informações gerais
AMBER        = "#f59e0b"   # cor do depósito central
TEAL         = "#14b8a6"   # cor secundária da rota (gradiente verde→teal)
POP_CLR      = "#1e4a7a"   # cor das rotas alternativas da população


# =============================================================================
# CONFIGURAÇÃO GLOBAL DO MATPLOTLIB
# Define o estilo visual de todos os gráficos gerados durante a animação
# =============================================================================
mpl.rcParams.update({
    "figure.facecolor": PANEL_COLOR,   # fundo da figura
    "axes.facecolor":   PANEL_COLOR,   # fundo da área do gráfico
    "axes.edgecolor":   BORDER_COLOR,  # borda dos eixos
    "axes.labelcolor":  TEXT_MUTED,    # cor dos rótulos dos eixos
    "axes.titlecolor":  TEXT_MUTED,    # cor do título do gráfico
    "xtick.color":      TEXT_MUTED,    # cor dos ticks do eixo X
    "ytick.color":      TEXT_MUTED,    # cor dos ticks do eixo Y
    "grid.color":       BORDER_COLOR,  # cor da grade
    "grid.linestyle":   "--",          # estilo da grade (tracejado)
    "grid.alpha":       0.4,           # transparência da grade
    "text.color":       TEXT_COLOR,    # cor padrão do texto
    "font.family":      "sans-serif",  # família de fonte
    "axes.titlesize":   10,            # tamanho do título
    "axes.labelsize":   8,             # tamanho dos rótulos
    "xtick.labelsize":  7,             # tamanho dos valores no eixo X
    "ytick.labelsize":  7,             # tamanho dos valores no eixo Y
})


# =============================================================================
# CONFIGURAÇÃO DA PÁGINA STREAMLIT
# Define título, ícone e layout da aplicação
# =============================================================================
st.set_page_config(
    page_title="MedRoute — Otimização de Rotas",
    page_icon="💊",
    layout="wide"   # usa toda a largura da tela
)


# =============================================================================
# ESTILOS CSS GLOBAIS
# Personaliza componentes do Streamlit que não têm API nativa de estilo,
# como fundo da página, sidebar, botões e cards de métricas
# =============================================================================
st.markdown(f"""
<style>
    /* Fundo geral da aplicação */
    .stApp {{ background-color: {BG_COLOR}; }}

    /* Remove padding padrão do container principal */
    .block-container {{
        padding: 2.8rem 0 0 0 !important;
        max-width: 100% !important;
    }}

    /* Fundo do header do Streamlit */
    header[data-testid="stHeader"] {{
        background-color: {BG_COLOR} !important;
    }}

    /* Estilo da sidebar */
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

    /* Estilo do botão principal */
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

    /* Estilo dos cards de métricas (st.metric) */
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

    /* Oculta menu e rodapé padrão do Streamlit */
    #MainMenu, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HEADER DA APLICAÇÃO
# Barra superior com nome do projeto, subtítulo e badge de tecnologia
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
# Permite ao usuário configurar o algoritmo genético antes de executar
# =============================================================================
st.sidebar.markdown(f"""
<div style="padding:1rem 0 0.8rem 0; border-bottom:1px solid {BORDER_COLOR}; margin-bottom:0.8rem;">
    <div style="color:{GREEN}; font-size:0.68rem; font-weight:600;
                letter-spacing:0.12em; text-transform:uppercase;">⚙️ Parâmetros</div>
</div>
""", unsafe_allow_html=True)

# Escolha do dataset: pontos aleatórios ou benchmark TSPLIB att48
dataset_option = st.sidebar.selectbox(
    "Pontos de entrega",
    ["Aleatórios", "att48 (TSPLIB)"]
)

# Se aleatório, permite escolher o número de pontos; se att48, fixa em 48
if dataset_option == "Aleatórios":
    num_cities = st.sidebar.slider("Nº de pontos", 5, 50, 20, key="num_cities_slider")
else:
    st.sidebar.caption("48 pontos fixos — benchmark TSPLIB")
    num_cities = 48

# Parâmetros do algoritmo genético
# population: quantas rotas candidatas existem em cada geração
population       = st.sidebar.slider("Tamanho da população", 50, 500, 200)

# mutation: probabilidade de trocar dois pontos aleatoriamente em uma rota
mutation         = st.sidebar.slider("Taxa de mutação", 0.0, 1.0, 0.2)

# generations: quantas rodadas de evolução o algoritmo vai executar
generations      = st.sidebar.slider("Gerações", 10, 300, 100)

# delay: pausa entre frames para controlar a velocidade da animação
delay            = st.sidebar.slider("Delay (s)", 0.0, 0.5, 0.05)

# Método de seleção dos pais para cruzamento:
# tournament: disputa entre grupos, top10: melhores 10%, roulette: probabilidade proporcional
selection_method = st.sidebar.selectbox("Seleção", ["tournament", "top10", "roulette"])

# Legenda visual do mapa
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

# Botão que dispara a execução do algoritmo
rodar = st.sidebar.button("▶  INICIAR OTIMIZAÇÃO")


# =============================================================================
# TELA DE BOAS-VINDAS
# Exibida enquanto o algoritmo não foi iniciado
# =============================================================================
if not rodar:
    st.markdown(f"""
    <div style="padding:3rem 2rem; text-align:center;">
        <div style="font-size:3.5rem; margin-bottom:1rem;">🏥</div>
        <div style="color:{TEXT_COLOR}; font-size:1.2rem; font-weight:600; margin-bottom:0.5rem;">
            Pronto para otimizar
        </div>
        <div style="color:{TEXT_MUTED}; font-size:0.82rem; font-weight:300;
                    max-width:480px; margin:0 auto; line-height:1.7;">
            Configure os parâmetros e clique em
            <span style="color:{GREEN}; font-weight:600;">Iniciar Otimização</span>
            para encontrar a rota mais eficiente de entrega de medicamentos.
        </div>
        <div style="display:flex; justify-content:center; gap:1.5rem;
                    margin-top:2.5rem; flex-wrap:wrap;">
            <div style="background:{CARD_COLOR}; border:1px solid {BORDER_COLOR};
                        border-radius:12px; padding:1.2rem 1.5rem; text-align:center; min-width:160px;">
                <div style="font-size:1.6rem;">🧬</div>
                <div style="color:{GREEN}; font-size:0.65rem; font-weight:600;
                            letter-spacing:0.08em; margin-top:0.4rem;">ALGORITMO GENÉTICO</div>
                <div style="color:{TEXT_MUTED}; font-size:0.68rem; margin-top:0.3rem;">
                    Seleção · Cruzamento · Mutação
                </div>
            </div>
            <div style="background:{CARD_COLOR}; border:1px solid {BORDER_COLOR};
                        border-radius:12px; padding:1.2rem 1.5rem; text-align:center; min-width:160px;">
                <div style="font-size:1.6rem;">🗺️</div>
                <div style="color:{BLUE}; font-size:0.65rem; font-weight:600;
                            letter-spacing:0.08em; margin-top:0.4rem;">PROBLEMA DO CAIXEIRO</div>
                <div style="color:{TEXT_MUTED}; font-size:0.68rem; margin-top:0.3rem;">
                    Minimização de distância total
                </div>
            </div>
            <div style="background:{CARD_COLOR}; border:1px solid {BORDER_COLOR};
                        border-radius:12px; padding:1.2rem 1.5rem; text-align:center; min-width:160px;">
                <div style="font-size:1.6rem;">🤖</div>
                <div style="color:{AMBER}; font-size:0.65rem; font-weight:600;
                            letter-spacing:0.08em; margin-top:0.4rem;">ANÁLISE COM LLM</div>
                <div style="color:{TEXT_MUTED}; font-size:0.68rem; margin-top:0.3rem;">
                    Interpretação dos resultados
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# EXECUÇÃO DO ALGORITMO GENÉTICO
# Bloco principal: roda quando o botão "Iniciar Otimização" é clicado
# =============================================================================
if rodar:

    # --- Carrega os pontos de entrega conforme o dataset escolhido ---
    if dataset_option == "Aleatórios":
        # Gera coordenadas (x, y) aleatórias para num_cities pontos
        cities = generate_cities(num_cities)
        # Usa distância euclidiana simples
        distance_function = calculate_distance
    else:
        # Carrega as 48 cidades do benchmark TSPLIB att48
        cities = load_att48()
        # Usa a fórmula de distância pseudo-euclidiana do benchmark att48
        distance_function = calculate_distance_att

    # --- Executa o algoritmo genético ---
    # Retorna três listas, uma entrada por geração:
    #   history      → distância da melhor rota em cada geração
    #   best_routes  → índices dos pontos na melhor rota de cada geração
    #   populations  → todas as rotas da população em cada geração
    history, best_routes, populations = run_ga_visual(
        cities, population, mutation, 3,
        generations, selection_method, distance_function
    )

    # --- Layout: mapa à esquerda (60%), gráficos à direita (40%) ---
    st.markdown(f"<div style='padding:0.6rem 1.5rem 0 1.5rem;'>", unsafe_allow_html=True)
    col1, col2 = st.columns([6, 4], vertical_alignment="top")
    st.markdown("</div>", unsafe_allow_html=True)

    # Placeholders permitem atualizar os gráficos a cada geração sem recriar a página
    route_placeholder  = col1.empty()   # mapa da rota
    status_placeholder = col1.empty()   # barra de progresso
    fit_placeholder    = col2.empty()   # gráfico de convergência
    hist_placeholder   = col2.empty()   # histograma da população

    # --- Calcula limites do mapa com padding para evitar pontos nas bordas ---
    x_vals, y_vals = zip(*cities)
    padding_x = (max(x_vals) - min(x_vals)) * 0.08 + 5
    padding_y = (max(y_vals) - min(y_vals)) * 0.08 + 5
    x_min, x_max = min(x_vals) - padding_x, max(x_vals) + padding_x
    y_min, y_max = min(y_vals) - padding_y, max(y_vals) + padding_y

    start_time    = time.time()
    distancia_ini = history[0]   # distância da primeira rota (sem otimização)

    # ==========================================================================
    # LOOP DE ANIMAÇÃO — atualiza os gráficos a cada geração
    # ==========================================================================
    for gen in range(len(history)):

        elapsed = time.time() - start_time
        pct = (gen + 1) / len(history) * 100   # percentual de progresso

        # ----------------------------------------------------------------------
        # MAPA DA ROTA
        # Desenha todas as rotas da população (suaves) + melhor rota (destacada)
        # ----------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(5.5, 3.0))
        fig.patch.set_facecolor(PANEL_COLOR)

        # Desenha as rotas alternativas da população em azul escuro e transparente
        # Mostram a "nuvem" de soluções que o algoritmo está explorando
        for route in populations[gen]:
            rc = [cities[i] for i in route] + [cities[route[0]]]
            rx, ry = zip(*rc)
            ax.plot(rx, ry, color=POP_CLR, linewidth=0.3, zorder=1, alpha=0.18)

        # Desenha a melhor rota da geração com gradiente verde→teal e setas
        best_rc = [cities[i] for i in best_routes[gen]] + [cities[best_routes[gen][0]]]
        bx, by  = list(zip(*best_rc))
        n_seg   = len(bx) - 1

        # Cria um colormap de verde para teal para colorir os segmentos progressivamente
        cmap_route = mpl.colors.LinearSegmentedColormap.from_list("rota", [GREEN, TEAL])

        for si in range(n_seg):
            t   = si / max(n_seg - 1, 1)   # posição normalizada (0 a 1) no percurso
            cor = cmap_route(t)             # cor do segmento baseada na posição
            sx, sy = [bx[si], bx[si+1]], [by[si], by[si+1]]

            # Efeito glow: três camadas com opacidade crescente
            ax.plot(sx, sy, color=cor, linewidth=6,   zorder=2, alpha=0.04)
            ax.plot(sx, sy, color=cor, linewidth=3,   zorder=2, alpha=0.08)
            ax.plot(sx, sy, color=cor, linewidth=1.6, zorder=3, alpha=0.9)

            # Seta de direção no meio do segmento para indicar sentido do percurso
            mx, my = (bx[si] + bx[si+1]) / 2, (by[si] + by[si+1]) / 2
            dx, dy = bx[si+1] - bx[si], by[si+1] - by[si]
            ax.annotate("", xy=(mx + dx*0.01, my + dy*0.01),
                        xytext=(mx - dx*0.01, my - dy*0.01),
                        arrowprops=dict(arrowstyle="-|>", color=cor,
                                        lw=1.2, mutation_scale=8),
                        zorder=4)

        # O primeiro ponto da melhor rota é o depósito central
        depot_idx = best_routes[gen][0]

        # Desenha os pontos de entrega (exceto o depósito)
        for idx, (cx, cy) in enumerate(cities):
            if idx == depot_idx:
                continue   # o depósito é desenhado separadamente

            # Círculo rosa com fundo escuro
            ax.scatter(cx, cy, s=60, marker="o",
                       facecolor="#1a2f4a", edgecolor="#e05b8b",
                       linewidth=1.2, zorder=5)

            # Cruz de hospital no centro do círculo
            ax.annotate("+", (cx, cy), fontsize=8, color="#e05b8b",
                        ha="center", va="center", fontweight="bold", zorder=6)

            # Número do ponto — exibido apenas no frame final para não poluir a animação
            if gen == len(history) - 1:
                offset = (y_max - y_min) * 0.04   # deslocamento proporcional ao tamanho do mapa
                ax.text(cx, cy + offset, str(idx),
                        fontsize=6, color=TEXT_COLOR,
                        ha="center", va="bottom", zorder=8)

        # Desenha o depósito central (ponto de partida e chegada da rota)
        depot   = cities[depot_idx]
        depot_r = (x_max - x_min) * 0.025   # raio proporcional ao tamanho do mapa

        # Círculo âmbar com borda branca
        ax.add_patch(plt.Circle(depot, depot_r, color=AMBER, zorder=5, alpha=0.9))
        ax.add_patch(plt.Circle(depot, depot_r, fill=False, edgecolor="white",
                                linewidth=1.5, zorder=6))

        # Cruz vermelha no centro do depósito (símbolo de saúde)
        ax.text(depot[0], depot[1], "+", fontsize=12, color="#cc0000",
                ha="center", va="center", fontweight="bold", zorder=7)

        # Título do gráfico: geração atual e distância da melhor rota
        # Usa dois textos separados para colorir a distância em verde
        label_txt = f"Geração {gen+1} / {len(history)}   ·   Melhor rota: "
        ax.text(0.5, 1.03, label_txt,
                transform=ax.transAxes, ha="right", va="bottom",
                fontsize=10, color=TEXT_MUTED)
        ax.text(0.5, 1.03, f"{history[gen]:.0f}",
                transform=ax.transAxes, ha="left", va="bottom",
                fontsize=10, color=GREEN, fontweight="bold")

        # Estiliza bordas do gráfico
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER_COLOR)
            spine.set_linewidth(1.2)

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.grid(True, alpha=0.3)
        fig.tight_layout(pad=0.6)
        route_placeholder.pyplot(fig, use_container_width=True)
        plt.close(fig)   # libera memória após renderizar

        # ----------------------------------------------------------------------
        # BARRA DE PROGRESSO
        # Mostra tempo decorrido, percentual concluído e barra animada
        # ----------------------------------------------------------------------
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

        # Calcula a distância de todas as rotas da população atual para os gráficos
        distances = [calculate_fitness(r, cities, distance_function) for r in populations[gen]]

        # ----------------------------------------------------------------------
        # GRÁFICO DE CONVERGÊNCIA
        # Mostra como a distância da melhor rota evoluiu ao longo das gerações
        # Uma queda indica que o algoritmo encontrou uma rota melhor
        # ----------------------------------------------------------------------
        fig_fit, ax_fit = plt.subplots(figsize=(5, 2.1))
        xs, ys = list(range(gen + 1)), history[:gen + 1]

        # Linha de evolução com marcadores
        ax_fit.plot(xs, ys, color=TEAL, linewidth=2.2,
                    marker="o", markersize=3.5,
                    markerfacecolor=AMBER, markeredgecolor=BG_COLOR,
                    markeredgewidth=0.5, zorder=3)

        # Área preenchida abaixo da linha até o mínimo atual
        ax_fit.fill_between(xs, ys, min(ys), alpha=0.18, color=TEAL, zorder=2)

        # Configura eixos com margem e escala fixa (0 a total de gerações)
        margem = (max(ys) - min(ys)) * 0.25 + 1
        ax_fit.set_ylim(min(ys) - margem, max(ys) + margem)
        ax_fit.set_xlim(0, len(history) - 1)   # eixo X fixo para não "pular" a cada frame

        # Linha tracejada verde no melhor valor encontrado até agora
        ax_fit.axhline(min(ys), color=GREEN, linewidth=1.2, linestyle="--",
                       alpha=0.8, label=f"Mín: {min(ys):.0f}")

        # Destaca gerações onde houve melhoria com um ponto verde
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

        # ----------------------------------------------------------------------
        # HISTOGRAMA DA POPULAÇÃO
        # Mostra a distribuição das distâncias de todas as 'population' rotas
        # À medida que o algoritmo evolui, as barras se concentram à esquerda
        # (rotas mais curtas), indicando convergência da população
        # ----------------------------------------------------------------------
        fig_hist, ax_hist = plt.subplots(figsize=(5, 2.1))
        n, bins, patches = ax_hist.hist(distances, bins=15,
                                        edgecolor=BG_COLOR, linewidth=0.4, alpha=0.92)

        # Colore as barras com gradiente verde (boas) → vermelho (ruins)
        cmap = mpl.cm.get_cmap("RdYlGn_r")
        norm = mpl.colors.Normalize(vmin=0, vmax=len(patches) - 1)
        for i, patch in enumerate(patches):
            patch.set_facecolor(cmap(norm(i)))

        # Linha tracejada verde na melhor distância atual
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

        # Pausa entre frames para controlar a velocidade da animação
        time.sleep(delay)


    # ==========================================================================
    # RESULTADO FINAL
    # Exibido após o término de todas as gerações
    # ==========================================================================

    # Calcula métricas finais
    best_found  = round(history[-1], 2)
    melhoria    = ((distancia_ini - best_found) / distancia_ini) * 100
    tempo_total = round(time.time() - start_time, 1)
    dist_media  = round(best_found / len(cities), 2)
    economia    = round(distancia_ini - best_found)

    # Encontra a primeira geração que atingiu a melhor distância final
    # Indica quando o algoritmo parou de melhorar
    min_val = min(history)
    gen_convergiu = next(i + 1 for i, v in enumerate(history) if v == min_val)

    st.markdown(f"""
    <div style="padding:0.8rem 1.5rem 0.4rem 1.5rem;">
        <div style="color:{GREEN}; font-size:0.65rem; font-weight:600;
                    letter-spacing:0.12em; text-transform:uppercase;">
            ✅ Otimização concluída
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Cards de métricas em 5 colunas
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Rota sem otimização", f"{distancia_ini:.0f}",
                  help="Distância da primeira rota gerada aleatoriamente")
    with c2:
        # delta_color="inverse" faz o delta negativo aparecer em verde (redução = bom)
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

    # --------------------------------------------------------------------------
    # SEQUÊNCIA DE ENTREGAS
    # Mostra a ordem exata de visita aos pontos na melhor rota encontrada
    # Formato: 📍 Depósito → #3 → #7 → ... → 🏁 Depósito
    # --------------------------------------------------------------------------
    best_final = best_routes[-1]                          # melhor rota da última geração
    paradas    = list(best_final) + [best_final[0]]       # adiciona retorno ao depósito
    n_paradas  = len(best_final) - 1                      # total de pontos de entrega

    # Monta a string da sequência com setas entre cada parada
    itens = []
    for i, idx in enumerate(paradas):
        if i == 0:
            itens.append(f"📍 Depósito #{idx}")          # ponto de partida
        elif i == len(paradas) - 1:
            itens.append(f"🏁 Depósito #{idx}")          # retorno ao depósito
        else:
            itens.append(f"#{idx}")                       # ponto de entrega intermediário
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

    # Exibe comparação com o ótimo conhecido apenas para o benchmark att48
    # O ótimo conhecido (10628) é a melhor solução documentada para esse problema
    if dataset_option == "att48 (TSPLIB)":
        best_known = 10628
        error = ((best_found - best_known) / best_known) * 100
        st.markdown(f"""
<div style="margin:0.4rem 0 0 0; color:#7a9bb5; font-size:0.75rem;">
    📌 <b>Benchmark att48</b> — Ótimo conhecido: <b style="color:#e8f4f8">{best_known}</b> · Erro: <b style="color:#f59e0b">{error:.2f}%</b>
</div>
""", unsafe_allow_html=True)
