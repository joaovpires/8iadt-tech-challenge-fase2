import folium
from folium.plugins import DualMap

from src.data.models import DeliveryPoint, Route, OptimizationResult
from src.data.distances import build_distance_matrix, route_total_distance

PRIORITY_COLORS = {
    "critica": "red",
    "alta": "orange",
    "media": "blue",
    "baixa": "green",
    "base": "black",
}

ROUTE_COLORS = ["#e74c3c", "#2980b9", "#27ae60", "#8e44ad", "#f39c12", "#1abc9c"]


def create_comparison_map(
    result: OptimizationResult,
    points: list[DeliveryPoint],
    output_path: str = "output/comparison_map.html",
) -> DualMap:
    base = points[0]

    dual_map = DualMap(
        location=[base.latitude, base.longitude],
        zoom_start=12,
        tiles="CartoDB positron",
    )

    # lado esquerdo: rotas sem otimização (ordem original dos pontos)
    _add_base_marker(dual_map.m1, base, "ANTES — Rota Inicial")
    _add_delivery_markers(dual_map.m1, points)

    initial_routes = _build_initial_routes(result, points)
    total_initial = 0.0
    for idx, (vehicle_name, coords, dist) in enumerate(initial_routes):
        color = ROUTE_COLORS[idx % len(ROUTE_COLORS)]
        total_initial += dist
        folium.PolyLine(
            locations=coords,
            weight=4,
            color=color,
            opacity=0.6,
            dash_array="10",
            popup=f"<b>{vehicle_name}</b><br>Distância: {dist:.2f} km<br><i>Sem otimização</i>",
        ).add_to(dual_map.m1)

    _add_total_label(dual_map.m1, total_initial, "SEM OTIMIZAÇÃO", "#e74c3c")

    # lado direito: rotas otimizadas pelo AG
    _add_base_marker(dual_map.m2, base, "DEPOIS — Rota Otimizada")
    _add_delivery_markers(dual_map.m2, points)

    total_optimized = 0.0
    for idx, route in enumerate(result.routes):
        color = ROUTE_COLORS[idx % len(ROUTE_COLORS)]
        total_optimized += route.total_distance

        coords = [[base.latitude, base.longitude]]
        for stop in route.stops:
            coords.append([stop.latitude, stop.longitude])
        coords.append([base.latitude, base.longitude])

        folium.PolyLine(
            locations=coords,
            weight=4,
            color=color,
            opacity=0.8,
            popup=(
                f"<b>{route.vehicle.name}</b><br>"
                f"Distância: {route.total_distance:.2f} km<br>"
                f"Carga: {route.total_load:.1f}/{route.vehicle.capacity} kg<br>"
                f"<i>Otimizado por AG</i>"
            ),
        ).add_to(dual_map.m2)

        for order, stop in enumerate(route.stops, start=1):
            folium.CircleMarker(
                location=[stop.latitude, stop.longitude],
                radius=10,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.9,
                popup=f"Parada #{order} - {stop.name}",
            ).add_to(dual_map.m2)

    _add_total_label(dual_map.m2, total_optimized, "OTIMIZADO (AG)", "#27ae60")

    # Salvar
    dual_map.save(output_path)
    print(f"Mapa comparativo salvo em: {output_path}")
    return dual_map


def _add_base_marker(map_obj, base: DeliveryPoint, title: str):
    folium.Marker(
        location=[base.latitude, base.longitude],
        popup=f"<b>{base.name}</b><br>{title}",
        icon=folium.Icon(color="black", icon="plus-sign"),
    ).add_to(map_obj)


def _add_delivery_markers(map_obj, points: list[DeliveryPoint]):
    for p in points[1:]:
        color = PRIORITY_COLORS.get(p.priority, "gray")
        folium.Marker(
            location=[p.latitude, p.longitude],
            popup=f"<b>{p.name}</b><br>Prioridade: {p.priority}<br>Demanda: {p.demand} kg",
            icon=folium.Icon(color=color, icon="info-sign"),
        ).add_to(map_obj)


def _build_initial_routes(result: OptimizationResult, points: list[DeliveryPoint]):
    """
    Recria as rotas na ordem original (não-otimizada) para comparação.
    Usa a mesma atribuição de pontos por veículo, mas sem reordenar.
    """
    base = points[0]
    dist_matrix = build_distance_matrix(points)
    initial_routes = []

    for route in result.routes:
        # Pegar os IDs dos pontos e ordená-los pelo ID original (ordem de chegada)
        original_order = sorted(route.sequence)
        coords = [[base.latitude, base.longitude]]
        for idx in original_order:
            coords.append([points[idx].latitude, points[idx].longitude])
        coords.append([base.latitude, base.longitude])

        dist = route_total_distance(original_order, dist_matrix)
        initial_routes.append((route.vehicle.name, coords, dist))

    return initial_routes


def _add_total_label(map_obj, total_dist: float, label: str, color: str):
    html = f"""
    <div style="position:fixed;top:15px;left:50%;transform:translateX(-50%);
        z-index:1000;background:white;padding:10px 18px;border-radius:8px;
        box-shadow:0 2px 8px rgba(0,0,0,0.2);font-size:14px;text-align:center;
        border-left:5px solid {color};">
        <b>{label}</b><br>
        Distância total: <b style="color:{color};">{total_dist:.2f} km</b>
    </div>
    """
    map_obj.get_root().html.add_child(folium.Element(html))
