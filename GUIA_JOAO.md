# 🟡 Guia de Experimentos e Documentação para João

Este documento descreve **exatamente o que você (João) precisa fazer** para sua parte do projeto.

---

## 📌 Resumo do Seu Papel

Você é responsável por:
1. ✅ **Rodar Experimentos** com diferentes parâmetros do GA
2. ✅ **Comparar Resultados** e gerar tabelas/gráficos
3. ✅ **Documentar** como rodar tudo
4. ✅ **Integrar LLM** para gerar relatórios em linguagem natural
5. ✅ **Preparar Apresentação** (vídeo e relatório técnico)

---

## 🚀 FASE 1: Começar com Experimentos (AGORA!)

### Passo 1: Entender o Script de Experimentos

Você já tem um script pronto em `src/experiments/main.py`. Ele faz:

```
1. Define combinações de parâmetros (PARAM_GRID)
2. Para cada combinação:
   - Roda GA 3 vezes
   - Calcula média e desvio padrão
   - Salva resultados
3. Exibe tabela com:
   - Melhor configuração (menor distância)
   - Mais rápida
   - Mais estável
```

### Passo 2: Rodar o Experimento

```bash
# Ativa ambiente virtual
.\venv\Scripts\activate

# Roda experimentos
python src/experiments/main.py
```

**Saída esperada:**
```
📊 Total de combinações a testar: 135
   Rodadas por combinação: 3
   Total de execuções: 405

[1/135] Testando: {'population_size': 100, 'mutation_probability': 0.1, ...}
  ✓ Run 1: 523.45 em 2.34s
  ✓ Run 2: 521.12 em 2.31s
  ✓ Run 3: 524.89 em 2.30s
  📈 Agregado: 523.15 ± 1.89

[2/135] ...
...
✅ Resultados salvos em: results/experiments_20260314_143022.csv
✅ Resultados também salvos em: results/experiments_20260314_143022.json

🏆 MELHOR CONFIGURAÇÃO:
   Distância média: 513.42
   Desvio padrão:   8.34
   Tempo médio:     3.15s
   Parâmetros:
      - population_size: 200
      - mutation_probability: 0.2
      - tournament_k: 3
      - max_generations: 150
      - selection_type: tournament
```

---

## 📈 FASE 2: Analisar Resultados

Depois de rodar os experimentos, você tem um arquivo CSV com os resultados.

### Criar um Notebook de Análise

Crie `src/notebooks/analysis.ipynb` com:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Carrega os resultados
results = pd.read_csv('results/experiments_20260314_143022.csv')

# 1. Melhor configuração geral
best_row = results.loc[results['avg_best_distance'].idxmin()]
print(f"MELHOR CONFIGURAÇÃO: {best_row}")

# 2. Impacto de cada parâmetro
for param in ['population_size', 'mutation_probability', 'tournament_k']:
    avg_by_param = results.groupby(param)['avg_best_distance'].mean()
    print(f"\nImpacto de {param}:")
    print(avg_by_param)

# 3. Gráfico: População vs Convergência
fig, ax = plt.subplots()
for pop_size in results['population_size'].unique():
    subset = results[results['population_size'] == pop_size]
    ax.plot(subset['tournament_k'], subset['avg_best_distance'], label=f"Pop {pop_size}")
ax.legend()
plt.show()

# 4. Gráfico: Tempo vs Qualidade (Pareto)
fig, ax = plt.subplots()
ax.scatter(results['avg_execution_time'], results['avg_best_distance'])
ax.set_xlabel('Tempo Médio (s)')
ax.set_ylabel('Distância Média (km)')
ax.set_title('Trade-off: Velocidade vs Qualidade')
plt.show()
```

### Perguntas a responder:

- ❓ Qual é a **melhor configuração geral**?
- ❓ Qual parâmetro tem **mais impacto** na qualidade?
- ❓ Qual métodos de seleção é **mais rápido**?
- ❓ Há trade-off entre **velocidade e qualidade**?
- ❓ A **probabilidade de mutação** afeta convergência?

---

## 📝 FASE 3: Documentação Técnica

Crie um documento `docs/RELATORIO_TECNICO.md` com:

### 1. Implementação do GA
```markdown
## Descrição da Implementação

### População Inicial (Híbrida)
- 40% Nearest Neighbour
- 40% Aleatória  
- 20% Convex Hull Aproximado

### Operadores Genéticos
- **Seleção:** 3 métodos (Torneio, Top-10, Roleta)
- **Crossover:** Order Crossover (OX)
- **Mutação:** 2-opt Swap
- **Elitismo:** Melhor indivíduo passa direto para próxima geração

### Parâmetros Testados
| Parâmetro | Valores Testados |
|---|---|
| population_size | 100, 200, 500 |
| mutation_probability | 0.1, 0.2, 0.5 |
| tournament_k | 2, 3, 5 |
| max_generations | 100, 200 |
| selection_type | tournament, top10, roulette |
```

### 2. Resultados Experimentais
```markdown
## Resultados

### Melhor Configuração
[Tabela com parâmetros e métricas]

### Análise de Sensibilidade
[Gráficos mostrando como cada parâmetro afeta resultado]

### Comparativo com Outras Abordagens
| Abordagem | Distância | Tempo |
|---|---|---|
| Aleatório | 650 km | 0.01s |
| Greedy (NN) | 550 km | 0.05s |
| GA (nosso) | 513 km | 3.2s |
```

### 3. Conclusões
```markdown
## Discussão

O GA encontrou soluções **10-20% melhores** que heurística gulosa,
com trade-off de tempo computacional aceitável para contexto hospitalar.
```

---

## 🤖 FASE 4: Integração com LLM

### Criar `src/llm/main.py`

```python
from openai import OpenAI

def generate_delivery_report(route, cities, total_distance, vehicle_count=1):
    """
    Usa LLM para gerar relatório em linguagem natural
    """
    
    client = OpenAI(api_key="sua-chave-aqui")
    
    prompt = f"""
    Você é um analista de logística hospitalar. 
    Recebeu uma rota otimizada para distribuição de medicamentos.
    
    Dados da rota:
    - Sequência de entrega: {route}
    - Distância total: {total_distance:.2f} km
    - Número de pontos: {len(cities)}
    - Veículos usados: {vehicle_count}
    
    Gere um relatório em português com:
    1. Resumo da rota
    2. Tempo estimado (assumir 60 km/h)
    3. Economia comparado a rota aleatória
    4. Recomendações de otimização  
    5. Instruções claras para o motorista
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000
    )
    
    return response.choices[0].message.content

# Uso:
route = [0, 5, 3, 8, 1, 2, 7, 4, 6, 0]
cities = [(x, y) for x, y in ...] 
distance = 523.45

report = generate_delivery_report(route, cities, distance)
print(report)
```

### Para usar:

1. **Instale OpenAI SDK:**
   ```bash
   pip install openai
   ```

2. **Crie conta e pegue chave em** https://platform.openai.com/account/api-keys

3. **Configure chave (segurança):**
   ```bash
   # Crie arquivo .env na raiz do projeto
   OPENAI_API_KEY=sk-...seu-token...
   ```

4. **Use no seu código:**
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   api_key = os.getenv("OPENAI_API_KEY")
   ```

---

## 🎬 FASE 5: Vídeo de Demonstração

Crie um vídeo (~15 min) mostrando:

### Roteiro sugerido:

**[0:00-1:00]** Introdução
- O que é MedRoute?
- Por que otimização de rotas importa?

**[1:00-3:00]** Arquitetura
- Diagrama dos componentes
- Explicar GA, LLM, Visualização

**[3:00-7:00]** Demonstração ao vivo
- Rodar o GA
- Mostrar convergência em tempo real
- Exibir rotas iniciais vs otimizadas

**[7:00-10:00]** Resultados
- Tabela de experimentos
- Gráficos comparativos  
- Economia obtida

**[10:00-15:00]** Relatório LLM
- Mostrar saída de texto gerada
- Explicar instruções para motorista
- Demonstrar customização de prompts

---

## ✅ Checklist de Entregáveis

### CÓDIGO
- [x] `src/experiments/main.py` → Script de experimentos
- [x] `src/notebooks/demo.ipynb` → Notebook de demonstração
- [ ] `src/notebooks/analysis.ipynb` → Análise dos resultados (CRIAR)
- [ ] `src/llm/main.py` → Integração LLM (CRIAR)
- [ ] `.env` → Variáveis de ambiente (CRIAR)
- [ ] `src/ga/test.py` → Testes (JÁ EXISTE/VERIFY)

### DOCUMENTAÇÃO
- [ ] `docs/RELATORIO_TECNICO.md` → Relatório técnico (CRIAR)
- [ ] `docs/MANUAL_USUARIO.md` → Como usar o sistema (CRIAR)
- [x] `README.md` → Já existe

### APRESENTAÇÃO
- [ ] `video_demo.mp4` → Vídeo de demonstração
- [ ] `slides_apresentacao.pptx` → Slides (opcional)

---

## 🎯 Próximos Passos Imediatos

1. **Hoje:** Rodar `python src/experiments/main.py` e ver se funciona
2. **Amanhã:** Criar notebook de análise (`src/notebooks/analysis.ipynb`)
3. **Próximos dias:** Escrever relatório técnico
4. **Depois:** Setup de LLM e testes
5. **Final:** Gravar vídeo

---

## 📞 Dúvidas Frequentes

**P: Quanto tempo leva para rodar todos os experimentos?**
R: ~2-3 minutos (135 combinações × 3 rodadas, com GA rápido)

**P: Posso modificar PARAM_GRID para testar outros valores?**
R: Sim! Edit `src/experiments/main.py` linha ~34

**P: Como uso a API da OpenAI sem gastar muito?**
R: Use `gpt-3.5-turbo` (mais barato). Configure limites na conta.

**P: Preciso rodar os testes antes de fazer commits?**
R: Sim! `python -m unittest discover -s src -p "test*.py"`

---

**Última atualização:** Março 2026
