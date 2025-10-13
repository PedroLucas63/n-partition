# utils/plot_error_vs_k.py

import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_error_vs_n(csv_file, imgs_dir):
    """
    Gera gráficos de erro percentual vs número de partições (N) para LS, LPT e MULTIFIT.
    Salva os gráficos na pasta imgs_dir/error_over_k.
    
    Args:
        csv_file (str): caminho do arquivo CSV com os resultados.
        imgs_dir (str): pasta base para salvar as imagens.
    """
    # Lê o CSV
    df = pd.read_csv(csv_file)

    # Calcula erro percentual em relação ao ótimo
    df["LS_Error(%)"] = 100 * (df["LS_MaxGroupSum"] / df["OptimalMakespan"] - 1)
    df["LPT_Error(%)"] = 100 * (df["LPT_MaxGroupSum"] / df["OptimalMakespan"] - 1)
    df["MULTIFIT_Error(%)"] = 100 * (df["MULTIFIT_MaxGroupSum"] / df["OptimalMakespan"] - 1)

    # Lista de heurísticas
    heuristics = {
        "LS": "LS_Error(%)",
        "LPT": "LPT_Error(%)",
        "MULTIFIT": "MULTIFIT_Error(%)"
    }

    # Cria pasta específica para os gráficos
    output_dir = os.path.join(imgs_dir, "boxplot_over_n")
    os.makedirs(output_dir, exist_ok=True)

    # Loop para gerar e salvar um gráfico por heurística
    for algo, col in heuristics.items():
        plt.figure(figsize=(8,5))
        plt.rcParams.update({
            'font.size': 16,         # Tamanho geral do texto
            'axes.titlesize': 16,    # Título dos eixos
            'axes.labelsize': 16,    # Rótulos dos eixos (x e y)
            'xtick.labelsize': 16,   # Tamanho dos ticks no eixo x
            'ytick.labelsize': 16,   # Tamanho dos ticks no eixo y
            'legend.fontsize': 16,   # Fonte das legendas
        })
                
        # Boxplot do erro em função de K
        Ks = sorted(df["N"].unique())
        df_box = [df[df["N"]==k][col].values for k in Ks]
        plt.boxplot(df_box, labels=Ks)
        
        # Linha da média
        means = [df[df["N"]==k][col].mean() for k in Ks]
        plt.plot(range(1, len(means)+1), means, color='red', linestyle='--', marker='o', label='Média')
        
        plt.xlabel("Número de partições (N)")
        plt.ylabel("Erro percentual (%)")
        plt.title(f"Erro percentual vs N - {algo}")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()
        
        # Salva a figura na pasta imgs
        output_file = os.path.join(output_dir, f"{algo}_error_vs_N.png")
        plt.savefig(output_file)
        plt.close()
