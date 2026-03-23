import folium
from folium.plugins import AntPath, Fullscreen, MiniMap, MousePosition

from src.data.models import DeliveryPoint, Route, OptimizationResult

PRIORITY_COLORS = {
    "critica": "red",
    "alta": "orange",
    "media": "blue",
    "baixa": "green",
    "base": "black",
}

ROUTE_COLORS = ["#e74c3c", "#2980b9", "#27ae60", "#8e44ad", "#f39c12", "#1abc9c"]


def create_route_map(result: OptimizationResult, points: list[DeliveryPoint], output_path: str = "output/route_map.html") -> folium.Map:
    base = points[0]
    route_map = folium.Map(
        location=[base.latitude, base.longitude],
        zoom_start=12,
        tiles="CartoDB positron",
    )

    folium.Marker(
        location=[base.latitude, base.longitude],
        popup=f"<b>{base.name}</b><br>DEPÓSITO",
        icon=folium.Icon(color="black", icon="plus-sign"),
    ).add_to(route_map)

    for p in points[1:]:
        color = PRIORITY_COLORS.get(p.priority, "gray")
        folium.Marker(
            location=[p.latitude, p.longitude],
            popup=(
                f"<b>{p.name}</b><br>"
                f"Prioridade: {p.priority}<br>"
                f"Demanda: {p.demand} kg"
            ),
            icon=folium.Icon(color=color, icon="info-sign"),
        ).add_to(route_map)

    for idx, route in enumerate(result.routes):
        color = ROUTE_COLORS[idx % len(ROUTE_COLORS)]

        # cada rota num FeatureGroup pra poder ligar/desligar no LayerControl
        layer = folium.FeatureGroup(name=f"{route.vehicle.name} ({route.total_distance:.1f} km)")

        # base -> paradas -> base
        coords = [[base.latitude, base.longitude]]
        for stop in route.stops:
            coords.append([stop.latitude, stop.longitude])
        coords.append([base.latitude, base.longitude])

        AntPath(
            locations=coords,
            weight=5,
            color=color,
            opacity=0.8,
            delay=800,
            dash_array=[20, 30],
            popup=(
                f"<b>{route.vehicle.name}</b><br>"
                f"Distância: {route.total_distance:.2f} km<br>"
                f"Carga: {route.total_load:.1f}/{route.vehicle.capacity} kg<br>"
                f"Paradas: {len(route.stops)}"
            ),
        ).add_to(layer)

        for order, stop in enumerate(route.stops, start=1):
            folium.CircleMarker(
                location=[stop.latitude, stop.longitude],
                radius=10,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.9,
                popup=f"Parada #{order} - {stop.name}",
            ).add_to(layer)

        layer.add_to(route_map)

    Fullscreen(position="topright").add_to(route_map)
    MiniMap(toggle_display=True, position="bottomright").add_to(route_map)
    MousePosition(position="bottomleft", separator=" | ", prefix="Lat/Lon:").add_to(route_map)
    folium.LayerControl(collapsed=False).add_to(route_map)

    route_map.get_root().html.add_child(folium.Element(_build_legend(result.routes)))
    route_map.save(output_path)
    print(f"Mapa salvo em: {output_path}")
    return route_map


def _build_legend(routes: list[Route]) -> str:
    """Gera HTML da legenda do mapa."""
    items = ""
    for idx, route in enumerate(routes):
        color = ROUTE_COLORS[idx % len(ROUTE_COLORS)]
        items += (
            f'<li><span style="background:{color};width:14px;height:14px;'
            f'display:inline-block;margin-right:6px;border-radius:2px;"></span>'
            f'{route.vehicle.name} — {route.total_distance:.1f} km, '
            f'{route.total_load:.1f} kg</li>'
        )

    return f"""
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
        background:white;padding:12px 16px;border-radius:8px;
        box-shadow:0 2px 8px rgba(0,0,0,0.2);font-size:13px;max-width:320px;">
        <b>Rotas dos Veículos</b>
        <ul style="list-style:none;padding:4px 0;margin:0;">{items}</ul>
        <hr style="margin:6px 0;">
        <b>Prioridades:</b>
        <span style="color:red;">● Crítica</span>
        <span style="color:orange;"> ● Alta</span>
        <span style="color:blue;"> ● Média</span>
        <span style="color:green;"> ● Baixa</span>
    </div>
    """
