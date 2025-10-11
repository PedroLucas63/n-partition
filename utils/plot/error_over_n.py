# utils/plot_error_vs_n.py
def plot_error_vs_n(csv_file, imgs_dir):
    import pandas as pd
    import matplotlib.pyplot as plt
    import os

    df = pd.read_csv(csv_file)
    df["LS_Error(%)"] = 100 * (df["LS_MaxGroupSum"] / df["OptimalMakespan"] - 1)
    df["LPT_Error(%)"] = 100 * (df["LPT_MaxGroupSum"] / df["OptimalMakespan"] - 1)
    df["MULTIFIT_Error(%)"] = 100 * (df["MULTIFIT_MaxGroupSum"] / df["OptimalMakespan"] - 1)

    heuristics = {
        "LS": "LS_Error(%)",
        "LPT": "LPT_Error(%)",
        "MULTIFIT": "MULTIFIT_Error(%)"
    }

    imgs_dir = os.path.join(imgs_dir, "error_over_n")
    os.makedirs(imgs_dir, exist_ok=True)

    for algo, col in heuristics.items():
        plt.figure(figsize=(12,6))
        Ns = sorted(df["N"].unique())
        medians = [pd.Series(df[df["N"]==n][col].values).median() for n in Ns]
        mins = [df[df["N"]==n][col].min() for n in Ns]
        maxs = [df[df["N"]==n][col].max() for n in Ns]

        plt.fill_between(range(1, len(Ns)+1), mins, maxs, color='lightblue', alpha=0.3, label='Min-Max')
        plt.plot(range(1, len(Ns)+1), medians, color='blue', marker='o', linestyle='-', label='Mediana')

        plt.xlabel("Tamanho da instância (N)")
        plt.ylabel("Erro percentual (%)")
        plt.title(f"Erro percentual vs N - {algo}")
        plt.xticks(range(1, len(Ns)+1), Ns, rotation=45)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()

        output_file = os.path.join(imgs_dir, f"{algo}_error_vs_N.png")
        plt.savefig(output_file)
        plt.close()
