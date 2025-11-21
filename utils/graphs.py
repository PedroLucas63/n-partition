# Import libs
import os
import re
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Parse arguments
def get_args() -> argparse.Namespace:
   """
   Parse arguments from command line.

   Returns:
       argparse.Namespace: A namespace containing the parsed arguments.

   The arguments are:

   --data: Path to data file
   --output: Path to output directory

   Example:
   python3 graphs.py --data data.csv --output results
   """
   parse = argparse.ArgumentParser(
      prog="Graphs tool",
      description="Generate graphs from data",
      epilog="Example: python3 graphs.py --data data.csv --output results"
   )
   parse.add_argument("--data", type=str, required=True, help="Path to data file")
   parse.add_argument("--output", type=str, required=True, help="Path to output directory")
   return parse.parse_args()

# Import data function
def import_data(path: str) -> pd.DataFrame:
   """
   Import data from a CSV file.

   Args:
       path (str): Path to CSV file.

   Returns:
       pd.DataFrame: DataFrame containing the data from the CSV file.
   """
   return pd.read_csv(path)

def plot(df: pd.DataFrame, output_path: str):
   """
   Generate various graphs from data.

   Args:
      df (pd.DataFrame): DataFrame containing the data to plot.
      output_path (str): Path to output directory.

   Returns:
      None

   Plots the following graphs:

      1. Line graphs comparing algorithms by N, M and B (log scale)
      2. 3D plots of time vs N, M and B for each algorithm
      3. Proximity and relative error graphs by N, M and B
      4. Heatmaps of proximity by N x M for each algorithm
      5. Score graphs by N, M and B for each algorithm

   The graphs are saved in the output directory specified by the user.
   """
   os.makedirs(output_path, exist_ok=True)

   # Work on a copy to avoid SettingWithCopyWarning
   df = df.copy()

   # --------------------------
   # Detect Genetic columns and compute means (same behaviour as metrics.py)
   # --------------------------
   genetic_makespan_cols = [c for c in df.columns if re.match(r"Genetic.*_MaxGroupSum", c)]
   genetic_time_cols = [c for c in df.columns if re.match(r"Genetic.*_Time\(us\)", c)]
   genetic_makespan_cols.sort()
   genetic_time_cols.sort()

   if genetic_makespan_cols:
      # média das execuções do genético (makespan)
      df["Genetic_Mean_MaxGroupSum"] = df[genetic_makespan_cols].mean(axis=1)
   if genetic_time_cols:
      # média das execuções do genético (tempo)
      df["Genetic_Mean_Time(us)"] = df[genetic_time_cols].mean(axis=1)

   # criar indicador de hit do genético: se qualquer execução atingiu o ótimo
   if genetic_makespan_cols:
      df["Genetic_hit"] = df[genetic_makespan_cols].eq(df["OptimalMakespan"], axis=0).any(axis=1).astype(int)
   else:
      df["Genetic_hit"] = 0

   # Rename time columns for plotting convenience. Include Genetic mean time if present.
   rename_map = {
      "LS_Time(us)": "LS",
      "LPT_Time(us)": "LPT",
      "MULTIFIT_Time(us)": "MULTIFIT",
      "CGA_Time(us)": "CGA"
   }
   if "Genetic_Mean_Time(us)" in df.columns:
      rename_map["Genetic_Mean_Time(us)"] = "Genetic"

   df_plot = df.rename(columns=rename_map)

   # Time columns to use in plots (only those present after rename)
   time_cols = [c for c in ["LS", "LPT", "MULTIFIT", "CGA", "Genetic"] if c in df_plot.columns]

   # 1️⃣ Gráficos de linha comparativos por N, M e B (log scale)
   for group_by in ["N", "M", "B"]:
      # ensure column exists in df
      if group_by not in df_plot.columns:
         continue
      df_grouped = df_plot.groupby(group_by)[time_cols].mean().reset_index()
      plt.figure(figsize=(8,5))
      for algo in time_cols:
         plt.plot(df_grouped[group_by], df_grouped[algo], marker='o', label=algo)
      plt.title(f"Tempo médio por {group_by} (log scale)")
      plt.xlabel(group_by)
      plt.ylabel("Tempo (us)")
      plt.yscale('log')  # escala log
      plt.legend()
      plt.grid(True, which="both", ls="--")
      plt.savefig(os.path.join(output_path, f"line_comparative_log_by_{group_by}.png"))
      plt.close()

   # 2️⃣ Gráficos 3D ajustados
   def plot_3d(x_col, y_col, alg='LS', filename_suffix=''):
      if x_col not in df_plot.columns or y_col not in df_plot.columns or alg not in df_plot.columns:
         return
      fig = plt.figure(figsize=(10,7))
      ax = fig.add_subplot(111, projection='3d')
      df_3d = df_plot.groupby([x_col, y_col])[alg].mean().reset_index()
      X, Y = np.meshgrid(sorted(df_3d[x_col].unique()), sorted(df_3d[y_col].unique()))
      Z = np.full_like(X, np.nan, dtype=float)
      for i, x_val in enumerate(sorted(df_3d[x_col].unique())):
         for j, y_val in enumerate(sorted(df_3d[y_col].unique())):
            row = df_3d[(df_3d[x_col]==x_val) & (df_3d[y_col]==y_val)]
            if not row.empty:
               Z[j,i] = row[alg].values[0]
      # if all nan -> skip
      if np.all(np.isnan(Z)):
         plt.close()
         return
      surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, edgecolor='k')
      fig.colorbar(surf, shrink=0.5, aspect=5, label=f"{alg} Tempo (us)")
      ax.set_xlabel(x_col)
      ax.set_ylabel(y_col)
      ax.set_zlabel(f"Tempo ({alg})")
      plt.title(f"{alg} Tempo 3D: {x_col} x {y_col}")
      plt.savefig(os.path.join(output_path, f"3D_{alg}_{x_col}_{y_col}{filename_suffix}.png"))
      plt.close()

   for algo in time_cols:
      plot_3d('N','M', alg=algo)
      plot_3d('N','B', alg=algo)
      plot_3d('M','B', alg=algo)

   # 3️⃣ Precisão e erro relativo em relação ao ótimo
   # Prepare list of proximity/ error algorithms (use Genetic mean if available)
   proximity_algos = ["LS", "LPT", "MULTIFIT", "CGA"]
   if "Genetic_Mean_MaxGroupSum" in df_plot.columns:
      proximity_algos.append("Genetic")

   for algo in proximity_algos:
      makespan_col = f"{algo}_MaxGroupSum" if algo != "Genetic" else "Genetic_Mean_MaxGroupSum"
      # guard clause if column not present
      if makespan_col not in df_plot.columns:
         continue
      # Proximidade: Alg / Ótimo
      df_plot[f"{algo}_proximity"] = df_plot[makespan_col] / df_plot["OptimalMakespan"]
      # Erro relativo: (Alg - Ótimo) / Ótimo
      df_plot[f"{algo}_error"] = (df_plot[makespan_col] - df_plot["OptimalMakespan"]) / df_plot["OptimalMakespan"]

   # Gráficos de proximidade por N, M, B
   for group_by in ["N", "M", "B"]:
      cols = [f"{algo}_proximity" for algo in proximity_algos if f"{algo}_proximity" in df_plot.columns]
      if group_by not in df_plot.columns or not cols:
         continue
      df_grouped = df_plot.groupby(group_by)[cols].mean().reset_index()
      plt.figure(figsize=(8,5))
      for algo in proximity_algos:
         col = f"{algo}_proximity"
         if col in df_grouped.columns:
            plt.plot(df_grouped[group_by], df_grouped[col], marker='o', label=algo)
      plt.title(f"Proximidade média ao ótimo por {group_by}")
      plt.xlabel(group_by)
      plt.ylabel("Proximidade (1 = ótimo)")
      plt.grid(True)
      plt.legend()
      plt.savefig(os.path.join(output_path, f"proximity_by_{group_by}.png"))
      plt.close()

   # Gráficos de erro relativo por N, M, B
   for group_by in ["N", "M", "B"]:
      cols = [f"{algo}_error" for algo in proximity_algos if f"{algo}_error" in df_plot.columns]
      if group_by not in df_plot.columns or not cols:
         continue
      df_grouped = df_plot.groupby(group_by)[cols].mean().reset_index()
      plt.figure(figsize=(8,5))
      for algo in proximity_algos:
         col = f"{algo}_error"
         if col in df_grouped.columns:
            plt.plot(df_grouped[group_by], df_grouped[col], marker='o', label=algo)
      plt.title(f"Erro médio relativo ao ótimo por {group_by}")
      plt.xlabel(group_by)
      plt.ylabel("Erro relativo ((Alg - Ótimo)/Ótimo)")
      plt.grid(True)
      plt.legend()
      plt.savefig(os.path.join(output_path, f"error_by_{group_by}.png"))
      plt.close()

   # Heatmaps de proximidade por N x M
   for algo in proximity_algos:
      col = f"{algo}_proximity"
      if col not in df_plot.columns:
         continue
      # group by N x M, pivot
      try:
         df_heat = df_plot.groupby(['N','M'])[col].mean().unstack()
         plt.figure(figsize=(8,6))
         sns.heatmap(df_heat, annot=True, fmt=".2f", cmap='viridis', cbar_kws={'label':'Proximidade'})
         plt.title(f"Proximidade média {algo} por N x M")
         plt.xlabel("M")
         plt.ylabel("N")
         plt.savefig(os.path.join(output_path, f"proximity_heatmap_{algo}_NxM.png"))
         plt.close()
      except Exception:
         # skip if grouping not possible
         pass

   # 4️⃣ Score de acertos (fração de instâncias que atingiram o ótimo)
   algorithms = ["LS", "LPT", "MULTIFIT", "CGA"]
   if "Genetic_Mean_MaxGroupSum" in df_plot.columns:
      algorithms.append("Genetic")

   # Criar coluna indicando se o algoritmo acertou o ótimo (1) ou não (0)
   for algo in algorithms:
      makespan_col = f"{algo}_MaxGroupSum" if algo != "Genetic" else "Genetic_Mean_MaxGroupSum"
      if makespan_col in df_plot.columns:
         df_plot[f"{algo}_hit"] = (df_plot[makespan_col] == df_plot["OptimalMakespan"]).astype(int)
      else:
         df_plot[f"{algo}_hit"] = 0

   # For Genetic we also want to reflect if any execution hit optimal (already computed)
   if "Genetic_hit" in df_plot.columns:
      df_plot["Genetic_hit"] = df_plot["Genetic_hit"]

   # Gráficos de score por N, M, B
   for group_by in ["N", "M", "B"]:
      hit_cols = [f"{algo}_hit" for algo in algorithms if f"{algo}_hit" in df_plot.columns]
      if group_by not in df_plot.columns or not hit_cols:
         continue
      df_grouped = df_plot.groupby(group_by)[hit_cols].mean().reset_index()
      plt.figure(figsize=(8,5))
      for algo in algorithms:
         col = f"{algo}_hit"
         if col in df_grouped.columns:
            plt.plot(df_grouped[group_by], df_grouped[col], marker='o', label=algo)
      plt.title(f"Score médio de acertos por {group_by} (1 = acerto)")
      plt.xlabel(group_by)
      plt.ylabel("Score de acertos (0-1)")
      plt.ylim(0,1.05)
      plt.grid(True)
      plt.legend()
      plt.savefig(os.path.join(output_path, f"accuracy_by_{group_by}.png"))
      plt.close()

# Main
if __name__ == "__main__":
   args = get_args()

   df = import_data(args.data)
   plot(df, args.output)
