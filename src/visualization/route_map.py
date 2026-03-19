"""
Visualização de rotas otimizadas em mapa interativo com Folium.
Gera um HTML que pode ser aberto no navegador.
"""
import folium

from src.data.models import DeliveryPoint, Route, OptimizationResult

# Cores por prioridade para os marcadores
PRIORITY_COLORS = {
    "critica": "red",
    "alta": "orange",
    "media": "blue",
    "baixa": "green",
    "base": "black",
}

# Cores para as rotas de cada veículo
ROUTE_COLORS = ["#e74c3c", "#2980b9", "#27ae60", "#8e44ad", "#f39c12", "#1abc9c"]


def create_route_map(result: OptimizationResult, points: list[DeliveryPoint], output_path: str = "output/route_map.html") -> folium.Map:
    """
    Cria mapa interativo mostrando as rotas otimizadas.

    Args:
        result: Resultado da otimização com as rotas.
        points: Lista de todos os pontos de entrega.
        output_path: Caminho para salvar o HTML do mapa.

    Returns:
        Objeto folium.Map.
    """
    # Centro do mapa = hospital base
    base = points[0]
    route_map = folium.Map(
        location=[base.latitude, base.longitude],
        zoom_start=12,
        tiles="CartoDB positron",
    )

    # Marcador do hospital base
    folium.Marker(
        location=[base.latitude, base.longitude],
        popup=f"<b>{base.name}</b><br>DEPÓSITO",
        icon=folium.Icon(color="black", icon="plus-sign"),
    ).add_to(route_map)

    # Marcadores de todos os pontos de entrega
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

    # Desenhar as rotas de cada veículo
    for idx, route in enumerate(result.routes):
        color = ROUTE_COLORS[idx % len(ROUTE_COLORS)]

        # Montar coordenadas: base → paradas → base
        coords = [[base.latitude, base.longitude]]
        for stop in route.stops:
            coords.append([stop.latitude, stop.longitude])
        coords.append([base.latitude, base.longitude])

        # Linha da rota
        folium.PolyLine(
            locations=coords,
            weight=4,
            color=color,
            opacity=0.8,
            popup=(
                f"<b>{route.vehicle.name}</b><br>"
                f"Distância: {route.total_distance:.2f} km<br>"
                f"Carga: {route.total_load:.1f}/{route.vehicle.capacity} kg<br>"
                f"Paradas: {len(route.stops)}"
            ),
        ).add_to(route_map)

        # Números nas paradas para indicar ordem
        for order, stop in enumerate(route.stops, start=1):
            folium.CircleMarker(
                location=[stop.latitude, stop.longitude],
                radius=10,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.9,
                popup=f"Parada #{order} - {stop.name}",
            ).add_to(route_map)

    # Legenda
    legend_html = _build_legend(result.routes)
    route_map.get_root().html.add_child(folium.Element(legend_html))

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
