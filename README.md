# MedRoute — Otimização de Rotas Hospitalares

**Tech Challenge Fase 2 · PosTech IA para Devs · Turma 8IADT · FIAP**

Sistema de otimização de rotas para distribuição de medicamentos e insumos entre unidades hospitalares em São Paulo, usando **Algoritmo Genético (VRP)** e **LLMs** para geração de instruções e relatórios.

---

## Equipe

| Membro  | Responsabilidade |
|---------|-----------------|
| Karina  | Algoritmo Genético — operadores de seleção, crossover e mutação |
| Bruna   | Modelagem VRP — fitness, restrições de capacidade/autonomia/prioridade |
| Matheus | Visualização, `main.py`, integração, experimentos, LLM e testes e2e |
| João    | Infraestrutura e documentação |

---

## Resultados

- **6 pontos de entrega**, 2 veículos
- Distância inicial → otimizada: **melhoria média de ~15%** (varia por configuração)
- Melhor configuração: Experimento 2 (pop=80, mut=0.05, tournament)

---

## Arquitetura

```
┌───────────────────────────────────────────────────────────┐
│                        main.py                            │
│         (orquestração, CLI, serialização JSON)            │
└────────────┬───────────────────────────┬──────────────────┘
             │                           │
   ┌─────────▼──────────┐     ┌──────────▼──────────────┐
   │  src/data/         │     │  src/visualization/      │
   │  models.py         │     │  route_map.py  (Folium)  │
   │  mock_data.py      │     │  comparison_map.py       │
   │  distances.py      │     │  charts.py (Matplotlib)  │
   └─────────┬──────────┘     └─────────────────────────-┘
             │
   ┌─────────▼──────────────────────────┐
   │  src/genetic_algorithm/            │
   │  ga_adapter.py  (ponte Matheus↔GA) │
   └─────────┬──────────────────────────┘
             │
   ┌─────────▼──────────────────────────────────────────┐
   │  src/ga/  (código Bruna + Karina)                  │
   │  algorithm_vrp.py   run_ga_vrp()                   │
   │  vrp_sequence_population.py                        │
   │  vrp_adapter.py     evaluate_sequence_solution()   │
   │  vrp_fitness.py     penalidades de capacidade,     │
   │                     prioridade, autonomia          │
   │  crossover.py · mutation.py · selection.py         │
   └────────────────────────────────────────────────────┘
             │
   ┌─────────▼──────────────────────────┐
   │  src/experiments/main.py           │
   │  3 experimentos comparativos       │
   └─────────┬──────────────────────────┘
             │
   ┌─────────▼──────────────────────────┐
   │  src/results/main.py               │
   │  tabela comparativa + gráficos     │
   └─────────┬──────────────────────────┘
             │
   ┌─────────▼──────────────────────────┐
   │  src/llm/main.py                   │
   │  instruções motoristas             │
   │  relatório executivo               │
   │  Q&A em linguagem natural          │
   └────────────────────────────────────┘
```

---

<<<<<<< HEAD
## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.10+

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/otimizacao-rotas-hospitalares.git
cd otimizacao-rotas-hospitalares
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instale as dependências
=======
## Estrutura do Projeto

```
tech-challenge-fase2/
├── main.py                              # Script principal (CLI)
├── requirements.txt
├── src/
│   ├── data/
│   │   ├── models.py                    # DeliveryPoint, Vehicle, Route, OptimizationResult
│   │   ├── mock_data.py                 # Dados canônicos (Bruna) + coordenadas SP
│   │   └── distances.py                # Haversine + matriz de distâncias
│   ├── ga/                              # Algoritmo Genético (Bruna + Karina)
│   │   ├── algorithm_vrp.py             # run_ga_vrp() — loop principal do AG
│   │   ├── vrp_sequence_population.py   # Geração de população por sequência
│   │   ├── vrp_adapter.py               # sequence → cromossomo VRP
│   │   ├── vrp_fitness.py               # Função fitness com penalidades
│   │   ├── vrp_models.py                # Delivery, Vehicle (modelos internos do AG)
│   │   ├── vrp_utils.py                 # Utilitários (haversine, split_routes...)
│   │   ├── crossover.py                 # Order crossover (OX)
│   │   ├── mutation.py                  # Swap mutation
│   │   └── selection.py                 # Tournament / Top-10 / Roulette
│   ├── genetic_algorithm/
│   │   └── ga_adapter.py                # Ponte entre modelos do Matheus e AG da Bruna
│   ├── visualization/
│   │   ├── route_map.py                 # Mapa interativo (Folium + AntPath)
│   │   ├── comparison_map.py            # DualMap antes vs depois
│   │   └── charts.py                    # 4 gráficos Matplotlib
│   ├── experiments/
│   │   └── main.py                      # 3 experimentos com configs diferentes
│   ├── results/
│   │   └── main.py                      # Análise comparativa + gráficos
│   └── llm/
│       └── main.py                      # Instruções, relatórios e Q&A via LLM
├── tests/
│   └── test_pipeline.py                 # 17 testes automatizados
└── output/
    ├── route_map.html
    ├── comparison_map.html
    ├── convergence.png
    ├── distance_comparison.png
    ├── vehicle_load.png
    ├── route_distances.png
    ├── result.json
    └── experiments/
        ├── experiment_1.json
        ├── experiment_2.json
        ├── experiment_3.json
        ├── all_experiments.json
        ├── convergence_comparison.png
        └── improvement_comparison.png
```

---

## Como rodar

### 1. Instalar dependências
>>>>>>> e96952fb869f9558f7af77d5b49ced95eae47bb1

```bash
pip install -r requirements.txt
```

<<<<<<< HEAD
---

## ▶️ Como Rodar

### Interface Web (Streamlit)

```bash
streamlit run src/ga/app.py
```

Acesse `http://localhost:8501` no navegador.

### Execução direta do Algoritmo Genético

```bash
python src/ga/algorithm.py
=======
### 2. Otimização principal (rota + visualizações)

```bash
python main.py
# Parâmetros opcionais:
python main.py --pop-size 80 --generations 100 --mutation-rate 0.05
```

### 3. Rodar os 3 experimentos comparativos

```bash
python -m src.experiments.main
```

### 4. Analisar e comparar resultados

```bash
python -m src.results.main
```

### 5. LLM — instruções, relatório e Q&A

```bash
# Sem chave OpenAI → usa templates estruturados (modo offline)
python -m src.llm.main

# Com OpenAI (GPT-4o-mini):
$env:OPENAI_API_KEY = "sk-..."
python -m src.llm.main
```

### 6. Testes automatizados

```bash
python -m pytest tests/ -v
>>>>>>> e96952fb869f9558f7af77d5b49ced95eae47bb1
```

---

<<<<<<< HEAD
## 🧬 Sobre o Algoritmo Genético

O GA é configurado com os seguintes parâmetros padrão:

| Parâmetro | Valor |
|---|---|
| Tamanho da população | 200 indivíduos |
| Número de gerações | 100 |
| Método de seleção | Tournament Selection |
| Representação | Permutação de hospitais |
| Função de fitness | Distância euclidiana total da rota |

A cada geração, os melhores indivíduos são selecionados via torneio, cruzados para gerar descendentes e submetidos a mutação, preservando a diversidade genética e convergindo para a rota de menor distância.

---

## 🤖 Análise com LLM

Após a execução do algoritmo, os resultados são enviados a um modelo de linguagem que interpreta:

- A qualidade da rota encontrada
- A economia percentual obtida em relação à rota inicial
- Sugestões de ajustes nos parâmetros do GA
- Análise do comportamento da população ao longo das gerações

---

## 📦 Dependências

```
streamlit
matplotlib
```

---

## 🎓 Contexto Acadêmico

Projeto desenvolvido como **Tech Challenge — Fase 2** do curso **IA para Devs** da **PosTech FIAP**, aplicando técnicas de otimização bio-inspirada e inteligência artificial generativa na resolução de problemas reais da área da saúde.
=======
## Restrições do VRP implementadas

| Restrição | Implementação |
|-----------|--------------|
| Capacidade máxima de carga | Penalidade proporcional ao excesso |
| Autonomia máxima do veículo | Penalidade proporcional ao excesso |
| Prioridade de entrega | Penalidade crescente por posição na rota |
| Múltiplos veículos (VRP) | Cromossomo por sequência + divisão por capacidade |
| Clientes faltantes | Penalidade alta (5000×) |
| Clientes duplicados | Penalidade alta (3000×) |

---

## Experimentos AG

| # | Configuração | Melhoria |
|---|-------------|---------|
| 1 | pop=30, mut=0.10, tournament | ~10–15% |
| 2 | pop=80, mut=0.05, tournament | maior precisão |
| 3 | pop=50, mut=0.30, roulette   | maior diversidade |

Resultados completos em `output/experiments/`.

---

## Integração com LLM

A integração LLM (`src/llm/main.py`) oferece três funcionalidades:

1. **Instruções para motoristas** — roteiro completo por veículo com alertas de prioridade crítica
2. **Relatório executivo** — métricas de eficiência, comparativo de experimentos, sugestões
3. **Q&A** — responde perguntas em linguagem natural sobre as rotas otimizadas

Funciona com a API OpenAI (defina `OPENAI_API_KEY`) ou em modo offline com templates estruturados.

---

## Saídas Geradas

| Arquivo | Descrição |
|---------|-----------|
| `route_map.html` | Mapa interativo com AntPath animado, LayerControl, Fullscreen, MiniMap |
| `comparison_map.html` | DualMap antes vs depois da otimização |
| `convergence.png` | Curva de convergência do fitness |
| `distance_comparison.png` | Barras: distância inicial vs otimizada |
| `vehicle_load.png` | Carga utilizada vs capacidade por veículo |
| `route_distances.png` | Distância percorrida vs autonomia por veículo |
| `result.json` | Resultado completo em JSON |
| `experiments/convergence_comparison.png` | Convergência dos 3 experimentos sobrepostos |
| `experiments/improvement_comparison.png` | Melhoria (%) por configuração |

---

## Tecnologias

- **Python 3.12** — linguagem principal
- **Folium 0.20** — mapas interativos (Leaflet.js + plugins AntPath, MiniMap, Fullscreen)
- **Matplotlib 3.10** — gráficos estáticos
- **OpenAI** *(opcional)* — GPT-4o-mini para instruções e relatórios
- **Pytest** — 17 testes automatizados

>>>>>>> e96952fb869f9558f7af77d5b49ced95eae47bb1
