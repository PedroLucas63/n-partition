import pandas as pd
import numpy as np

# Ler o CSV
import os
import pandas as pd

# Caminho do diretório atual do script
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))

# Caminho completo para o CSV
csv_path = os.path.join(project_dir, "random-results.csv")

df = pd.read_csv(csv_path)

# Lista de algoritmos e colunas correspondentes
algoritmos = {
    "LS": ("LS_MaxGroupSum", "LS_Time(us)"),
    "LPT": ("LPT_MaxGroupSum", "LPT_Time(us)"),
    "MultiFit": ("MULTIFIT_MaxGroupSum", "MULTIFIT_Time(us)"),
    "CGA": ("CGA_MaxGroupSum", "CGA_Time(us)"),
    "Genetic": ("Genetic_MaxGroupSum", "Genetic_Time(us)")
}

data = []

for alg, (makespan_col, time_col) in algoritmos.items():
    makespans = df[makespan_col].values
    tempos = df[time_col].values  
    optimal = df["OptimalMakespan"].values
    
    # Erro percentual
    erro_pct = 100 * (makespans - optimal) / optimal
    
    # Número de soluções ótimas
    solucoes_otimas = np.sum(makespans == optimal)
    
    # Estatísticas
    linha = {
        "Algoritmo": alg,
        "Média Erro (%)": np.mean(erro_pct),
        "Mediana Erro (%)": np.median(erro_pct),
        "Desvio Padrão (%)": np.std(erro_pct),
        "Erro Mínimo (%)": np.min(erro_pct),
        "Erro Máximo (%)": np.max(erro_pct),
        "Soluções Ótimas": solucoes_otimas,
        "Tempo Médio (us)": np.mean(tempos),
        "Tempo Máx (us)": np.max(tempos),
        "Tempo Mín (us)": np.min(tempos)
    }
    data.append(linha)

# Criar DataFrame final
tabela_metricas = pd.DataFrame(data)

# Salvar CSV
output_path = os.path.join(project_dir, "random-metrics.csv")

tabela_metricas.to_csv(output_path, index=False)

# Mostrar na tela
print(tabela_metricas)
