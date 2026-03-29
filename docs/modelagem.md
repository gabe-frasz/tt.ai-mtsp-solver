# Problema de Múltiplos Vendedores Viajantes

Descritivo da modelagem do problema principal com detalhamento das seguintes seções:


- [Problema de Múltiplos Vendedores Viajantes](#problema-de-múltiplos-vendedores-viajantes)
  - [_***Cromossomo***_](#cromossomo)
    - [**Representação de genes**](#representação-de-genes)
    - [**Domínio dos valores**](#domínio-dos-valores)
    - [**Tamanho do cromossomo**](#tamanho-do-cromossomo)
  - [_***Função de aptidão***_](#função-de-aptidão)
    - [**Fórmula**](#fórmula)
    - [**Componente**](#componente)
  - [_***Operadores***_](#operadores)
  - [_***Inicialização***_](#inicialização)
  - [_***Critério de Parada***_](#critério-de-parada)



## _***Cromossomo***_

A solução implementada foi um cromossomo unidimensional, ou seja, vetor 1D, composto por inteiros.

 ### **Representação de genes** 
   > Cada gene pode assumir dois tipos de valores:
   >
   > _**Cidades de 1 até N:**  Representam os índices das cidades a serem visitadas._
   >
   > _**Nós fictícios (dummy nodes):**  Representam separadores entre rotas de diferentes trabalhadores._
 
 O cromossomo é decifrado como múltiplas rotas, onde cada sequência entre dois nós fictícios correspondem a um trabalhador.

 Como:  
 `[1, 5, 3, 31, 2, 8, 32, 4, 6]`
 - Trabalhador 1 → [1, 5, 3]
 - Trabalhador 2 → [2, 8]
 - Trabalhador 3 → [4, 6]

### **Domínio dos valores** 

`N` = número de cidades

`K` = número de trabalhadores

Ou seja:

- Cidades → valores de `1` até `N`
- Dummy nodes → valores de `N+1` até `N+(K-1)`


### **Tamanho do cromossomo** 

`Tamanho = N + (K - 1)`

O tamanho do cromossomo garante que todas as cidades sejam visitadas exatamente uma vez e assegura a divisão das rotas entre os trabalhadores.


## _***Função de aptidão***_

A função de aptidão é definida como um problema de maximização com penalidades, onde as soluções inválidas recebem penalizações sérias.

### **Fórmula** 

```
    fitness = V 
              - penalidades 
              - (α × distância_total) 
              - (β × desvio_padrão)
```

### **Componente** 

- **Distância total:** Soma as distâncias percorridas por todos os trabalhadores. Tem o objetivo minimizar a distância percorrida.

- **Desvio padrão das rotas:** Mede o balanceamento da carga entre os trabalhadores. Tem como objetivo minimizar diferenças entre cargas de trabalho.

- **Penalidades:** 
  >`R4:` mínimo de cidades por trabalhador
  >
  >`R5:` máximo de cidades por trabalhador
  >
  >`R6:` diferença máxima entre trabalhadores
  >
  >`R7:` limite de distância por trabalhador

  As penalidades são calculadas proporcionalmente à violação. As demais restrições (R1 até R3) são validadas durante a execução do algoritmo, ou seja, todos os indivíduos as respeitam, não sendo necessário o cálculo de suas respectivas penalidades.

- **Parâmetros utilizados:** 
  >`V = 10000:` constante base
  >
  >`α = 1.0:` peso da distância
  >
  >`β = 3.0:` peso do balanceamento
  >
  >`penalty_multiplier = 5000` 


- **Justificativa dos pesos:** 
   O valor elevado de `V` garante que o fitness permaneça positivo. O peso `β > α` prioriza o **balanceamento das rotas**. Penalidades elevadas forçam o algoritmo a evitar soluções inválidas.


## _***Operadores***_

- **Seleção — Torneio** 
 
  >O método utilizado foi **Tournament Selection**, onde seleciona `k` indivíduos aleatórios e retorna o maior fitness. Suas principais características incluem a simples implementação, mantém pressão evolutiva e favorece soluções melhores sem eliminar diversidade.

- **Crossover — Order Crossover (OX)** 
 
  Outro método utilizado foi o Order Crossover onde tem o seguinte funcionamento:

  1. Seleciona dois pontos de corte
  2. Copia subsequência do primeiro pai
  3. Preenche com genes do segundo pai mantendo a ordem e excluindo aqueles iguais aos copiados do primeiro pai

  Esse metódo garante que nenhuma cidade saia duplicada ou 
  perdida e tem preservação parcial da estrutura das rotas.

- **Mutação** 
 
  Foi utilizado dois tipos:
  - **Insert (80%):** Move um gene para outra posição.
  - **Swap (20%):** Troca dois genes de posição.

- **Tratamento das restrições** 
  
  >Os operadores não garantem diretamente as retrições. Ao invés disso, elas permitem soluções inválidas e a função de aptidão penaliza essas soluções rigorosamente.
  >
  >A vantagem desse tratamento é a maior liberdade de exploração e evita complexidade nos operadores.


## _***Inicialização***_

A população inicial é gerada por uma abordagem híbrida:
  1. **Aleatória (95%)**
  >Os cromossomos são embaralhados aleatoriamente, garantindo diversidade.

  2. **Heurística gulosa (5%)**
  >É baseada na estratégia **Nearest Neighbor (Vizinho Mais Próximo)** onde seleciona a cidade inicial aleatória e sempre escolhe a cidade não visitada mais próxima.

- **Tratamento das restrições** 
  
  Algumas restriçoes são parcialmente respeitadas como o balanceamento inicial. As demais são tratadas pela função de aptidão.

## _***Critério de Parada***_
  
  O algotimo utiliza o número fixo de gerações. 
  ```
  Critério: execução até G gerações
  ```

  Com o critério de execução até `G` gerações, onde `G` é definido pelo usuário. Esse algotimo é simples de implementar e permite o controle direto do tempo de execução.

