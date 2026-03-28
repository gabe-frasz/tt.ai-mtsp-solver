# Solucionador de mTSP - Algoritmo Genético

Este projeto implementa um solucionador para o **Problema do Caixeiro Viajante Múltiplo (mTSP)** usando um **Algoritmo Genético (AG)** em Python. O Problema do Caixeiro-Viajante Múltiplo (mTSP) é uma versão do clássico Problema do Caixeiro-Viajante (TSP), em que vários vendedores trabalham juntos para visitar um conjunto de cidades.

## 📋 Descrição do Problema

Neste projeto, considera-se um cenário realista de uma empresa com 3 vendedores responsáveis por atender 30 cidades, representadas por coordenadas fixas em um plano cartesiano. Todos os vendedores partem de um depósito central localizado em (30, 30), realizam suas visitas e retornam ao ponto de origem ao final da rota.

O desafio é decidir quais cidades cada vendedor deve visitar e em que ordem, buscando tornar o trabalho da equipe o mais eficiente possível.

- 🎯 **Objetivos:**
O problema tem dois objetivos principais:
  - Reduzir ao máximo a distância total percorrida por todos os vendedores;
  - Manter as rotas equilibradas, evitando que alguns percorram muito mais que outros.
Assim, a ideia é encontrar uma solução que seja não só eficiente no geral, mas também justa na divisão do trabalho entre os vendedores.
 
- ⚠️ **Restrições:**
A solução deve respeitar as seguintes restrições:
  - **Cobertura completa**: cada cidade deve ser visitada exatamente uma vez;
  - **Limite de carga**: cada vendedor deve visitar entre 5 e 15 cidades;
  - **Balanceamento**: a diferença no número de cidades entre quaisquer dois vendedores não pode exceder 5;
  - **Limite de distância**: a rota total de cada vendedor não pode ultrapassar 350 unidades de distância;
  - **Ciclo fechado**: todas as rotas devem começar e terminar no depósito central.
 
- ⚙️ **Abordagem de Solução:**
Para resolver o problema, o projeto utiliza um **Algoritmo Genético**, inspirado no processo de evolução natural, para encontrar boas soluções de forma aproximada. Cada solução possível representa uma maneira de dividir e organizar as rotas entre os vendedores, e, ao longo das gerações, essas soluções vão sendo melhoradas por meio de operações como **seleção, cruzamento e mutação**.

## 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/your-username/tt.ai-mtsp-solver.git
   cd tt.ai-mtsp-solver
   ```

2. **(Opcional) Crie um ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/bin/activate  # Linux/macOS
   ```

3. **Instale as dependências:**
   *(Opcional)* Se você quiser usar arquivos de configuração YAML:
   ```bash
   pip install pyyaml
   ```

## 🚀 Execução:

Execute o solucionador usando os parâmetros padrão:
```bash
python3 main.py
```

### Configuração via Flags da CLI

Você pode sobrescrever os parâmetros diretamente da linha de comando:
```bash
python3 main.py -p 200 -g 500 -m 0.1 -w 3
```

**Opções disponíveis:**
- `-p, --population`: Tamanho da população (default: 100).
- `-g, --generations`: Número de gerações (default: 1000).
- `-m, --mutation`: Taxa de mutação (0.0 to 1.0).
- `-x, --crossover`: Taxa de cruzamento (0.0 to 1.0).
- `-e, --elite`: Número de indivíduos de elite a serem preservados.
- `-c, --config`: Caminho para um arquivo de configuração `.json` ou `.yaml`.

### Exemplos de saída

O programa exibirá a rota completa para cada trabalhador, as distâncias individuais, a distância total, o desvio padrão e quaisquer violações de restrição encontradas.

## 📂 Estrutura do Projeto

- `src/`: Código-fonte contendo a lógica do algoritmo genético, a definição do problema e utilitários.
- `main.py`: Ponto de entrada para a aplicação.
- `docs/`: Documentação técnica (modelagem e hiperparâmetros).
