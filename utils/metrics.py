#!/usr/bin/env python3
import argparse
import os
import re
import sys

import numpy as np
import pandas as pd

def find_meta_prefixes(df, exclude_prefixes=None):
    """
    Detecta prefixes de metaheurísticas presentes nas colunas do DataFrame.
    Retorna um dicionário: { prefix: (makespan_cols, time_cols) }.
    exclude_prefixes: lista de prefixes a ignorar (ex.: algoritmos simples).
    """
    meta = {}
    # encontra colunas de makespan
    for c in df.columns:
        m = re.match(r"(.+?)_.*_MaxGroupSum$", c)
        if m:
            p = m.group(1)
            if exclude_prefixes and p in exclude_prefixes:
                continue
            meta.setdefault(p, {"makes": [], "times": []})
            meta[p]["makes"].append(c)
    # encontra colunas de tempo
    for c in df.columns:
        m = re.match(r"(.+?)_.*_Time\(us\)$", c)
        if m:
            p = m.group(1)
            if exclude_prefixes and p in exclude_prefixes:
                continue
            meta.setdefault(p, {"makes": [], "times": []})
            meta[p]["times"].append(c)
    # ordenar para consistência
    for p in list(meta.keys()):
        meta[p]["makes"].sort()
        meta[p]["times"].sort()
    return meta

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

    # algoritmos simples
    algoritmos_simples = {
        "LS": ("LS_MaxGroupSum", "LS_Time(us)"),
        "LPT": ("LPT_MaxGroupSum", "LPT_Time(us)"),
        "MultiFit": ("MULTIFIT_MaxGroupSum", "MULTIFIT_Time(us)"),
        "CGA": ("CGA_MaxGroupSum", "CGA_Time(us)"),
    }

    data = []
    # variáveis relacionadas ao CGA (mantive comportamento antigo)
    cga_erros_indices = None

    if "OptimalMakespan" not in df.columns:
        raise RuntimeError("Coluna 'OptimalMakespan' não encontrada! Verifique o CSV.")

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

    # -----------------------------
    # Detectar metaheurísticas (genérico)
    # -----------------------------
    # excluir prefixes correspondentes aos algoritmos simples
    exclude_prefixes = []
    for _, (makes_col, _) in algoritmos_simples.items():
        # prefix é a parte antes do primeiro underscore
        prefix = makes_col.split('_', 1)[0]
        exclude_prefixes.append(prefix)

    meta_prefixes = find_meta_prefixes(df, exclude_prefixes=exclude_prefixes)

    if not meta_prefixes:
        raise RuntimeError("Nenhuma coluna de metaheurística encontrada! Verifique o CSV.")

    # Path de saída do meta CSV (mesma variável usada depois)
    meta_out = os.path.join(outdir, f"{basename}-metaheuristics.csv")

    meta_rows = []

    # Processar cada metaheurística detectada (mesma lógica que você tinha para Genetic)
    for prefix, cols in meta_prefixes.items():
        makespan_cols = cols.get("makes", [])
        time_cols = cols.get("times", [])

        # conferindo pares: mantém comportamento original
        if len(makespan_cols) != len(time_cols):
            n = min(len(makespan_cols), len(time_cols))
            makespan_cols = makespan_cols[:n]
            time_cols = time_cols[:n]

        # coletar arrays: cada linha da lista corresponde a uma execução (coluna)
        all_errors = []
        all_times = []
        all_sols = []

        for mcol, tcol in zip(makespan_cols, time_cols):
            makes = df[mcol].values
            times = df[tcol].values
            errors = 100.0 * (makes - optimal) / optimal
            sols = (makes == optimal)
            all_errors.append(errors)
            all_times.append(times)
            all_sols.append(sols)

        all_errors = np.array(all_errors)      # shape: (runs, instances)
        all_times = np.array(all_times)
        all_sols = np.array(all_sols)

        mean_error = np.mean(all_errors, axis=0) if all_errors.size else np.array([])
        mean_time = np.mean(all_times, axis=0) if all_times.size else np.array([])
        mean_solutions = np.mean(all_sols, axis=0) if all_sols.size else np.array([])

        solutions_per_run = np.sum(all_sols, axis=1) if all_sols.size else np.array([])

        # adicionar linha resumo (como fazia para Genetic)
        data.append({
            "Algoritmo": f"{prefix} (Média)",
            "Média Erro (%)": float(np.mean(mean_error)) if mean_error.size else float("nan"),
            "Mediana Erro (%)": float(np.median(mean_error)) if mean_error.size else float("nan"),
            "Desvio Padrão (%)": float(np.std(mean_error)) if mean_error.size else float("nan"),
            "Erro Mínimo (%)": float(np.min(mean_error)) if mean_error.size else float("nan"),
            "Erro Máximo (%)": float(np.max(mean_error)) if mean_error.size else float("nan"),
            "Soluções Ótimas (instâncias)": float(np.mean(solutions_per_run)) if solutions_per_run.size else float("nan"),
            "Tempo Médio (us)": float(np.mean(mean_time)) if mean_time.size else float("nan"),
            "Tempo Máx (us)": float(np.max(mean_time)) if mean_time.size else float("nan"),
            "Tempo Mín (us)": float(np.min(mean_time)) if mean_time.size else float("nan")
        })

        # === Resumo específico da metaheurística (mesma lógica que tinha) ===
        if all_errors.size:
            makes_matrix = np.vstack([df[c].values for c in makespan_cols])  # (runs, instances)
            times_matrix = np.vstack([df[c].values for c in time_cols]) if time_cols else np.zeros_like(makes_matrix)

            deviation_per_run = 100.0 * (makes_matrix - optimal) / optimal  # (runs, instances)
            mean_deviation_per_run = np.mean(np.abs(deviation_per_run), axis=1)  # média por execução

            num_optimal_per_run = np.sum(makes_matrix == optimal, axis=1)

            max_time = float(np.max(times_matrix))
            min_time = float(np.min(times_matrix))

            max_hits = int(np.max(num_optimal_per_run))
            min_hits = int(np.min(num_optimal_per_run))

            max_deviation = float(np.max(np.max(deviation_per_run, axis=1)))
            min_deviation = float(np.min(np.min(deviation_per_run, axis=1)))

            meta_summary = {
                "Metaheuristic": prefix,
                "NumRunsDetected": len(makespan_cols),
                "AvgDeviationFromBestKnown_pct": float(np.mean(mean_deviation_per_run)),
                "MaxExecutionTime_us": max_time,
                "MinExecutionTime_us": min_time,
                "MaxOptimalHitsInRun": max_hits,
                "MinOptimalHitsInRun": min_hits,
                "MaxDeviationInRun_pct": max_deviation,
                "MinDeviationInRun_pct": min_deviation
            }

            meta_rows.append(meta_summary)

    # salvar métricas gerais
    tabela_metricas = pd.DataFrame(data)
    metrics_out = os.path.join(outdir, f"{basename}-metrics.csv")
    tabela_metricas.to_csv(metrics_out, index=False)

    # salvar resumo de metaheurísticas
    if meta_rows:
        meta_df = pd.DataFrame(meta_rows)
        meta_df.to_csv(meta_out, index=False)
    else:
        # manter compatibilidade: cria arquivo vazio com colunas esperadas
        meta_df = pd.DataFrame(columns=[
            "Metaheuristic", "NumRunsDetected",
            "AvgDeviationFromBestKnown_pct", "MaxExecutionTime_us", "MinExecutionTime_us",
            "MaxOptimalHitsInRun", "MinOptimalHitsInRun",
            "MaxDeviationInRun_pct", "MinDeviationInRun_pct"
        ])
        meta_df.to_csv(meta_out, index=False)

    # prints finais rápidos (manter formato original, ajustando para genérico)
    print("======================================")
    print(" ESTATÍSTICAS GERAIS DOS ALGORITMOS ")
    print("======================================\n")
    print(tabela_metricas.to_string(index=False))
    print("\n======================================")
    print(" RESUMO DAS EXECUÇÕES DAS METAHEURÍSTICAS ")
    print("======================================\n")
    if meta_rows:
        print(pd.DataFrame(meta_rows).to_string(index=False))
    else:
        print("[AVISO] Nenhuma metaheurística resumida.")

    # Informações adicionais (soma das runs detectadas)
    total_runs = sum(r.get("NumRunsDetected", 0) for r in meta_rows)
    print(f"\nTotal de execuções detectadas (soma das runs por metaheurística): {total_runs}")

    # Se existia anteriormente a variável genetic_* usada nos prints finais, manter saída similar:
    # imprimir total de execuções detectadas do primeiro prefix (se quiser mostrar por prefix, já imprimimos acima)
    first_prefix = next(iter(meta_prefixes.keys()))
    first_makes = meta_prefixes[first_prefix]["makes"]
    print(f"\nArquivos gravados:\n - {metrics_out}\n - {meta_out}")

if __name__ == "__main__":
    main()
