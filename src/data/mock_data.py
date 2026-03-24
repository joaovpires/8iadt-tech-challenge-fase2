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
    DeliveryPoint(0,  "Hospital Universitário - Base", -23.5614, -46.6558, "base",     0.0),
    DeliveryPoint(1,  "UBS Vila Mariana",               -23.5895, -46.6388, "critica", 10.0),
    DeliveryPoint(2,  "UPA Mooca",                      -23.5585, -46.6008, "alta",    15.0),
    DeliveryPoint(3,  "Hospital São Paulo",             -23.5985, -46.6427, "critica", 12.0),
    DeliveryPoint(4,  "UBS Pinheiros",                  -23.5614, -46.6930, "media",    8.0),
    DeliveryPoint(5,  "Clínica Itaim",                  -23.5863, -46.6756, "alta",     7.0),
    DeliveryPoint(6,  "UPA Lapa",                       -23.5225, -46.6917, "critica", 20.0),
    DeliveryPoint(7,  "Hospital das Clínicas",          -23.5573, -46.6706, "critica", 18.0),
    DeliveryPoint(8,  "UBS Santana",                    -23.4986, -46.6266, "media",    6.0),
    DeliveryPoint(9,  "Hospital Albert Einstein",       -23.5988, -46.7199, "alta",     9.0),
    DeliveryPoint(10, "UPA Tatuapé",                    -23.5421, -46.5722, "alta",    11.0),
]

# ---------------------------------------------------------------------------
# Veículos — capacidades ajustadas para demanda total de 116 kg (10 pontos).
# ---------------------------------------------------------------------------
VEHICLES = [
    Vehicle(1, "Van Medicamentos A", capacity=65.0, max_distance=180.0),
    Vehicle(2, "Van Medicamentos B", capacity=65.0, max_distance=200.0),
]
