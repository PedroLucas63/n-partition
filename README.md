# N-Partition Problem

![C++](https://img.shields.io/badge/C%2B%2B-17-blue) ![Python 3.13+](https://img.shields.io/badge/Python-3.13%2B-blue) 
<!-- ![Java](https://img.shields.io/badge/Java-17-blue) -->

Este projeto implementa e analisa heurísticas aproximativas para o problema da **$n$-partição**, um problema NP-difícil com diversas aplicações práticas, como escalonamento de tarefas e balanceamento de carga. O sistema permite execução em **três linguagens**: C++, Java e Python.

Realiza teste com base em três algoritmos aproximativos e um exato:

* **LS**: List Scheduling
* **LPT**: Longest Processing Time
* **MULTIFIT**: MultiFit Algorithm
* **CGA**: Complete Greedy Algorithm


---

## Estrutura Geral 

```text
.
├───.idea
├───.vscode
├───cpp
│   ├───include
│   └───src
├───instances
├───java
│   └───src
│       ├───experiment
│       ├───partition
│       └───utils
├───python/include/
├───results/imgs
└───utils/plot/
```

---
### Pré‑requisitos

* **C++17** ou superior (GCC, Clang, MSVC)
* **CMake ≥ 3.11.2**
* **Java 17** ou superior
* **Python ≥ 3.13**

### Clonar o repositório

```bash
git clone https://github.com/PedroLucas63/n-partition.git
cd n-partition
```

## 🚀 Instruções de Execução


### 1. Gerar Instâncias de Teste

Gere as instâncias de dados que serão usadas por todas as implementações. As instâncias serão salvas em 'instances/'.

Comando:
```bash
python .\utils\generate-instances.py
```

### 2.1. Executar Testes em C++

Certifique-se de ter o **CMake** instalado. A execução irá compilar o código e rodar os testes.

```bash
cd cpp
cmake -S . -B build
cmake --build build
./build/n-partition
```

### 2.2. Executar Testes em Python

Navegue para o diretório de Python e execute o arquivo principal.

```bash
cd python
python main.py
```

### 2.3. Executar Testes em Java

```bash
cd java
javac -d out/production/n-partition src/partition/*.java src/experiment/*.java src/utils/*.java src/Main.java
java -cp out/production/n-partition Main
```

### 3. Gerar Gráficos

#### Ambiente Python (opcional, para visualização)

```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Para sair, basta digitar:

```bash
deactivate
```


> `requirements.txt` inclui:
>
> ```text
> pandas
> matplotlib
> numpy
> ```


Utilize este script para processar os resultados CSV e gerar os gráficos comparativos.

```bash
python .\utils\graphs.py
```

### 4. Calcular Métricas

Calcule métricas de desempenho e erro a partir dos resultados.

```bash
python .\utils\metrics.py
```

### 5. Resultados

Todos os arquivos gerados (gráficos, métricas e resultados brutos) estarão disponíveis na pasta 'results/':

```text
results/
├── imgs                   # Gráficos (3D, Acurácia, erro, score)
│   ├── balanced
│   └── random
├── balanced-metrics.csv   # Métricas gerais (instâncias balanceadas)
├── balanced-results.csv   # Resultados das execuções (instâncias balanceadas)
├── random-metrics.csv     # Métricas gerais (instâncias aleatórias)
└── random-results.csv     # Resultados das execuções (instâncias aleatórias)
```


## License 📄

MIT License. Veja [LICENSE](LICENSE) para detalhes.

## Contact 📧

Feito com ❤️ por Pedro Lucas e Gabriel Victor

Email: [g.victor.silva01@gmail.com](mailto:g.victor.silva01@gmail.com) e [pedrolucas.jsrn@gmail.com](mailto:pedrolucas.jsrn@gmail.com)
