# Roteiro - Demonstração MedRoute v2.0 (15 minutos)

🎬 **Duração Total:** 15 minutos  
🎯 **Público:** Professores/Avaliadores da Tech Challenge  
📝 **Objetivo:** Demonstrar novo layout, visualizações aprimoradas e integração LLM

---

## SEGMENTO 1: Introdução (0:00 - 1:30)

### O que falar:
```
"Olá, sou João Victor. Este é o MedRoute v2.0, um sistema inteligente 
de otimização de rotas para entregas médicas com Algoritmos Genéticos 
e Inteligência Artificial.

Realizamos uma refatoração completa da arquitetura, melhorando a experiência 
de usuário com visualizações aprimoradas. O novo layout integra três 
funcionalidades: otimização, experimentos e relatórios com IA."
```

### O que mostrar:
- [ ] Seu rosto em webcam (20s)
- [ ] Browser com app rodando em localhost:8501 (10s)

### Transição:
"Deixa eu mostrar como funciona..."

---

## SEGMENTO 2: Interface Principal (1:30 - 3:30)

### O que falar:
```
"A interface está organizada em 3 abas principais:
1. Otimização — roda o GA com métricas e visualizações
2. Experimentos — compara 3 configurações
3. LLM / Relatório — gera documentos com IA

Na barra lateral: parâmetros do AG ajustáveis,
pontos de entrega editáveis (demanda, prioridade),
e veículos com capacidade e autonomia."
```

### O que mostrar:
- [ ] Sidebar completo (30s):
  - Sliders: pop_size=80, generations=100, mutation=0.05, seed=42
  - Expander "Pontos de Entrega" (expandir e mostrar)
  - Expander "Veículos" (expandir e mostrar)
  
### Transição:
"Clico em 'Rodar Otimizacao' e vemos os resultados..."

---

## SEGMENTO 3: Aba Otimização (3:30 - 7:30)

### O que mostrar:

#### 3.1 Métricas (30s)
```
Distância Inicial: 450.32 km
Distância Otimizada: 349.85 km (-22.3%)
Gerações executadas: 100
Veículos utilizados: 3
```
Falar: "Redução significativa de ~450 para ~350 km."

#### 3.2 Rotas por Veículo (60s)
Expandir cada uma mostrando paradas com demanda e prioridade.
Falar: "Entregas críticas vêm primeiro (restrição de prioridade)."

#### 3.3 Gráficos (90s)
Mostrar 4 gráficos em grid 2x2:
- **Convergência:** evolução da melhor solução  
- **Comparação:** antes vs depois
- **Carga de Veículos:** balanceamento
- **Distâncias:** distribuição entre rotas

#### 3.4 Mapas Interativos (120s)
Duas abas:
- **Rotas Otimizadas:** mapa com coordenadas reais, diferentes cores
- **Comparativo:** antes (aleatório) vs depois (otimizado)

Falar: "O mapa mostra onde cada pedido vai, cores diferentes para cada veículo."

### Transição:
"Agora vemos a comparação de múltiplas configurações..."

---

## SEGMENTO 4: Aba Experimentos (7:30 - 10:00)

### O que falar:
```
"Testei 3 configurações diferentes para ver qual 
oferece o melhor balanço entre qualidade e velocidade."
```

### O que mostrar:

#### 4.1 Tabela de Experimentos (30s)
```
Exp | Pop | Gen | Mutacao | Selecao
#1  | 50  | 50  | 0.01    | tournament
#2  | 80  | 100 | 0.05    | tournament  ← Recomendado
#3  | 150 | 200 | 0.10    | tournament
```

#### 4.2 Ranking de Resultados (90s)
```
Rank | Nome        | Dist Inic | Dist Otim | Melhoria | Tempo
#1   | Balanceado  | 450.32    | 349.85    | 22.3%    | 3.2s
#2   | Rápido      | 450.32    | 380.12    | 15.6%    | 1.1s
#3   | Preciso     | 450.32    | 348.20    | 22.6%    | 8.7s
```
Falar: "O Balanceado (#2) é 99% tão bom quanto o Preciso, mas 2.7x mais rápido."

#### 4.3 Gráficos Comparativos (60s)
- **Convergência de cada config:** 3 curvas
- **Melhoria em %:** gráfico de barras

### Transição:
"Por fim, a integração com IA que gera relatórios automaticamente..."

---

## SEGMENTO 5: Aba LLM / Relatório (10:00 - 13:30)

### O que falar:
```
"A funcionalidade mais inovadora: geração automática de documentos 
com IA para diferentes públicos da organização."
```

### O que mostrar:

#### 5.1 Instruções para Motoristas (45s)
```
Botão: "Gerar Instruções para Motoristas"
Await ~2s

Exemplo de saída:
====================================
ROTEIRO DE ENTREGA — 24/03/2026
Base: Hospital Central

VEÍCULO 1 — Van Branca
Partida: 08:00

Parada 1: 08:05 - Hospital X, Rua A, 123
  Carga: 50kg
  Prioridade: CRÍTICA ⚠️
  
Parada 2: 08:15 - Clínica Y, Rua B, 456
  Carga: 40kg
  Prioridade: Alta
  ...

Retorno: 09:00
Distância: 85.32 km
====================================
```
Falar: "Motorista recebe tudo pronto, sem adivinhas."

#### 5.2 Relatório Executivo (45s)
```
Exemplo:
====================================
RELATÓRIO EXECUTIVO
Data: 24/03/2026

MÉTRICAS:
- Redução: 22.3%
- Economia diária (combustível): R$ 125
- Tempo economizado: 35 minutos
- Cobertura: 21 pontos em 3 veículos

RECOMENDAÇÕES:
1. Usar esta config como base
2. Ajustar para emergências
3. Monitorar autonomia dos veículos
====================================
```
Falar: "Gestor recebe documento executivo limpo."

#### 5.3 Perguntas e Respostas (45s)
```
Input: "Quais entregas têm prioridade crítica?"

Output (da IA):
"Existem 3 entregas com prioridade crítica:
1. Hospital X - 50kg (Parada 1 - Veículo 1)
2. Clínica Premium - 30kg (Parada 3 - Veículo 2)
3. Lab de Análises - 25kg (Parada 2 - Veículo 3)

Todas foram agendadas para as primeiras paradas 
dos seus respectivos roteiros para garantir 
entrega rápida."
```
Falar: "É tipo um chatbot da rota. Você pergunta o que quiser."

### Transição:
"Deixa eu fazer uma pergunta rápida..."

---

## SEGMENTO 6: Conclusão e Arquitetura (13:30 - 15:00)

### O que falar:
```
"RESUMO DO QUE VOCÊS VIRAM:

✅ Interface Streamlit profissional
✅ Otimização de rotas com visualizações aprimoradas  
✅ Mapas interativos com Folium
✅ Comparação de múltiplas configurações
✅ Geração automática de documentos com IA
✅ Chat para análise de rotas

ARQUITETURA:
- Python + Streamlit (interface)
- Algoritmo Genético (src/ga/)
- Integração OpenAI (fallback para templates)
- Visualização com Matplotlib e Folium
- 21 pontos de entrega, 3 veículos, múltiplas restrições

O sistema está pronto para produção em cenários 
hospitalares reais de São Paulo."
```

### O que mostrar:
- [ ] Seu rosto em webcam (30s)
- [ ] Diagrama de arquitetura (opcional, 20s)
- [ ] Slide final com logo (10s)

---

## 📊 Timing Estimado

| Segmento | Duração | Total |
|----------|---------|-------|
| 1. Intro | 1:30 | 1:30 |
| 2. Interface | 2:00 | 3:30 |
| 3. Otimização | 4:00 | 7:30 |
| 4. Experimentos | 2:30 | 10:00 |
| 5. LLM | 3:30 | 13:30 |
| 6. Conclusão | 1:30 | 15:00 |

**Total: 15 minutos exatos**

---

## 📋 Checklist Pré-Gravação

### Setup Técnico:
- [ ] venv ativado
- [ ] `streamlit run app.py` testado
- [ ] `.env` com OPENAI_API_KEY preenchida
- [ ] Webcam/áudio testados
- [ ] OBS Studio ou similar pronto

### Conteúdo:
- [ ] Sidebar configurado com valores padrão
- [ ] Dados de teste carregados (mock_data já vem no código)
- [ ] Aba Otimização executada e resultado em cache
- [ ] Este roteiro impresso à mão

### Dicas de Gravação:
- Não fale muito rápido (subtítulos depois)
- Pausas de 2-3s entre abas
- Zoom de tela para fonte legível
- Grave em 1080p, 30fps
- Áudio: microfone a ~30cm, sem ventilador fundo

---

## 💾 Estrutura Novo Projeto

```
8iadt-tech-challenge-fase2/
├── app.py                    ← PRINCIPAL (Streamlit)
├── .env.example              ← Template
├── .env                      ← Seu arquivo (não commitar)
├── requirements.txt
│
├── src/
│   ├── data/
│   │   ├── models.py         ← Classes: DeliveryPoint, Vehicle, Route
│   │   ├── mock_data.py      ← 21 pontos + 3 veículos de teste
│   │   └── distances.py      ← build_distance_matrix()
│   │
│   ├── genetic_algorithm/
│   │   └── ga_adapter.py     ← run_genetic_algorithm()
│   │
│   ├── visualization/
│   │   ├── route_map.py      ← create_route_map() (Folium)
│   │   ├── comparison_map.py ← create_comparison_map()
│   │   └── charts.py         ← Gráficos (Matplotlib)
│   │
│   ├── llm/
│   │   └── main.py           ← generate_driver_instructions(), etc
│   │
│   ├── experiments/
│   │   └── main.py           ← EXPERIMENTS list, run_experiments()
│   │
│   └── ga/                   ← Core GA original (ainda em uso)
│
└── docs/
    ├── ROTEIRO_VIDEO_V2.md   ← Este arquivo
    ├── RELATORIO_TECNICO.md
    ├── MANUAL_USUARIO.md
    └── ...
```

---

**Última atualização:** Março 2026 | v2.0
