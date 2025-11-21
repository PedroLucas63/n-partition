import pandas as pd
import numpy as np
import os
import re

# Caminho do diretório atual do script
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp"))

# Caminho completo para o CSV
csv_path = os.path.join(project_dir, "balanced-results2.csv")

df = pd.read_csv(csv_path)

# Algoritmos simples (1 coluna por algoritmo)
algoritmos_simples = {
    "LS": ("LS_MaxGroupSum", "LS_Time(us)"),
    "LPT": ("LPT_MaxGroupSum", "LPT_Time(us)"),
    "MultiFit": ("MULTIFIT_MaxGroupSum", "MULTIFIT_Time(us)"),
    "CGA": ("CGA_MaxGroupSum", "CGA_Time(us)")
}

# -------------------------
# 🔍 Detectar colunas do genético automaticamente
# -------------------------
genetic_makespan_cols = [c for c in df.columns if re.match(r"Genetic.*_MaxGroupSum", c)]
genetic_time_cols = [c for c in df.columns if re.match(r"Genetic.*_Time\(us\)", c)]

if not genetic_makespan_cols:
    raise RuntimeError("Nenhuma coluna do genético encontrada! Verifique o CSV.")

genetic_makespan_cols.sort()
genetic_time_cols.sort()

# -------------------------
# 📊 Estatísticas gerais
# -------------------------
data = []

# Para cálculos detalhados do genético
genetic_all_errors = []
genetic_all_times = []
genetic_all_solutions = []

# Para armazenar instâncias em que o CGA errou
cga_erros_indices = None

# Processar algoritmos simples (LS, LPT, MultiFit, CGA)
for alg, (makespan_col, time_col) in algoritmos_simples.items():
    makespans = df[makespan_col].values
    tempos = df[time_col].values
    optimal = df["OptimalMakespan"].values

    erro_pct = 100 * (makespans - optimal) / optimal
    solucoes_otimas = np.sum(makespans == optimal)

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

    if alg == "CGA":
        cga_erros_indices = np.where(makespans != optimal)[0] + 1

    data.append(linha)

# -------------------------
# 📊 Estatísticas do genético (média das execuções)
# -------------------------

optimal = df["OptimalMakespan"].values

for mcol, tcol in zip(genetic_makespan_cols, genetic_time_cols):
    makes = df[mcol].values
    times = df[tcol].values

    errors = 100 * (makes - optimal) / optimal
    sols = (makes == optimal)

    genetic_all_errors.append(errors)
    genetic_all_times.append(times)
    genetic_all_solutions.append(sols)

# Converter listas para arrays
genetic_all_errors = np.array(genetic_all_errors)
genetic_all_times = np.array(genetic_all_times)
genetic_all_solutions = np.array(genetic_all_solutions)

# Média das execuções
genetic_mean_error = np.mean(genetic_all_errors, axis=0)
genetic_mean_time = np.mean(genetic_all_times, axis=0)
genetic_mean_solutions = np.mean(genetic_all_solutions, axis=0)

# Média de soluções ótimas por execução
genetic_solutions_per_run = np.sum(genetic_all_solutions, axis=1) 

data.append({
    "Algoritmo": "Genetic (Média)",
    "Média Erro (%)": np.mean(genetic_mean_error),
    "Mediana Erro (%)": np.median(genetic_mean_error),
    "Desvio Padrão (%)": np.std(genetic_mean_error),
    "Erro Mínimo (%)": np.min(genetic_mean_error),
    "Erro Máximo (%)": np.max(genetic_mean_error),
    "Soluções Ótimas": np.mean(genetic_solutions_per_run),
    "Tempo Médio (us)": np.mean(genetic_mean_time),
    "Tempo Máx (us)": np.max(genetic_mean_time),
    "Tempo Mín (us)": np.min(genetic_mean_time)
})

# Criar DataFrame final e salvar
tabela_metricas = pd.DataFrame(data)
tabela_metricas.to_csv(os.path.join(project_dir, "balanced-metrics2.csv"), index=False)

# ============================
# 📌 1. Estatísticas gerais
# ============================
print("======================================")
print(" ESTATÍSTICAS GERAIS DOS ALGORITMOS ")
print("======================================\n")
print(tabela_metricas)

# ============================
# 📌 2. Resumo das execuções do genético
# ============================
print("\n======================================")
print(" RESUMO DAS EXECUÇÕES DO GENÉTICO ")
print("======================================\n")

print(f"Total de execuções detectadas: {len(genetic_makespan_cols)}\n")

print(f"MELHOR nº de soluções ótimas: {np.max(np.sum(genetic_all_solutions, axis=1))}")
print(f"PIOR nº de soluções ótimas:   {np.min(np.sum(genetic_all_solutions, axis=1))}\n")

print(f"Maior tempo (us): {np.max(genetic_all_times):.4f}")
print(f"Menor tempo (us): {np.min(genetic_all_times):.4f}")