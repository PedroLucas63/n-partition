#!/usr/bin/env python3
import argparse
import os
import re
import sys

import numpy as np
import pandas as pd

def find_cols(df):
    genetic_makespan_cols = [c for c in df.columns if re.match(r"Genetic.*_MaxGroupSum", c)]
    genetic_time_cols = [c for c in df.columns if re.match(r"Genetic.*_Time\(us\)", c)]
    genetic_makespan_cols.sort()
    genetic_time_cols.sort()
    return genetic_makespan_cols, genetic_time_cols

def safe_mean(arr):
    return float(np.mean(arr)) if len(arr) > 0 else float("nan")

def main():
    p = argparse.ArgumentParser(description="Gerar métricas e resumo de metaheurísticas a partir de um CSV de resultados.")
    p.add_argument("--input", "-i", required=True, help="Arquivo CSV de entrada (ex.: balanced-results2.csv)")
    p.add_argument("--outdir", "-o", required=True, help="Pasta de saída (será criada se não existir)")
    p.add_argument("--basename", "-b", required=True, help="Nome base para os arquivos de saída (ex.: balanced)")
    args = p.parse_args()

    input_path = args.input
    outdir = args.outdir
    basename = args.basename

    if not os.path.isfile(input_path):
        print(f"Arquivo de entrada não encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(outdir, exist_ok=True)

    df = pd.read_csv(input_path)

    # determina colunas
    genetic_makespan_cols, genetic_time_cols = find_cols(df)
    if not genetic_makespan_cols:
        raise RuntimeError("Nenhuma coluna do genético encontrada! Verifique o CSV.")

    # algoritmos simples
    algoritmos_simples = {
        "LS": ("LS_MaxGroupSum", "LS_Time(us)"),
        "LPT": ("LPT_MaxGroupSum", "LPT_Time(us)"),
        "MultiFit": ("MULTIFIT_MaxGroupSum", "MULTIFIT_Time(us)"),
        "CGA": ("CGA_MaxGroupSum", "CGA_Time(us)"),
        "SA": ("SA_MaxGroupSum", "SA_Time(us)")  # <--- ADICIONE ESTA LINHA    }
    }

    data = []
    genetic_all_errors = []
    genetic_all_times = []
    genetic_all_solutions = []

    cga_erros_indices = None

    optimal = df["OptimalMakespan"].values

    # Processar algoritmos simples
    for alg, (makespan_col, time_col) in algoritmos_simples.items():
        if makespan_col not in df.columns or time_col not in df.columns:
            # pula se não existir
            continue
        makespans = df[makespan_col].values
        tempos = df[time_col].values

        erro_pct = 100.0 * (makespans - optimal) / optimal
        solucoes_otimas = int(np.sum(makespans == optimal))

        linha = {
            "Algoritmo": alg,
            "Média Erro (%)": float(np.mean(erro_pct)),
            "Mediana Erro (%)": float(np.median(erro_pct)),
            "Desvio Padrão (%)": float(np.std(erro_pct)),
            "Erro Mínimo (%)": float(np.min(erro_pct)),
            "Erro Máximo (%)": float(np.max(erro_pct)),
            "Soluções Ótimas (instâncias)": int(solucoes_otimas),
            "Tempo Médio (us)": float(np.mean(tempos)),
            "Tempo Máx (us)": float(np.max(tempos)),
            "Tempo Mín (us)": float(np.min(tempos))
        }

        if alg == "CGA":
            cga_erros_indices = np.where(makespans != optimal)[0] + 1

        data.append(linha)

    # Processar genético (várias execuções)
    # conferindo pares
    if len(genetic_makespan_cols) != len(genetic_time_cols):
        # tenta emparelhar pelo número encontrado; avisa mas continua com o menor conjunto
        n = min(len(genetic_makespan_cols), len(genetic_time_cols))
        genetic_makespan_cols = genetic_makespan_cols[:n]
        genetic_time_cols = genetic_time_cols[:n]

    # coletar arrays: cada linha da lista corresponde a uma execução (coluna)
    for mcol, tcol in zip(genetic_makespan_cols, genetic_time_cols):
        makes = df[mcol].values
        times = df[tcol].values
        errors = 100.0 * (makes - optimal) / optimal
        sols = (makes == optimal)
        genetic_all_errors.append(errors)
        genetic_all_times.append(times)
        genetic_all_solutions.append(sols)

    genetic_all_errors = np.array(genetic_all_errors)      # shape: (runs, instances)
    genetic_all_times = np.array(genetic_all_times)
    genetic_all_solutions = np.array(genetic_all_solutions)

    genetic_mean_error = np.mean(genetic_all_errors, axis=0) if genetic_all_errors.size else np.array([])
    genetic_mean_time = np.mean(genetic_all_times, axis=0) if genetic_all_times.size else np.array([])
    genetic_mean_solutions = np.mean(genetic_all_solutions, axis=0) if genetic_all_solutions.size else np.array([])

    genetic_solutions_per_run = np.sum(genetic_all_solutions, axis=1) if genetic_all_solutions.size else np.array([])

    # adicionar linha resumo para Genetic
    data.append({
        "Algoritmo": f"Genetic (Média)",
        "Média Erro (%)": float(np.mean(genetic_mean_error)) if genetic_mean_error.size else float("nan"),
        "Mediana Erro (%)": float(np.median(genetic_mean_error)) if genetic_mean_error.size else float("nan"),
        "Desvio Padrão (%)": float(np.std(genetic_mean_error)) if genetic_mean_error.size else float("nan"),
        "Erro Mínimo (%)": float(np.min(genetic_mean_error)) if genetic_mean_error.size else float("nan"),
        "Erro Máximo (%)": float(np.max(genetic_mean_error)) if genetic_mean_error.size else float("nan"),
        "Soluções Ótimas (instâncias)": float(np.mean(genetic_solutions_per_run)) if genetic_solutions_per_run.size else float("nan"),
        "Tempo Médio (us)": float(np.mean(genetic_mean_time)) if genetic_mean_time.size else float("nan"),
        "Tempo Máx (us)": float(np.max(genetic_mean_time)) if genetic_mean_time.size else float("nan"),
        "Tempo Mín (us)": float(np.min(genetic_mean_time)) if genetic_mean_time.size else float("nan")
    })

    # salvar métricas gerais
    tabela_metricas = pd.DataFrame(data)
    metrics_out = os.path.join(outdir, f"{basename}-metrics.csv")
    tabela_metricas.to_csv(metrics_out, index=False)

    # ============================
    # Resumo específico das metaheurísticas
    # ============================
    meta_rows = []

    # --- Genetic (agregado) ---
    # ============================
    # Resumo específico da metaheurística (apenas Genetic)
    # ============================
    if genetic_all_errors.size:
        # Reconstruir makespans originais e tempos
        makes_matrix = np.vstack([df[c].values for c in genetic_makespan_cols])  # shape: (runs, instances)
        times_matrix = np.vstack([df[c].values for c in genetic_time_cols]) if genetic_time_cols else np.zeros_like(makes_matrix)
        
        # Afastamento médio das soluções encontradas para as melhores soluções conhecidas
        deviation_per_run = 100.0 * (makes_matrix - optimal) / optimal  # shape: (runs, instances)
        mean_deviation_per_run = np.mean(np.abs(deviation_per_run), axis=1)  # média por execução
        
        # Número de acertos (solução ótima) por execução
        num_optimal_per_run = np.sum(makes_matrix == optimal, axis=1)
        
        # Tempo máximo e mínimo entre todas execuções/instâncias
        max_time = float(np.max(times_matrix))
        min_time = float(np.min(times_matrix))
        
        # Maior e menor número de acertos em uma execução
        max_hits = int(np.max(num_optimal_per_run))
        min_hits = int(np.min(num_optimal_per_run))
        
        # Maior e menor distanciamento do ótimo em uma execução
        max_deviation = float(np.max(np.max(deviation_per_run, axis=1)))
        min_deviation = float(np.min(np.min(deviation_per_run, axis=1)))
        
        meta_summary = {
            "Metaheuristic": "Genetic",
            "NumRunsDetected": len(genetic_makespan_cols),
            "AvgDeviationFromBestKnown_pct": float(np.mean(mean_deviation_per_run)),
            "MaxExecutionTime_us": max_time,
            "MinExecutionTime_us": min_time,
            "MaxOptimalHitsInRun": max_hits,
            "MinOptimalHitsInRun": min_hits,
            "MaxDeviationInRun_pct": max_deviation,
            "MinDeviationInRun_pct": min_deviation
        }
        
        meta_df = pd.DataFrame([meta_summary])
        meta_out = os.path.join(outdir, f"{basename}-metaheuristics.csv")
        meta_df.to_csv(meta_out, index=False)

    # prints finais rápidos
    print("======================================")
    print(" ESTATÍSTICAS GERAIS DOS ALGORITMOS ")
    print("======================================\n")
    print(tabela_metricas.to_string(index=False))
    print("\n======================================")
    print(" RESUMO DAS EXECUÇÕES DO GENÉTICO ")
    print("======================================\n")
    print(f"Total de execuções detectadas: {len(genetic_makespan_cols)}")
    if genetic_all_times.size:
        print(f"Maior tempo (us): {np.max(genetic_all_times):.4f}")
        print(f"Menor tempo (us): {np.min(genetic_all_times):.4f}")
    print(f"\nArquivos gravados:\n - {metrics_out}\n - {meta_out}")

if __name__ == "__main__":
    main()
