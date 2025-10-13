# utils/plot_scatter_time_vs_n_m.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_scatter_time_vs_n_m(csv_file, imgs_dir):
    """
    Generates scatter plots showing execution time as a function of:
        - N: number of partitions (previously K)
        - M: instance size (previously N)
    for the heuristics LS, LPT, and MULTIFIT.
    
    Also computes and displays the Pearson correlation coefficient.

    Args:
        csv_file (str): Path to the CSV file containing results.
        imgs_dir (str): Directory where output images will be saved.
    """
    # Check if the input CSV exists
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"The file {csv_file} was not found!")

    # Read the CSV results file
    df = pd.read_csv(csv_file)

    # Create output directory for scatter plots
    output_dir = os.path.join(imgs_dir, "scatter_time")
    os.makedirs(output_dir, exist_ok=True)

    # Define heuristics and corresponding time columns
    heuristics = {
        "LS": "LS_Time(us)",
        "LPT": "LPT_Time(us)",
        "MULTIFIT": "MULTIFIT_Time(us)"
    }

    # Generate scatter plots for each heuristic
    for algo, time_col in heuristics.items():
        # ==========================================================
        # SCATTER PLOT: Execution Time vs N (number of partitions)
        # ==========================================================
        plt.figure(figsize=(8, 5))
        plt.scatter(df["N"], df[time_col], alpha=0.7, edgecolors='k', color='tab:blue')

        # Configure visual style
        plt.rcParams.update({
            'font.size': 16,
            'axes.titlesize': 16,
            'axes.labelsize': 16,
            'xtick.labelsize': 16,
            'ytick.labelsize': 16,
            'legend.fontsize': 16,
        })

        # Compute linear regression (trend line)
        z = np.polyfit(df["N"], df[time_col], 1)
        p = np.poly1d(z)
        plt.plot(df["N"], p(df["N"]), "r--", label="Linear trend")

        # Compute correlation between N and execution time
        corr_n = df["N"].corr(df[time_col])
        plt.title(f"{algo} — Time vs N (correlation: {corr_n:.3f})")
        plt.xlabel("Number of partitions (N)")
        plt.ylabel("Execution time (µs)")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()

        # Save figure (Time vs N)
        plt.savefig(os.path.join(output_dir, f"{algo}_time_vs_N_scatter.png"))
        plt.close()

        # ==========================================================
        # SCATTER PLOT: Execution Time vs M (instance size)
        # ==========================================================
        plt.figure(figsize=(8, 5))
        plt.scatter(df["M"], df[time_col], alpha=0.7, edgecolors='k', color='tab:green')

        # Compute linear regression for M
        z = np.polyfit(df["M"], df[time_col], 1)
        p = np.poly1d(z)
        plt.plot(df["M"], p(df["M"]), "r--", label="Linear trend")

        # Compute correlation between M and execution time
        corr_m = df["M"].corr(df[time_col])
        plt.title(f"{algo} — Time vs M (correlation: {corr_m:.3f})")
        plt.xlabel("Instance size (M)")
        plt.ylabel("Execution time (µs)")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()

        # Save figure (Time vs M)
        plt.savefig(os.path.join(output_dir, f"{algo}_time_vs_M_scatter.png"))
        plt.close()
