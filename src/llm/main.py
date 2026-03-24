"""
Integração com LLM para geração de instruções, relatórios e Q&A sobre rotas.

Suporta dois modos:
  - OpenAI (GPT-4o / GPT-3.5-turbo): defina a variável de ambiente OPENAI_API_KEY.
  - Fallback de template: quando a chave não está configurada, gera textos
    estruturados sem depender de API externa — útil para demonstração offline.

Funções principais:
  generate_driver_instructions(result, points) → texto com roteiro completo
  generate_route_report(result, experiment_results) → relatório executivo
  ask_question(question, result, points) → resposta em linguagem natural
"""
import os
import json
from datetime import date

from src.data.models import OptimizationResult, DeliveryPoint


# ---------------------------------------------------------------------------
# Cliente LLM — usa OpenAI se disponível, senão fallback de template
# ---------------------------------------------------------------------------

def _has_openai() -> bool:
    try:
        import openai  # noqa: F401
        return bool(os.getenv("OPENAI_API_KEY"))
    except ImportError:
        return False


def _call_openai(system: str, user: str, model: str = "gpt-4o-mini") -> str:
    import openai
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.4,
        max_tokens=1200,
    )
    return response.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# Helpers para montar o contexto das rotas em texto
# ---------------------------------------------------------------------------

PRIORITY_LABEL = {"critica": "CRÍTICA ⚠️", "alta": "Alta", "media": "Média", "baixa": "Baixa", "base": "Base"}


def _routes_to_text(result: OptimizationResult, points: list[DeliveryPoint]) -> str:
    base = points[0] if points else None
    lines = [f"Base de partida: {base.name}"] if base else []
    for r in result.routes:
        if not r.stops:
            lines.append(f"\n{r.vehicle.name}: sem paradas")
            continue
        lines.append(f"\n{r.vehicle.name} (cap. {r.vehicle.capacity} kg / autonomia {r.vehicle.max_distance} km):")
        lines.append(f"  Distância total: {r.total_distance:.2f} km")
        lines.append(f"  Carga total: {r.total_load:.1f} kg")
        lines.append("  Sequência de entregas:")
        for i, stop in enumerate(r.stops, 1):
            priority = PRIORITY_LABEL.get(stop.priority, stop.priority)
            lines.append(f"    {i}. {stop.name} — {stop.demand} kg — Prioridade: {priority}")
    return "\n".join(lines)


def _improvement_text(result: OptimizationResult) -> str:
    if result.initial_distance > 0:
        pct = (1 - result.optimized_distance / result.initial_distance) * 100
        return f"{pct:.1f}%"
    return "N/A"


# ---------------------------------------------------------------------------
# 1. Instruções para motoristas
# ---------------------------------------------------------------------------

SYSTEM_DRIVER = (
    "Você é um assistente logístico hospitalar. "
    "Gere instruções claras, objetivas e seguras para motoristas de entrega de medicamentos. "
    "Use linguagem simples. Inclua alertas para entregas críticas. "
    "O texto deve ser prático e direto ao ponto."
)


def _driver_instructions_template(result: OptimizationResult, points: list[DeliveryPoint]) -> str:
    today = date.today().strftime("%d/%m/%Y")
    base = points[0].name
    lines = [
        f"ROTEIRO DE ENTREGA — {today}",
        f"Base: {base}",
        "=" * 50,
    ]
    for r in result.routes:
        lines.append(f"\n{r.vehicle.name.upper()}")
        lines.append(f"Distância estimada: {r.total_distance:.2f} km | Carga: {r.total_load:.1f}/{r.vehicle.capacity:.0f} kg")
        if not r.stops:
            lines.append("  → Sem entregas atribuídas nesta saída.")
            continue
        lines.append("Ordem de entrega:")
        for i, stop in enumerate(r.stops, 1):
            alert = " *** PRIORIDADE CRÍTICA — entregue imediatamente ***" if stop.priority == "critica" else ""
            lines.append(f"  {i}. {stop.name} ({stop.demand:.1f} kg){alert}")
        lines.append(f"  → Retornar para {base} ao final.")
    lines += [
        "\nCUIDADOS GERAIS:",
        "  • Verifique a carga e documentação antes de partir.",
        "  • Mantenha medicamentos críticos em área de fácil acesso.",
        "  • Em caso de problema, contate a central imediatamente.",
    ]
    return "\n".join(lines)


def generate_driver_instructions(result: OptimizationResult, points: list[DeliveryPoint]) -> str:
    routes_ctx = _routes_to_text(result, points)
    user_prompt = (
        f"Gere um roteiro detalhado de entrega para os motoristas com base nas rotas abaixo.\n\n"
        f"{routes_ctx}\n\n"
        f"Inclua: ordem de visita, alertas para entregas críticas, cuidados com carga e "
        f"instruções de retorno à base."
    )
    if _has_openai():
        return _call_openai(SYSTEM_DRIVER, user_prompt)
    return _driver_instructions_template(result, points)


# ---------------------------------------------------------------------------
# 2. Relatório executivo de eficiência
# ---------------------------------------------------------------------------

SYSTEM_REPORT = (
    "Você é um analista de logística hospitalar. "
    "Gere relatórios executivos concisos com insights acionáveis para gestores. "
    "Use dados concretos, aponte pontos de atenção e sugira melhorias."
)


def _report_template(result: OptimizationResult, experiment_results: list[dict] | None = None) -> str:
    today = date.today().strftime("%d/%m/%Y")
    improvement = _improvement_text(result)
    lines = [
        f"RELATÓRIO DE EFICIÊNCIA LOGÍSTICA — {today}",
        "=" * 50,
        "",
        "RESUMO EXECUTIVO",
        f"  Distância inicial (sem otimização): {result.initial_distance:.2f} km",
        f"  Distância após otimização (AG):     {result.optimized_distance:.2f} km",
        f"  Redução obtida:                     {improvement}",
        f"  Veículos utilizados: {len([r for r in result.routes if r.stops])} / {len(result.routes)}",
        "",
        "DESEMPENHO POR VEÍCULO",
    ]
    for r in result.routes:
        util_load = (r.total_load / r.vehicle.capacity * 100) if r.vehicle.capacity > 0 else 0
        util_dist = (r.total_distance / r.vehicle.max_distance * 100) if r.vehicle.max_distance > 0 else 0
        lines.append(
            f"  {r.vehicle.name}: {len(r.stops)} paradas | "
            f"{r.total_distance:.2f} km ({util_dist:.0f}% autonomia) | "
            f"{r.total_load:.1f} kg ({util_load:.0f}% capacidade)"
        )

    if experiment_results:
        lines += ["", "COMPARATIVO DE EXPERIMENTOS AG"]
        best = min(experiment_results, key=lambda e: e["metrics"]["optimized_distance_km"])
        for e in experiment_results:
            marker = " ← MELHOR" if e["id"] == best["id"] else ""
            lines.append(
                f"  Exp {e['id']}: pop={e['config']['population_size']}, "
                f"mut={e['config']['mutation_rate']}, {e['config']['selection_type']} "
                f"→ {e['metrics']['improvement_pct']:.1f}% melhoria{marker}"
            )

    lines += [
        "",
        "SUGESTÕES DE MELHORIA",
        "  • Avaliar janelas de tempo para entregas críticas.",
        "  • Monitorar utilização de carga — veículos subutilizados podem ser consolidados.",
        "  • Aumentar gerações do AG se a convergência ocorrer nas primeiras iterações.",
    ]
    return "\n".join(lines)


def generate_route_report(
    result: OptimizationResult,
    experiment_results: list[dict] | None = None,
) -> str:
    routes_ctx = _routes_to_text(result, [])  # sem base aqui para simplificar
    improvement = _improvement_text(result)

    exp_ctx = ""
    if experiment_results:
        exp_ctx = "\n\nRESULTADOS DOS EXPERIMENTOS AG:\n" + json.dumps(
            [{
                "id": e["id"], "name": e["name"],
                "improvement_pct": e["metrics"]["improvement_pct"],
                "config": e["config"],
            } for e in experiment_results],
            ensure_ascii=False, indent=2
        )

    user_prompt = (
        f"Gere um relatório executivo de eficiência logística para o gestor hospitalar.\n\n"
        f"MÉTRICAS GERAIS:\n"
        f"  - Distância inicial: {result.initial_distance:.2f} km\n"
        f"  - Distância otimizada: {result.optimized_distance:.2f} km\n"
        f"  - Melhoria: {improvement}\n\n"
        f"ROTAS:\n{routes_ctx}{exp_ctx}\n\n"
        f"Inclua: resumo executivo, análise de eficiência por veículo, "
        f"comparativo de experimentos (se disponível) e sugestões de melhoria."
    )
    if _has_openai():
        return _call_openai(SYSTEM_REPORT, user_prompt)
    return _report_template(result, experiment_results)


# ---------------------------------------------------------------------------
# 3. Q&A — responde perguntas sobre rotas em linguagem natural
# ---------------------------------------------------------------------------

SYSTEM_QA = (
    "Você é um assistente especialista em logística hospitalar. "
    "Responda perguntas sobre rotas de entrega de medicamentos de forma clara e objetiva. "
    "Use apenas as informações fornecidas no contexto. "
    "Se a informação não estiver disponível, diga isso claramente."
)


def _qa_template(question: str, result: OptimizationResult, points: list[DeliveryPoint]) -> str:
    q = question.lower()
    if "quantos" in q and "ponto" in q or "quantas" in q and "entrega" in q:
        total = sum(len(r.stops) for r in result.routes)
        return f"Há {total} pontos de entrega distribuídos entre {len(result.routes)} veículos."
    if "distância" in q or "km" in q:
        return (f"A distância total otimizada é {result.optimized_distance:.2f} km. "
                f"Antes da otimização era {result.initial_distance:.2f} km "
                f"({_improvement_text(result)} de redução).")
    if "críti" in q or "prioridade" in q:
        criticos = [s.name for r in result.routes for s in r.stops if s.priority == "critica"]
        if criticos:
            return f"Pontos com entrega crítica: {', '.join(criticos)}."
        return "Não há pontos com prioridade crítica nesta rota."
    if "veículo" in q or "van" in q or "carro" in q:
        resp = []
        for r in result.routes:
            stops = ", ".join(s.name for s in r.stops) if r.stops else "nenhuma parada"
            resp.append(f"{r.vehicle.name}: {stops} ({r.total_distance:.2f} km)")
        return "\n".join(resp)
    # Resposta genérica
    routes_ctx = _routes_to_text(result, points)
    return (f"Com base nas rotas otimizadas:\n{routes_ctx}\n\n"
            f"Para '{question}', consulte os detalhes acima.")


def ask_question(
    question: str,
    result: OptimizationResult,
    points: list[DeliveryPoint],
) -> str:
    routes_ctx = _routes_to_text(result, points)
    user_prompt = (
        f"Contexto das rotas otimizadas:\n{routes_ctx}\n\n"
        f"Pergunta: {question}"
    )
    if _has_openai():
        return _call_openai(SYSTEM_QA, user_prompt)
    return _qa_template(question, result, points)


# ---------------------------------------------------------------------------
# CLI simples para demonstração
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from src.data.mock_data import DELIVERY_POINTS, VEHICLES
    from src.data.distances import build_distance_matrix
    from src.genetic_algorithm.ga_adapter import run_genetic_algorithm

    build_distance_matrix(DELIVERY_POINTS)
    result = run_genetic_algorithm(
        points=DELIVERY_POINTS, vehicles=VEHICLES,
        population_size=50, generations=50,
    )

    print("\n" + "=" * 60)
    print("INSTRUÇÕES PARA MOTORISTAS")
    print("=" * 60)
    print(generate_driver_instructions(result, DELIVERY_POINTS))

    print("\n" + "=" * 60)
    print("RELATÓRIO EXECUTIVO")
    print("=" * 60)
    print(generate_route_report(result))

    print("\n" + "=" * 60)
    print("Q&A — PERGUNTAS SOBRE AS ROTAS")
    print("=" * 60)
    questions = [
        "Quais são os pontos com entrega crítica?",
        "Qual a distância total otimizada?",
        "Como estão distribuídas as entregas por veículo?",
    ]
    for q in questions:
        print(f"\nPergunta: {q}")
        print(f"Resposta: {ask_question(q, result, DELIVERY_POINTS)}")

