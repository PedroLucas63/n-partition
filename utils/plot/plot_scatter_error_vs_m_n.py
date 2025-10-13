import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_scatter_error_vs_m_n(csv_file, imgs_dir):
    """
    Gera scatter plots do erro percentual vs N e vs K para LS, LPT e MULTIFIT.
    Salva em imgs_dir/scatter_error.
    """
    if not os.path.exists(csv_file):
        raise FileNotFoundError(csv_file)

    df = pd.read_csv(csv_file)

    # calcula erro percentual se ainda não existir
    if "LS_Error(%)" not in df.columns:
        df["LS_Error(%)"] = 100 * (df["LS_MaxGroupSum"] / df["OptimalMakespan"] - 1)
        df["LPT_Error(%)"] = 100 * (df["LPT_MaxGroupSum"] / df["OptimalMakespan"] - 1)
        df["MULTIFIT_Error(%)"] = 100 * (df["MULTIFIT_MaxGroupSum"] / df["OptimalMakespan"] - 1)

    output_dir = os.path.join(imgs_dir, "scatter_error")
    os.makedirs(output_dir, exist_ok=True)

    heuristics = {
        "LS": "LS_Error(%)",
        "LPT": "LPT_Error(%)",
        "MULTIFIT": "MULTIFIT_Error(%)"
    }

    for algo, col in heuristics.items():
        # --- Error vs N ---
        x = df["N"].values
        y = df[col].values

        # correlation
        if np.std(x) == 0 or np.std(y) == 0:
            corr = np.nan  # sem variação, correlação indefinida
        else:
            corr = np.corrcoef(x, y)[0, 1]


        plt.figure(figsize=(8,5))
        plt.scatter(x, y, alpha=0.6, s=30, edgecolors='k', linewidth=0.2)
        # linear fit
        plt.rcParams.update({
            'font.size': 16,         # Tamanho geral do texto
            'axes.titlesize': 16,    # Título dos eixos
            'axes.labelsize': 16,    # Rótulos dos eixos (x e y)
            'xtick.labelsize': 16,   # Tamanho dos ticks no eixo x
            'ytick.labelsize': 16,   # Tamanho dos ticks no eixo y
            'legend.fontsize': 16,   # Fonte das legendas
        })
               
        try:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            xs = np.linspace(x.min(), x.max(), 100)
            plt.plot(xs, p(xs), 'r--', linewidth=1.5, label=f"Tendência (slope={z[0]:.3g})")
        except Exception:
            pass

        plt.title(f"{algo} — Erro vs M (corr={corr:.3f})")
        plt.xlabel("M (tamanho da instância)")
        plt.ylabel("Erro (%)")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{algo}_error_vs_M_scatter.png"), dpi=150)
        plt.close()

        # --- Error vs K ---
        x = df["N"].values
        y = df[col].values
        corr = np.corrcoef(x, y)[0,1]

        plt.figure(figsize=(8,5))
        plt.scatter(x, y, alpha=0.6, s=30, edgecolors='k', linewidth=0.2)
        try:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            xs = np.linspace(x.min(), x.max(), 100)
            plt.plot(xs, p(xs), 'r--', linewidth=1.5, label=f"Tendência (slope={z[0]:.3g})")
        except Exception:
            pass

        plt.title(f"{algo} — Erro vs N (corr={corr:.3f})")
        plt.xlabel("N (número de partições)")
        plt.ylabel("Erro (%)")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{algo}_error_vs_N_scatter.png"), dpi=150)
        plt.close()
