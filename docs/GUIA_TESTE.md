# Guia de Teste - Integração OpenAI (MedRoute LLM)

## 🔧 Passo 1: Configurar API Key

### 1.1 Obter Chave OpenAI
1. Vá para https://platform.openai.com/api-keys
2. Faça login com sua conta OpenAI (crie se não tiver)
3. Clique em "+ Create new secret key"
4. Copie a chave (aparece uma única vez - **guarde em local seguro**)

### 1.2 Configurar Arquivo .env

Na raiz do projeto (`8iadt-tech-challenge-fase2/`), você já tem `.env.example`.  
**Copie para `.env`:**

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

**Edite o arquivo `.env` com a chave:**

```env
# .env (NUNCA commit isso para GitHub!)
OPENAI_API_KEY=sk-proj-xxx...  # Colar aqui (chave secreta)
OPENAI_MODEL=gpt-3.5-turbo     # Padrão OK
DEBUG=false
```

**⚠️ IMPORTANTE:** Adicione `.env` ao `.gitignore` para não vazar chave:

```bash
# No terminal
echo ".env" >> .gitignore
```

---

## 🧪 Passo 2: Teste Rápido (Terminal/PowerShell)

### 2.1 Ativar Ambiente Virtual

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 2.2 Rodar Teste Simples

Crie arquivo temporário `test_llm_simple.py`:

```python
# test_llm_simple.py
from src.llm.main import MedRouteReportGenerator

print("🔗 Testando conexão OpenAI...")

try:
    gerador = MedRouteReportGenerator()
    print("✅ API Key carregada com sucesso!")
    
    # Teste 1: Resumo rápido (mais rápido, menos tokens)
    print("\n📝 Gerando resumo rápido...")
    resumo = gerador.generate_quick_summary(
        distance=419.2,
        num_stops=20,
        time_minutes=45,
        vehicles=2
    )
    print(f"Resumo:\n{resumo}\n")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    print("💡 Dica: Verifique se OPENAI_API_KEY está em .env")
```

**Rodar:**

```bash
python test_llm_simple.py
```

**Saída esperada:**

```
🔗 Testando conexão OpenAI...
✅ API Key carregada com sucesso!

📝 Gerando resumo rápido...
Resumo:
Rota otimizada para 20 paradas em 419.2km usando 2 veículos, 
tempo estimado 45 minutos, via algoritmo genético (GA).

✅ Teste passou!
```

---

## 🚀 Passo 3: Teste Completo (Todos os 4 Tipos de Relatório)

Crie arquivo `test_llm_complete.py`:

```python
# test_llm_complete.py
from src.llm.main import MedRouteReportGenerator
import json

print("🚀 TESTE COMPLETO - MedRoute LLM Integration\n")
print("="*60)

try:
    gerador = MedRouteReportGenerator()
    print("✅ Conexão OpenAI estabelecida")
    print("="*60)
    
    # TESTE 1: Resumo Executivo
    print("\n[1/4] Gerando Resumo Executivo...\n")
    resumo = gerador.generate_quick_summary(
        distance=419.2,
        num_stops=20,
        time_minutes=45,
        vehicles=2
    )
    print(f"📄 Resultado:\n{resumo}\n")
    print("-"*60)
    
    # TESTE 2: Relatório de Eficiência
    print("\n[2/4] Gerando Relatório de Eficiência...\n")
    relat_efic = gerador.generate_efficiency_report(
        total_distance=419.2,
        num_cities=20,
        num_vehicles=2,
        avg_distance_random=670,  # baseline
        execution_time=3.2
    )
    print(f"📊 Resultado:\n{relat_efic}\n")
    print("-"*60)
    
    # TESTE 3: Instruções para Motorista
    print("\n[3/4] Gerando Instruções para Motorista...\n")
    
    # Dados exemplo (estrutura simplificada)
    rota_exemplo = [0, 5, 3, 2, 1, 4, 0]
    cidades_exemplo = [
        {"id": 0, "x": 0, "y": 0, "nome": "HOSPITAL (Saída)"},
        {"id": 1, "x": 10.5, "y": 20.3, "nome": "Clínica Central"},
        {"id": 2, "x": 5.2, "y": 15.1, "nome": "Farmácia Zona Sul"},
        {"id": 3, "x": 25.0, "y": 30.5, "nome": "Centro Diagnóstico"},
        {"id": 4, "x": 18.3, "y": 8.9, "nome": "Consultório Dr. Silva"},
        {"id": 5, "x": 35.2, "y": 22.1, "nome": "Lab Análises"},
    ]
    
    instrucoes = gerador.generate_driver_instructions(
        route=rota_exemplo,
        cities=cidades_exemplo,
        route_distance=419.2,
        estimated_time_minutes=45
    )
    print(f"🚗 Resultado:\n{instrucoes}\n")
    print("-"*60)
    
    # TESTE 4: Análise Técnica
    print("\n[4/4] Gerando Análise Técnica...\n")
    analise = gerador.generate_optimization_analysis(
        best_distance=419.2,
        worst_distance=470.0,
        avg_distance=440.0,
        generations_to_converge=95,
        population_size=200,
        mutation_rate=0.2
    )
    print(f"🔬 Resultado:\n{analise}\n")
    print("="*60)
    print("\n✅ TODOS OS TESTES PASSARAM!\n")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("\n💡 Dicas de Troubleshooting:")
    print("  1. Verifique se OPENAI_API_KEY está em .env")
    print("  2. Verifique se a chave é válida em https://platform.openai.com/api-keys")
    print("  3. Verifique se você tem crédito suficiente em sua conta OpenAI")
    print("     (vá a https://platform.openai.com/account/billing/overview)")
    print("  4. Se erro de 'rate limit', aguarde 1 minuto e tente novamente")
```

**Rodar:**

```bash
python test_llm_complete.py
```

**Saída esperada:** ~2-3 minutos para rodar (dependendendo de latência da OpenAI)

```
🚀 TESTE COMPLETO - MedRoute LLM Integration

============================================================
✅ Conexão OpenAI estabelecida
============================================================

[1/4] Gerando Resumo Executivo...

📄 Resultado:
Rota otimizada para 20 paradas em 419.2km usando 2 veículos, 
tempo estimado 45 minutos, via algoritmo genético (GA).

------------------------------------------------------------

[2/4] Gerando Relatório de Eficiência...

📊 Resultado:
[RELATÓRIO LONGO aqui com análise de eficiência...]

------------------------------------------------------------

...

✅ TODOS OS TESTES PASSARAM!
```

---

## 📊 Passo 4: Teste Integrado (Com Streamlit)

Se quiser testar **dentro da interface Streamlit**:

### 4.1 Abrir Streamlit

```bash
streamlit run src/ga/app.py
```

Abre em http://localhost:8501

### 4.2 Adicionar Botão de Teste (Futuro)

Você pode adicionar ao `src/ga/app.py` (ao final):

```python
# Adicionar ao final de app.py
import streamlit as st
from src.llm.main import MedRouteReportGenerator

# Sidebar com botão de teste
with st.sidebar:
    if st.button("🤖 Gerar Relatório LLM"):
        st.write("### Relatório de Eficiência")
        try:
            gerador = MedRouteReportGenerator()
            relatorio = gerador.generate_quick_summary(
                distance=419.2,
                num_stops=20,
                time_minutes=45,
                vehicles=2
            )
            st.markdown(relatorio)
        except Exception as e:
            st.error(f"Erro ao gerar relatório: {e}")
```

---

## 💰 Passo 5: Entender Custos OpenAI

**Modelo usado:** `gpt-3.5-turbo`

**Preço (aproximado em 2026):**
- **Entrada:** $0.50 / 1M tokens
- **Saída:** $1.50 / 1M tokens

**Custo por relatório (estimada):**
- Resumo rápido: ~50 tokens entrada, 50 saída = ~$0.00005 (0.00005¢ 😄)
- Relatório eficiência: ~100 entrada, 200 saída = ~$0.0004
- Instruções motorista: ~100 entrada, 600 saída = ~$0.001
- Análise técnica: ~150 entrada, 200 saída = ~$0.0006

**Custo total para gerar os 4 relatórios:** ~$0.002 (0.2¢ de centavo!)

**Recomendação:** Use gerador de forma sensata (não em loop infinito), mas o custo é negligenciável.

---

## 🐛 Troubleshooting Comum

### Erro: `ModuleNotFoundError: No module named 'openai'`

```bash
# Instalar dependência
pip install openai
```

### Erro: `OPENAI_API_KEY not found in environment`

```
❌ Erro: API Key não carregada

Solução:
  1. Confirme que .env existe na raiz do projeto
  2. Abra .env e verifique se tem:
     OPENAI_API_KEY=sk-proj-...
  3. Reinicie terminal/Jupyter (variáveis de ambiente só são lidas na inicialização)
```

### Erro: `401 Unauthorized - Invalid API Key`

```
❌ Erro: Chave inválida ou expersa

Solução:
  1. Gere uma NOVA chave em https://platform.openai.com/api-keys
  2. Chaves antigas podem expirar
  3. Copie a nova para .env
```

### Erro: `429 Too Many Requests - Rate Limited`

```
❌ Erro: Muitas requisições muito rápido

Solução:
  1. Aguarde 1-2 minutos
  2. Tente novamente
  3. Se persistir, entre em https://platform.openai.com/account/billing/limits
```

### Erro: `Insufficient quota - You exceeded your current quota`

```
❌ Erro: Sem crédito suficiente na conta

Solução:
  1. Vá a https://platform.openai.com/account/billing/overview
  2. Adicione método de pagamento ou créditos
  3. Aguarde 5 minutos para sincronizar
```

---

## ✅ Checklist Final

- [ ] Arquivo `.env` criado (cópia de `.env.example`)
- [ ] `OPENAI_API_KEY` preenchida com chave válida
- [ ] `pip install openai` executado
- [ ] `.env` adicionado a `.gitignore`
- [ ] `test_llm_simple.py` passou
- [ ] `test_llm_complete.py` passou
- [ ] Streamlit testado (abra e rode até fim)
- [ ] Análise de custos compreendida (negligenciável)

---

**Após completar: Você está pronto para gravar o vídeo!** 🎬
