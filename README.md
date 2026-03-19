# Otimização de Rotas para Distribuição de Medicamentos Hospitalares

**Tech Challenge — Fase 2 | Pós-graduação 8IADT — FIAP**

Sistema que utiliza **Algoritmo Genético** para otimizar rotas de veículos na distribuição de medicamentos e insumos hospitalares na região de São Paulo, resolvendo o problema conhecido como VRP (Vehicle Routing Problem).

## Equipe

| Membro  | Responsabilidade |
|---------|-----------------|
| Karina  | Algoritmo Genético (seleção, crossover, mutação) |
| Bruna   | Modelagem de dados e base de pontos de entrega |
| Matheus | Visualização, script principal, integração e testes e2e |
| João    | Infraestrutura e documentação |

## Resultados

Com dados de teste (15 pontos de entrega, 3 veículos):

| Métrica | Valor |
|---------|-------|
| Distância inicial (sem otimização) | 150.37 km |
| Distância otimizada (AG) | 110.65 km |
| **Melhoria** | **26.4%** |

## Estrutura do Projeto

```
tech-challenge-fase2/
├── main.py                          # Script principal de execução
├── requirements.txt                 # Dependências Python
├── src/
│   ├── data/
│   │   ├── models.py                # Dataclasses (DeliveryPoint, Vehicle, Route...)
│   │   ├── mock_data.py             # Dados de teste (São Paulo)
│   │   └── distances.py             # Haversine e matriz de distâncias
│   ├── genetic_algorithm/
│   │   └── ga_mock.py               # AG simplificado (placeholder)
│   └── visualization/
│       ├── route_map.py             # Mapa interativo (Folium)
│       ├── comparison_map.py        # Mapa comparativo antes vs depois
│       └── charts.py                # Gráficos (convergência, carga, distâncias)
├── tests/
│   └── test_pipeline.py             # 17 testes (distâncias, AG, e2e, visualização)
└── output/                          # Arquivos gerados pela execução
    ├── route_map.html
    ├── comparison_map.html
    ├── convergence.png
    ├── distance_comparison.png
    ├── vehicle_load.png
    ├── route_distances.png
    └── result.json
```

## Como Executar

### Pré-requisitos

- Python 3.10+

### Instalação

```bash
pip install -r requirements.txt
```

### Execução

```bash
python main.py
```

Os resultados serão gerados na pasta `output/`.

#### Parâmetros opcionais

```bash
python main.py --pop-size 100 --generations 200 --mutation-rate 0.15 --seed 42 --output-dir output
```

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `--pop-size` | 50 | Tamanho da população do AG |
| `--generations` | 100 | Número de gerações |
| `--mutation-rate` | 0.1 | Taxa de mutação (0 a 1) |
| `--seed` | 42 | Seed para reprodutibilidade |
| `--output-dir` | output | Diretório de saída |

### Testes

```bash
python -m pytest tests/ -v
```

## Tecnologias

- **Python 3.12** — linguagem principal
- **Folium** — mapas interativos (Leaflet.js)
- **Matplotlib** — gráficos estáticos
- **Pytest** — framework de testes
- **Haversine** — cálculo de distância real entre coordenadas

## Saídas Geradas

| Arquivo | Descrição |
|---------|-----------|
| `route_map.html` | Mapa interativo com rotas otimizadas, marcadores coloridos por prioridade |
| `comparison_map.html` | Mapa lado a lado: rotas antes vs depois da otimização |
| `convergence.png` | Curva de convergência do fitness ao longo das gerações |
| `distance_comparison.png` | Gráfico de barras comparando distância inicial vs otimizada |
| `vehicle_load.png` | Carga utilizada vs capacidade de cada veículo |
| `route_distances.png` | Distância percorrida vs autonomia de cada veículo |
| `result.json` | Resultado completo em formato JSON |
