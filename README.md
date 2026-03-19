# MedRoute — Otimização de Rotas Hospitalares

Projeto desenvolvido para o Tech Challenge Fase 2 da pós-graduação 8IADT (FIAP).

O objetivo é otimizar a distribuição de medicamentos para hospitais e UBSs em São Paulo usando Algoritmo Genético para resolver o VRP (Vehicle Routing Problem). O sistema reduz a distância total percorrida pelos veículos enquanto respeita restrições de capacidade e autonomia.

## Equipe

| Membro  | Responsabilidade |
|---------|-----------------|
| Karina  | Algoritmo Genético (seleção, crossover, mutação) |
| Bruna   | Modelagem de dados e base de pontos de entrega |
| Matheus | Visualização, script principal, integração e testes e2e |
| João    | Infraestrutura e documentação |

## Resultados (dados de teste)

- 15 pontos de entrega, 3 veículos
- Distância inicial: 150.37 km → otimizada: 110.65 km (**-26.4%**)

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

## Como rodar

```bash
pip install -r requirements.txt
python main.py
```

Outputs gerados na pasta `output/`. Parâmetros opcionais: `--pop-size`, `--generations`, `--mutation-rate`, `--seed`, `--output-dir`.

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
