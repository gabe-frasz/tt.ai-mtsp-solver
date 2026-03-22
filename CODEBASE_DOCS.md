# Documentação do Código-Fonte

Esta é uma documentação simplificada do código-fonte, detalhando cada arquivo, classe e método para que você possa entender facilmente como o solucionador mTSP (Multiple Traveling Salesperson Problem - Problema dos Múltiplos Caixeiros Viajantes) funciona, sem precisar de um conhecimento profundo em algoritmos complexos.

### 1. `main.py`
Este é o ponto de entrada do programa, onde tudo se conecta.
* **`main()`**: A função principal que inicia o programa. Ela carrega a configuração, inicializa o problema com coordenadas fixas de cidades e do depósito (depot), configura o Algoritmo Genético (Genetic Algorithm - GA), executa-o e, por fim, imprime as melhores rotas encontradas e suas estatísticas.

---

### 2. `src/utils.py`
Contém utilitários matemáticos úteis usados em todo o projeto.
* **`Utils` (Classe)**: Uma coleção de ferramentas auxiliares.
  * **`calc_euclidean_distance(coord1, coord2)`**: Calcula a distância em linha reta (Euclidiana) entre dois pontos em um mapa 2D.
  * **`calc_std_dev(data)`**: Calcula o desvio padrão (standard deviation). Isso é usado para verificar se a carga de trabalho está balanceada entre os diferentes trabalhadores (por exemplo, se um trabalhador viaja 100 milhas e outro viaja 10, o desvio padrão é alto, o que queremos evitar).

---

### 3. `src/parser.py`
Lida com a forma como o programa recebe configurações e opções do usuário.
* **`_load_config_file(filepath)`**: Um método auxiliar que lê as configurações de um arquivo `.json` ou `.yaml`.
* **`get_config()`**: O principal construtor de configurações. Ele verifica as configurações padrão, quaisquer arquivos de configuração fornecidos e argumentos de linha de comando (como `-p 100` para o tamanho da população). Ele prioriza os argumentos de linha de comando sobre os arquivos, e os arquivos sobre os padrões.

---

### 4. `src/genetic_algorithm.py`
O "cérebro" da operação. Ele usa conceitos inspirados na evolução para melhorar as soluções ao longo do tempo.
* **`GeneticAlgorithm` (Classe)**: O motor que executa o processo de evolução.
  * **`__init__(...)`**: Configura o algoritmo com regras definidas pelo usuário, como quantas soluções existem ao mesmo tempo (`population`), quantas rodadas executar (`generations`), e com que frequência misturar ou alterar suas características (taxas de `crossover`/`mutation`).
  * **`run(problem)`**: O loop principal. Ele gera um lote inicial de soluções aleatórias e repete um ciclo: avalia-as, escolhe as melhores, mistura suas características (`crossover`), altera algumas aleatoriamente (`mutate`), e cria uma nova geração até que o número máximo de rodadas seja atingido.
  * **`_tournament_selection(evaluated_population, k)`**: Uma maneira de escolher os pais para a próxima geração. Ele seleciona aleatoriamente `k` soluções do grupo, as faz "competir" entre si, e aquela com a melhor pontuação ganha o direito de se reproduzir.

---

### 5. `src/mtsp.py`
Define as regras específicas do seu Problema dos Múltiplos Caixeiros Viajantes.
* **`MTSP` (Classe)**: Representa o mapa, os trabalhadores e as regras que eles devem seguir.
  * **`__init__(...)`**: Configura o mapa recebendo as coordenadas das cidades, o depósito (ponto de partida/chegada), e o número de trabalhadores. Ele também pré-calcula as distâncias entre todas as cidades para acelerar o programa.
  * **`initialize(population_size)`**: Cria a primeira geração de soluções. Ela faz com que 95% delas sejam completamente aleatórias, mas inclui 5% de palpites "inteligentes" (greedy) para dar ao algoritmo um bom ponto de partida.
  * **`fitness(chromosome)`**: **O avaliador mais importante.** Ele pontua uma solução (um "cromossomo") com base em três coisas:
    1. Distância total (quanto menor, melhor).
    2. Equilíbrio da carga de trabalho (todos os trabalhadores devem fazer aproximadamente a mesma quantidade de trabalho).
    3. Violações de regras (penaliza fortemente a pontuação se um trabalhador visitar muitas/poucas cidades ou viajar muito longe).
  * **`crossover(parent1, parent2)`**: Combina as rotas de duas boas soluções para criar um descendente. Ele usa um método específico (Order Crossover) que garante que nenhuma cidade seja acidentalmente duplicada ou deixada de fora.
  * **`mutate(chromosome)`**: Altera aleatoriamente uma rota para introduzir novas ideias. Pode trocar a posição de duas cidades ou mover uma cidade para um ponto completamente diferente na rota.
  * **`get_solution_from_individual(individual)`**: Traduz a versão de código bruto de uma solução de volta para uma lista legível para humanos de rotas reais com distâncias e pontos de coordenadas.
  * **`_get_violations_report(chromosome)`**: Verifica se uma solução quebra alguma regra de negócio (como trabalhar por muito tempo) e a formata em uma string simples para o usuário ler.
  * **`_build_distance_matrix()`**: Pré-computa a distância de cada ponto para todos os outros pontos apenas uma vez, para que o programa não tenha que fazer a mesma matemática milhões de vezes depois.
  * **`_generate_greedy_chromosome()`**: Cria uma solução de "palpite inteligente" apenas atribuindo a cidade não visitada mais próxima a um trabalhador até que ele esteja cheio.
  * **`_decode_chromosome(chromosome)`**: No código, uma solução é apenas uma longa lista de números. Este método divide essa única lista em listas separadas, atribuindo um grupo específico de cidades a cada trabalhador individual.

* **`MTSPLogger` (Classe)**: 
  * **`print_header()` / `log(...)`**: Simplesmente desenha a tabela de texto no terminal para que você possa observar o algoritmo melhorar as rotas em tempo real conforme as gerações passam.
