# Manual do Usuário - MedRoute

**Otimização de Rotas para Entrega de Medicamentos com Algoritmo Genético + LLM**

---

## 📋 Índice

1. [Instalação](#instalação)
2. [Configuração](#configuração)
3. [Como Usar](#como-usar)
4. [Entendendo os Resultados](#entendendo-os-resultados)
5. [Exemplos de Uso](#exemplos-de-uso)
6. [Troubleshooting](#troubleshooting)
7. [Estrutura do Projeto](#estrutura-do-projeto)

---

## 🔧 Instalação

### Pré-requisitos

- **Python 3.10+** (verificar com `python --version`)
- **pip** (gerenciador de pacotes, vem com Python)
- **Git** (para clonar o repositório)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/8iadt-tech-challenge-fase2.git
cd 8iadt-tech-challenge-fase2
```

### Passo 2: Criar Ambiente Virtual

Um ambiente virtual isola as dependências do projeto:

```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### Passo 3: Ativar Ambiente Virtual

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

Você saberá que está ativado quando o terminal mostrar `(venv)` no início da linha.

### Passo 4: Instalar Dependências

```bash
pip install -r requirements.txt
```

Isto instala:
- `numpy` - computações numéricas
- `pandas` - análise de dados
- `matplotlib` - visualizações
- `streamlit` - interface web
- `openai` - integração com OpenAI
- `python-dotenv` - configuração de variáveis de ambiente
- E mais...

---

## ⚙️ Configuração

### Configurar API Key da OpenAI (Obrigatório para Relatórios)

O sistema LLM que gera relatórios requer uma API key da OpenAI.

#### 1. Obter API Key

1. Vá para https://platform.openai.com/account/api-keys
2. Clique em **"+ Create new secret key"**
3. **Copie a chave** (aparece uma única vez!)
4. Guarde em local seguro

#### 2. Configurar Arquivo `.env`

Na raiz do projeto, crie um arquivo chamado `.env`:

```bash
# Windows
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

**Abra o arquivo `.env` e preencha:**

```env
OPENAI_API_KEY=sk-proj-seu-token-aqui

# Mantém estes valores padrão:
OPENAI_MODEL=gpt-3.5-turbo
DEBUG=False
LOG_LEVEL=INFO
```

**⚠️ Importante:**
- **NUNCA** faça commit do arquivo `.env` com chave verdadeira
- `.env` já está em `.gitignore`, então está seguro
- Se vazar a chave, revogue em https://platform.openai.com/account/api-keys

#### 3. Verificar Crédito OpenAI

```
https://platform.openai.com/account/billing/overview
```

Se não tiver crédito ("Usage limit reached"), a integração LLM não funcionará.

---

## 🎯 Como Usar

### Interface Interativa (Recomendado)

A forma mais amigável é usar a interface Streamlit com 3 abas:

```bash
streamlit run app.py
```

Abre automaticamente em `http://localhost:8501`

#### Na Interface:

**Sidebar (esquerda):**
- Configura parâmetros do Algoritmo Genético:
  - **População:** 50-200 (default: 80)
  - **Gerações:** 10-200 (default: 100)
  - **Taxa de Mutação:** 0.01-0.20 (default: 0.05)
  - **Seed Aleatória:** para reproduzibilidade

- Edita pontos de entrega:
  - Demanda (kg) de cada ponto
  - Prioridade (Crítica, Alta, Média, Baixa)
  - Remove/adiciona novos pontos

- Edita frota de veículos:
  - Capacidade (kg) de cada veículo
  - Autonomia máxima (km)
  - Remove/adiciona novos veículos

#### Aba 1: Otimização

1. **Clica "Rodar Otimização"**
2. **Visualiza métricas:**
   - Distância inicial (rota aleatória)
   - Distância otimizada (após GA)
   - Percentual de melhoria
   - Número de gerações executadas

3. **Vê rotas por veículo:**
   - Cada parada com demanda e prioridade
   - Sequência de entrega (críticas primeiro)

4. **Explora 4 gráficos:**
   - Convergência: evolução da melhor solução
   - Comparação: antes vs depois
   - Carga de veículos: balanceamento
   - Distâncias: por rota

5. **Interage com 2 mapas:**
   - Mapa otimizado: uma cor por veículo
   - Comparativo: antes (aleatório) vs depois (otimizado)

#### Aba 2: Experimentos

1. Mostra 3 configurações pre-definidas de GA
2. **Clica "Rodar Todos os Experimentos"**
3. Vê ranking de resultados:
   - Qual config foi melhor?
   - Qual foi mais rápida?
   - Trade-off qualidade vs velocidade
4. Gráficos comparativos de convergência e melhoria

#### Aba 3: LLM / Relatório

Gera 3 tipos de documentos com IA:

**Sub-aba: Instruções para Motoristas**
- Gera roteiro pronto pra imprimir
- Paradas, horários, endereços
- Demanda de cada entrega

**Sub-aba: Relatório Executivo**
- Resumo para gestor
- Métricas de economia
- Recomendações

**Sub-aba: Pergunte Algo**
- Chat interativo
- Faça perguntas sobre a rota
- IA responde em português

### Resultados:
   - 5 métricas principais
   - Sequência de entregas
   - Seção "🤖 Geração de Relatórios com IA" (4 abas)

#### Gerando Relatórios com IA:

Após a otimização, na seção inferior, escolha um relatório:

| Aba | Para Quem | Conteúdo |
|-----|-----------|----------|
| 📊 Eficiência | Gestores | Economia, ROI, métricas |
| 🚗 Motorista | Campo | Instruções passo-a-passo |
| 🔬 Análise Técnica | Analistas | Configuração, convergência |
| ⚡ Resumo Rápido | Executivos | Uma linha |

### Opção 2: Jupyter Notebook (Avançado)

Para análise e experimentação em notebook:

```bash
jupyter notebook
```

Abra [notebooks/main.ipynb](../notebooks/main.ipynb) para exemplos interativos.

### Opção 3: Script CLI (Programático)

Para rodar comparação de 3 experimentos via terminal:

```bash
python -c "from src.experiments.main import run_experiments; run_experiments()"
```

Isto testa 3 configurações pré-definidas de GA.

---

## 📊 Entendendo os Resultados (Aba Otimização)

### Métricas Principais

**1. Distância Inicial:**
- Rotas geradas aleatoriamente (baseline)
- Sempre significativamente maior

**2. Distância Otimizada:**
- Melhor rota encontrada pelo GA
- Redução típica: 15-25%

**3. Percentual de Melhoria:**
- (Distância Inicial - Distância Otimizada) / Distância Inicial × 100
- Maior = melhor

**4. Restrições Satisfeitas:**
- ✅ Entregas críticas primeiro
- ✅ Capacidade dos veículos respeitada
- ✅ Todas as paradas cobertos

**5. Solução encontrada na geração:**
- Em qual geração convergiu
- Mostra eficiência do algoritmo

### Entendendo a Convergência

```
Geração 1:   Distância = 800km  (exploração - população diversa)
Geração 50:  Distância = 450km  (melhora significativa)
Geração 95:  Distância = 419km  (melhor encontrado)
Geração 100: Distância = 419km  (estabilizado - elitismo)
```

Quando a linha do gráfico fica plana, significa que o algoritmo não encontra soluções melhores.

### Entendendo os Gráficos

**Convergência:**
```
Gen 1:   Dist = 350km  (população inicial aleatória)
Gen 30:  Dist = 320km  (primeira melhora)
Gen 70:  Dist = 295km  (convergência)
Gen 100: Dist = 295km  (estabilizado)
```

**Carga de Veículos:**
- Barras equilibradas = boa distribuição
- Barra acima de 100% = erro de restrição

**Comparação Antes/Depois:**
- Linha inicial = rota aleatória
- Linha otimizada = resultado final

---

## 💡 Exemplos de Uso (v2.0)

### Exemplo 1: Demo Rápida com Dados de Teste (2 minutos)

```
Ação:
1. app.py já carrega 21 pontos + 3 veículos automaticamente
2. Sidebar: Aceite valores padrão (pop=80, gen=100, mut=0.05)
3. Clique "Rodar Otimização"
4. Veja métricas, rotas, gráficos, mapas
```

Tempo: ~3 segundos de execução (computação rápida).

### Exemplo 2: Customizar Dados de Entrega (5 minutos)

```
Ação:
1. Sidebar → Expanda "Pontos de Entrega"
2. Edite demanda de um ponto (ex: Hospital Central de 50kg para 75kg)
3. Expanda "Veículos"
4. Mude capacidade máxima de Van Branca de 200kg para 250kg
5. Clique "Rodar Otimização"
6. Veja como a solução se adapta
```

Aprendizado: Restrições de capacidade impactam fortemente.

### Exemplo 3: Comparar Configurações (3 minutos)

```
Ação:
1. Clique na aba "Experimentos"
2. Clique "Rodar Todos os Experimentos"
4. Veja ranking: qual config foi melhor?
5. Veja trade-off: velocidade vs qualidade
```

Aprendizado: Configuração "Balanceado" é 99% boa em 2.7x mais rápido.
5. Aguarde ~2s pelo resultado da IA
```

Você recebe um relatório executivo pronto para apresentação!

### Exemplo 4: Instruções para Motorista

```
1. Rode otimização
2. Scroll até "🤖 Geração de Relatórios com IA"
3. Clique na aba "🚗 Motorista"
4. Clique "🗺️ Gerar Instruções para Motorista"
5. Copie o texto e envie para o motorista
```

Motorista recebe algo como:
```
ROTA OTIMIZADA - 19 PARADAS

Saída: 08:00 - Hospital Central (Depósito)
Parada 1: 08:05 - Rua A, nº 123 (Clínica Silva)
Parada 2: 08:12 - Rua B, nº 456 (Farmácia Central)
...
Retorno: 09:00 - Hospital Central
```

---

## 🐛 Troubleshooting

### Erro: "No module named 'streamlit'"

**Solução:** Instalar dependências

```bash
pip install -r requirements.txt
```

### Erro: "ModuleNotFoundError: No module named 'openai'"

**Solução:** Instalar pacote específico

```bash
pip install openai
```

### Erro: "OPENAI_API_KEY not found in environment"

**Solução:**
1. Verificar se arquivo `.env` existe na raiz
2. Verificar se tem `OPENAI_API_KEY=sk-proj-...` dentro
3. Reiniciar terminal (variáveis de ambiente carregam apenas na inicialização)

### Erro: "401 Unauthorized - Invalid API Key"

**Solução:**
1. Chave inválida ou expirada
2. Gere nova chave em https://platform.openai.com/account/api-keys
3. Atualize `.env`

### Erro: "429 Too Many Requests"

**Solução:** Aguarde 1-2 minutos e tente novamente. OpenAI tem limite de requisições.

### Erro: "Insufficient quota"

**Solução:**
1. Vá a https://platform.openai.com/account/billing/overview
2. Adicione método de pagamento ou créditos
3. Aguarde 5 minutos para sincronizar

### Streamlit não abre em http://localhost:8501

**Solução:**
1. Verifique se Streamlit rodou sem erros no terminal
2. Copie a URL manualmente (ex: http://192.168.0.3:8501)
3. Tente noutra porta: `streamlit run app.py --server.port 8502`

### Gráficos não aparecem

**Solução:**
1. Aguarde a execução completar (pode levar minutos)
2. Se problema persistir, atualize a página
3. Tente com número menor de gerações

---

## 📁 Estrutura do Projeto (v2.0)

```
8iadt-tech-challenge-fase2/
├── app.py                           # Interface Streamlit PRINCIPAL (3 abas)
│
├── src/
│   ├── data/                        # Modelos e dados
│   │   ├── models.py                # Classes: DeliveryPoint, Vehicle, Route, OptimizationResult
│   │   ├── mock_data.py             # 21 pontos de entrega + 3 veículos de teste
│   │   └── distances.py             # build_distance_matrix()
│   │
│   ├── genetic_algorithm/           # Core do GA
│   │   └── ga_adapter.py            # run_genetic_algorithm() - adaptador
│   │
│   ├── visualization/               # Gráficos e mapas (NOVO)
│   │   ├── route_map.py             # create_route_map() com Folium
│   │   ├── comparison_map.py        # create_comparison_map() - antes/depois
│   │   └── charts.py                # Convergência, carga, distâncias
│   │
│   ├── llm/                         # Geração de documentos com IA
│   │   └── main.py                  # generate_driver_instructions(), generate_route_report(), ask_question()
│   │
│   ├── experiments/                 # Comparação de múltiplas configs
│   │   └── main.py                  # EXPERIMENTS list, run_experiments()
│   │
│   ├── ga/                          # Algoritmo Genético original (v1.0 - referência)
│   │   ├── algorithm.py
│   │   ├── population.py
│   │   ├── fitness.py
│   │   ├── selection.py
│   │   ├── crossover.py
│   │   ├── mutation.py
│   │   ├── vrp_models.py
│   │   └── ...
│   │
│   ├── config/
│   │   └── config.py                # Configurações globais
│   │
│   └── [outros módulos]
│
├── docs/
│   ├── RELATORIO_TECNICO.md         # Análise técnica detalhada
│   ├── ROTEIRO_VIDEO_V2.md          # Script para vídeo demo (15 min)
│   ├── GUIA_TESTE.md                # Como testar componentes
│   └── MANUAL_USUARIO.md            # Este arquivo
│
├── notebooks/
│   └── main.ipynb                   # Exemplos de uso em Jupyter
│
├── .env.example                     # Template para variáveis de ambiente
├── .env                             # Suas credenciais (não commitar!)
├── .gitignore                       # Regras do git
├── requirements.txt                 # Dependências Python
└── README.md                        # Introdução ao projeto
```

---

## 🚀 Próximos Passos

1. **Explorar Aba Otimização:**
   - Ajuste população (50-200), gerações (50-200), mutação (0.01-0.20)
   - Veja como cada parâmetro afeta convergência
   - Teste com dados reais (pontos de entrega, veículos)

2. **Comparar Experimentos:**
   - Execute os 3 experimentos pré-configurados
   - Identifique o melhor trade-off qualidade/velocidade
   - Use para calibração futura

3. **Gerar Documentos com IA:**
   - Instrções para motoristas (impressível)
   - Relatório executivo (para gestor)
   - Pergunte à IA sobre rotas específicas

4. **Análise Avançada:**
   - Abra [notebooks/main.ipynb](../notebooks/main.ipynb) para experimentação
   - Modifique pontos/veículos para seu caso
   - Implemente suas próprias restrições

5. **Customização:**
   - Adicione novos tipos de prioridade em `src/data/models.py`
   - Implemente novo operador genético em `src/ga/mutation.py`
   - Modifique função de fitness em `src/ga/fitness.py`

---

## 📞 Suporte

Se encontrar problemas:

1. **Verifique este manual** (section Troubleshooting)
2. **Leia os comentários no código** (são muito detalhados)
3. **Consulte RELATORIO_TECNICO.md** para contexto técnico
4. **Issue no GitHub?** Abra um issue com:
   - Descrição do problema
   - Output completo do erro
   - Seus parâmetros usados

---

## 📄 Licença

Este projeto foi desenvolvido como parte do Tech Challenge PosTech IA para Devs.

---

**Última atualização:** Março 2026  
**Versão:** 2.0 (refatoração com novo layout Streamlit e integração visual)
