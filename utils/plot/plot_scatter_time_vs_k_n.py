# utils/plot_scatter_time_vs_k_n.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_scatter_time_vs_k_n(csv_file, imgs_dir):
    """
    Gera gráficos de dispersão (scatter) mostrando o tempo de execução
    em função de K e N para as heurísticas LS, LPT e MULTIFIT.
    Também calcula e exibe o coeficiente de correlação de Pearson.

    Args:
        csv_file (str): Caminho do arquivo CSV com resultados.
        imgs_dir (str): Pasta base para salvar as imagens.
    """
    # Verifica se o arquivo existe
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"O arquivo {csv_file} não foi encontrado!")

    # Lê o CSV
    df = pd.read_csv(csv_file)

    # Cria pasta de destino
    output_dir = os.path.join(imgs_dir, "scatter_time")
    os.makedirs(output_dir, exist_ok=True)

    # Define as heurísticas e colunas de tempo
    heuristics = {
        "LS": "LS_Time(us)",
        "LPT": "LPT_Time(us)",
        "MULTIFIT": "MULTIFIT_Time(us)"
    }

    # Gera gráficos para cada heurística
    for algo, time_col in heuristics.items():
        # ---- SCATTER: Tempo vs K ----
        plt.figure(figsize=(8, 5))
        plt.scatter(df["K"], df[time_col], alpha=0.7, edgecolors='k', color='tab:blue')

        plt.rcParams.update({
            'font.size': 16,         # Tamanho geral do texto
            'axes.titlesize': 16,    # Título dos eixos
            'axes.labelsize': 16,    # Rótulos dos eixos (x e y)
            'xtick.labelsize': 16,   # Tamanho dos ticks no eixo x
            'ytick.labelsize': 16,   # Tamanho dos ticks no eixo y
            'legend.fontsize': 16,   # Fonte das legendas
        })
               

        # Regressão linear para tendência
        z = np.polyfit(df["K"], df[time_col], 1)
        p = np.poly1d(z)
        plt.plot(df["K"], p(df["K"]), "r--", label="Tendência linear")

        # Correlação
        corr_k = df["K"].corr(df[time_col])
        plt.title(f"{algo} — Tempo vs K (correlação: {corr_k:.3f})")
        plt.xlabel("Número de partições (K)")
        plt.ylabel("Tempo de execução (µs)")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()

        # Salva figura
        plt.savefig(os.path.join(output_dir, f"{algo}_time_vs_K_scatter.png"))
        plt.close()

        # ---- SCATTER: Tempo vs N ----
        plt.figure(figsize=(8, 5))
        plt.scatter(df["N"], df[time_col], alpha=0.7, edgecolors='k', color='tab:green')

        # Regressão linear
        z = np.polyfit(df["N"], df[time_col], 1)
        p = np.poly1d(z)
        plt.plot(df["N"], p(df["N"]), "r--", label="Tendência linear")

        # Correlação
        corr_n = df["N"].corr(df[time_col])
        plt.title(f"{algo} — Tempo vs N (correlação: {corr_n:.3f})")
        plt.xlabel("Tamanho da instância (N)")
        plt.ylabel("Tempo de execução (µs)")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()

        # Salva figura
        plt.savefig(os.path.join(output_dir, f"{algo}_time_vs_N_scatter.png"))
        plt.close()
