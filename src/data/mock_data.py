"""
Dados mock para desenvolvimento e testes.
Simula pontos de entrega em São Paulo e veículos disponíveis.
"""
from src.data.models import DeliveryPoint, Vehicle

# Hospital base (ponto 0 — depósito/origem)
HOSPITAL_BASE = DeliveryPoint(
    id=0,
    name="Hospital Universitário - Base",
    latitude=-23.5614,
    longitude=-46.6558,
    priority="base",
    demand=0.0,
)

# Pontos de entrega simulados em São Paulo
DELIVERY_POINTS = [
    HOSPITAL_BASE,
    DeliveryPoint(1, "UBS Vila Mariana", -23.5895, -46.6388, "critica", 12.0),
    DeliveryPoint(2, "UPA Mooca", -23.5585, -46.6008, "alta", 8.5),
    DeliveryPoint(3, "Hospital São Paulo", -23.5985, -46.6427, "critica", 15.0),
    DeliveryPoint(4, "UBS Pinheiros", -23.5614, -46.6930, "media", 6.0),
    DeliveryPoint(5, "Clínica Itaim", -23.5863, -46.6756, "alta", 10.0),
    DeliveryPoint(6, "UPA Lapa", -23.5225, -46.6917, "media", 7.5),
    DeliveryPoint(7, "Hospital Municipal", -23.5440, -46.6340, "baixa", 5.0),
    DeliveryPoint(8, "UBS Santana", -23.5050, -46.6280, "alta", 9.0),
    DeliveryPoint(9, "Posto Saúde Penha", -23.5310, -46.5430, "media", 4.5),
    DeliveryPoint(10, "UPA Santo Amaro", -23.6540, -46.7100, "critica", 14.0),
    DeliveryPoint(11, "Clínica Tatuapé", -23.5390, -46.5760, "baixa", 3.0),
    DeliveryPoint(12, "UBS Butantã", -23.5720, -46.7310, "media", 6.5),
    DeliveryPoint(13, "Hospital Jabaquara", -23.6310, -46.6390, "alta", 11.0),
    DeliveryPoint(14, "Posto Saúde Ipiranga", -23.5880, -46.6100, "media", 5.5),
    DeliveryPoint(15, "UPA Vila Prudente", -23.5810, -46.5800, "baixa", 4.0),
]

# Veículos disponíveis
VEHICLES = [
    Vehicle(1, "Van Medicamentos A", capacity=50.0, max_distance=80.0),
    Vehicle(2, "Van Medicamentos B", capacity=45.0, max_distance=70.0),
    Vehicle(3, "Carro Insumos C", capacity=30.0, max_distance=60.0),
]
