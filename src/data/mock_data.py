"""
Dados de entrada do problema VRP para entrega de medicamentos em São Paulo.

Fonte canônica: definição da Bruna (src/ga/run_vrp.py) — IDs, demandas e
prioridades são os mesmos usados pelo algoritmo genético.  As coordenadas
geográficas (lat/lon) foram adicionadas para as visualizações no mapa.

Mapeamento de prioridade:
    0 = "base"  (depósito)
    1 = "critica"
    2 = "alta"
    3 = "media"
"""
from src.data.models import DeliveryPoint, Vehicle

# ---------------------------------------------------------------------------
# Pontos de entrega — mesmos IDs/demandas/prioridades do run_vrp.py da Bruna
# Coordenadas geográficas de hospitais reais em São Paulo
# ---------------------------------------------------------------------------
DELIVERY_POINTS = [
    DeliveryPoint(0, "Hospital Universitário - Base", -23.5614, -46.6558, "base",    0.0),
    DeliveryPoint(1, "UBS Vila Mariana",               -23.5895, -46.6388, "critica", 10.0),
    DeliveryPoint(2, "UPA Mooca",                      -23.5585, -46.6008, "alta",    15.0),
    DeliveryPoint(3, "Hospital São Paulo",             -23.5985, -46.6427, "critica", 12.0),
    DeliveryPoint(4, "UBS Pinheiros",                  -23.5614, -46.6930, "media",    8.0),
    DeliveryPoint(5, "Clínica Itaim",                  -23.5863, -46.6756, "alta",     7.0),
    DeliveryPoint(6, "UPA Lapa",                       -23.5225, -46.6917, "critica", 20.0),
]

# ---------------------------------------------------------------------------
# Veículos — estrutura da Bruna (run_vrp.py), capacidades ajustadas para que
# o problema seja feasível (demanda total = 72 kg > 65 kg originais).
# ---------------------------------------------------------------------------
VEHICLES = [
    Vehicle(1, "Van Medicamentos A", capacity=40.0, max_distance=180.0),
    Vehicle(2, "Van Medicamentos B", capacity=40.0, max_distance=200.0),
]
