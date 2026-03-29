# Estudo de Hiperparâmetros

Este documento foi gerado automaticamente através de testes empíricos do algoritmo genético.

| Experimento | População | Mutação | Melhor Fitness | Convergência (Ger.) | Violações |
| :--- | :---: | :---: | :---: | :---: | :---: |
| População Baixa + Mutação Baixa | 50 | 0.05 | 9485.32 | 1997 | 0 |
| População Baixa + Mutação Alta | 50 | 0.45 | 9529.14 | 385 | 0 |
| População Alta + Mutação Baixa | 200 | 0.05 | 9523.35 | 810 | 0 |
| População Alta + Mutação Alta | 200 | 0.45 | 9513.61 | 1851 | 0 |

## Gráficos de Convergência

### População Baixa + Mutação Baixa

```mermaid
xychart-beta
    title "Evolução do Fitness — pop=50, mut=0.05"
    x-axis "Geração" [0, 166, 332, 498, 664, 830, 996, 1162, 1328, 1494, 1660, 1826, 1992, 1999]
    y-axis "Fitness" 9406 --> 10000
    line [9406, 9434, 9434, 9443, 9443, 9443, 9446, 9449, 9452, 9468, 9478, 9480, 9484, 9485]
```

### População Baixa + Mutação Alta

```mermaid
xychart-beta
    title "Evolução do Fitness — pop=50, mut=0.45"
    x-axis "Geração" [0, 166, 332, 498, 664, 830, 996, 1162, 1328, 1494, 1660, 1826, 1992, 1999]
    y-axis "Fitness" 9376 --> 10000
    line [9376, 9485, 9528, 9529, 9529, 9529, 9529, 9529, 9529, 9529, 9529, 9529, 9529, 9529]
```

### População Alta + Mutação Baixa

```mermaid
xychart-beta
    title "Evolução do Fitness — pop=200, mut=0.05"
    x-axis "Geração" [0, 166, 332, 498, 664, 830, 996, 1162, 1328, 1494, 1660, 1826, 1992, 1999]
    y-axis "Fitness" 9437 --> 10000
    line [9437, 9509, 9521, 9523, 9523, 9523, 9523, 9523, 9523, 9523, 9523, 9523, 9523, 9523]
```

### População Alta + Mutação Alta

```mermaid
xychart-beta
    title "Evolução do Fitness — pop=200, mut=0.45"
    x-axis "Geração" [0, 166, 332, 498, 664, 830, 996, 1162, 1328, 1494, 1660, 1826, 1992, 1999]
    y-axis "Fitness" 9438 --> 10000
    line [9438, 9480, 9510, 9510, 9510, 9511, 9511, 9511, 9511, 9513, 9513, 9513, 9513, 9513]
```

