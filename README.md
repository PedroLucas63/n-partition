# N-Partition System

Este projeto implementa e analisa heurísticas aproximativas para o problema da **$n$-partição**, um problema NP-difícil com diversas aplicações práticas, como escalonamento de tarefas e balanceamento de carga. O sistema permite execução em **três linguagens**: C++, Java e Python.

---

## Linguagens suportadas

O sistema oferece implementações equivalentes em:

1. **C++**
   - Baseado em `Partition.hpp`, `ReadInstances.hpp` e algoritmos `LS`, `LPT` e `MULTIFIT`.
   - Compilação e execução via `CMake` ou `g++`.

2. **Java**
   - Classes organizadas em pacotes:
     - `experiment` → execução dos experimentos
     - `partition` → implementação das heurísticas
     - `utils` → leitura de instâncias e funções auxiliares
   - Compilação e execução via terminal ou IDEs como IntelliJ.

3. **Python**
   - Scripts organizados em `include/` e `utils/plot/`.
   - Dependências: `pandas`, `numpy`, `matplotlib`.
   - Execução direta via `python main.py`.

---

## Estrutura de pastas

```text
.
├───.idea
├───.vscode
├───cpp
│   ├───build
│   │   └───CMakeFiles
│   │       ├───3.28.3
│   │       │   └───CompilerIdCXX/tmp
│   │       ├───n-partition.dir/include
│   │       └───n-partition.dir/src
│   ├───include
│   └───src
├───instances
├───java
│   └───src
│       ├───experiment
│       ├───partition
│       └───utils
├───out/production/n-partition
│   ├───experiment
│   ├───partition
│   └───utils
├───python/include/__pycache__
├───results/imgs
│   ├───boxplot_over_n
│   ├───error_over_instances
│   ├───scatter_error
│   └───scatter_time
└───utils/plot/__pycache__
