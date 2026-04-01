# Multiple Traveling Salesperson Problem (mTSP)

The mTSP is an extension of the classic Traveling Salesperson Problem
where multiple salespeople must visit a set of cities,
starting and returning to a central depot,
ensuring all cities are visited exactly once while optimizing for distance and balance.

## Configuration

### Fields

- `num_workers`: Number of workers.
- `depot`: Coordinates of the depot.
- `cities`: List of cities, each represented by a list of coordinates.

### Example

```yaml
problem_name: "mtsp"

problem_config:
  num_workers: 3
  depot: [30, 30]
  cities:
    - [5, 10]
    - [15, 25]
    - [30, 5]
    # ... more cities
```

---

## _***Chromosome***_

The solution is represented as a 1D integer vector.

### **Gene Representation**

> Each gene can take two types of values:
>
> _**Cities (1 to N):** Represent the indices of the cities to be visited._
>
> _**Dummy nodes:** Represent separators between routes of different workers._

The chromosome is decoded as multiple routes, where each sequence between two dummy nodes corresponds to a worker.

Example with 7 cities and 3 workers: `[1, 5, 3, 8, 2, 7, 9, 4, 6]`
- Worker 1 → [1, 5, 3]
- Worker 2 → [2, 7]
- Worker 3 → [4, 6]

### **Domain of Values**

`N` = number of cities
`K` = number of workers

- Cities → values from `1` to `N`
- Dummy nodes → values from `N+1` to `N+(K-1)`

### **Chromosome Size**

`Size = N + (K - 1)`

---

## _***Fitness Function***_

Defined as a maximization problem with penalties for invalid solutions.

### **Formula**

```
fitness = V - penalties - (α × total_distance) - (β × standard_deviation)
```

### **Components**

- **Total Distance:** Sum of distances traveled by all workers.
- **Standard Deviation:** Measures the load balance between workers.
- **Penalties:** Applied for violations of minimum/maximum cities per worker, balance differences, and distance limits.
- **α:** Total distance weight.
- **β:** Standard deviation weight.

---

## _***Operators***_

- **Selection:** Tournament Selection.
- **Crossover:** Order Crossover (OX) to preserve route structures without duplication.
- **Mutation:** Insert (80%) and Swap (20%).

---

## _***Initialization***_

Hybrid approach combining:
1. **Random (95%):** Ensures diversity.
2. **Greedy Heuristic (5%):** Based on Nearest Neighbor to provide a strong starting point.

---

## _***Stop Criterion***_

The algorithm runs for a fixed number of generations `G` as defined in the configuration.
