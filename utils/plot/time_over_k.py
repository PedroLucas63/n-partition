# utils/plot_time_vs_k.py

import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_time_vs_k(csv_file, imgs_dir):

    df = pd.read_csv(csv_file)

    # Lista de heurísticas e suas colunas de tempo
    heuristics = {
        "LS": "LS_Time(us)",
        "LPT": "LPT_Time(us)",
        "MULTIFIT": "MULTIFIT_Time(us)"
    }

    # Cria pasta específica para os gráficos
    output_dir = os.path.join(imgs_dir, "time_over_k")
    os.makedirs(output_dir, exist_ok=True)

    # Loop para cada heurística
    for algo, col in heuristics.items():
        plt.figure(figsize=(8,5))
        
        Ks = sorted(df["K"].unique())
        df_box = [df[df["K"]==k][col].values for k in Ks]
        plt.boxplot(df_box, labels=Ks)
        
        # Linha da média
        means = [df[df["K"]==k][col].mean() for k in Ks]
        plt.plot(range(1, len(means)+1), means, color='red', linestyle='--', marker='o', label='Média')
        
        plt.xlabel("Número de partições (K)")
        plt.ylabel("Tempo de execução (µs)")
        plt.title(f"Tempo de execução vs K - {algo}")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()
        
        # Salva a figura
        output_file = os.path.join(output_dir, f"{algo}_time_vs_K.png")
        plt.savefig(output_file)
        plt.close()
