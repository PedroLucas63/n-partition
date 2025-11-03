# Import libs
import os
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Parse arguments
def get_args() -> argparse.Namespace:
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
   return pd.read_csv(path)

def plot(df: pd.DataFrame, output_path: str):
   os.makedirs(output_path, exist_ok=True)
   
   # Rename columns
   df = df.rename(columns={
      "LS_Time(us)": "LS",
      "LPT_Time(us)": "LPT",
      "MULTIFIT_Time(us)": "MULTIFIT",
      "CGA_Time(us)": "CGA"
   })
   
   time_cols = ["LS", "LPT", "MULTIFIT", "CGA"]
   
   # 1️⃣ Gráficos de linha comparativos por N, M e B (log scale)
   for group_by in ["N", "M", "B"]:
      df_grouped = df.groupby(group_by)[time_cols].mean().reset_index()
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
      fig = plt.figure(figsize=(10,7))
      ax = fig.add_subplot(111, projection='3d')
      df_3d = df.groupby([x_col, y_col])[alg].mean().reset_index()
      X, Y = np.meshgrid(sorted(df_3d[x_col].unique()), sorted(df_3d[y_col].unique()))
      Z = np.zeros_like(X, dtype=float)
      for i, x_val in enumerate(sorted(df_3d[x_col].unique())):
         for j, y_val in enumerate(sorted(df_3d[y_col].unique())):
            row = df_3d[(df_3d[x_col]==x_val) & (df_3d[y_col]==y_val)]
            if not row.empty:
               Z[j,i] = row[alg].values[0]
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
   for algo in ["LS", "LPT", "MULTIFIT", "CGA"]:
      # Proximidade: Alg / Ótimo
      df[f"{algo}_proximity"] = df[f"{algo}_MaxGroupSum"] / df["OptimalMakespan"]
      # Erro relativo: (Alg - Ótimo) / Ótimo
      df[f"{algo}_error"] = (df[f"{algo}_MaxGroupSum"] - df["OptimalMakespan"]) / df["OptimalMakespan"]
   
   # Gráficos de proximidade por N, M, B
   for group_by in ["N", "M", "B"]:
      df_grouped = df.groupby(group_by)[[f"{algo}_proximity" for algo in ["LS","LPT","MULTIFIT","CGA"]]].mean().reset_index()
      plt.figure(figsize=(8,5))
      for algo in ["LS","LPT","MULTIFIT","CGA"]:
         plt.plot(df_grouped[group_by], df_grouped[f"{algo}_proximity"], marker='o', label=algo)
      plt.title(f"Proximidade média ao ótimo por {group_by}")
      plt.xlabel(group_by)
      plt.ylabel("Proximidade (1 = ótimo)")
      plt.grid(True)
      plt.legend()
      plt.savefig(os.path.join(output_path, f"proximity_by_{group_by}.png"))
      plt.close()
   
   # Gráficos de erro relativo por N, M, B
   for group_by in ["N", "M", "B"]:
      df_grouped = df.groupby(group_by)[[f"{algo}_error" for algo in ["LS","LPT","MULTIFIT","CGA"]]].mean().reset_index()
      plt.figure(figsize=(8,5))
      for algo in ["LS","LPT","MULTIFIT","CGA"]:
         plt.plot(df_grouped[group_by], df_grouped[f"{algo}_error"], marker='o', label=algo)
      plt.title(f"Erro médio relativo ao ótimo por {group_by}")
      plt.xlabel(group_by)
      plt.ylabel("Erro relativo ((Alg - Ótimo)/Ótimo)")
      plt.grid(True)
      plt.legend()
      plt.savefig(os.path.join(output_path, f"error_by_{group_by}.png"))
      plt.close()
   
   # Heatmaps de proximidade por N x M
   for algo in ["LS","LPT","MULTIFIT","CGA"]:
      df_heat = df.groupby(['N','M'])[f"{algo}_proximity"].mean().unstack()
      plt.figure(figsize=(8,6))
      sns.heatmap(df_heat, annot=True, fmt=".2f", cmap='viridis', cbar_kws={'label':'Proximidade'})
      plt.title(f"Proximidade média {algo} por N x M")
      plt.xlabel("M")
      plt.ylabel("N")
      plt.savefig(os.path.join(output_path, f"proximity_heatmap_{algo}_NxM.png"))
      plt.close()
      
   # 4️⃣ Score de acertos (fração de instâncias que atingiram o ótimo)
   algorithms = ["LS", "LPT", "MULTIFIT", "CGA"]

   # Criar coluna indicando se o algoritmo acertou o ótimo (1) ou não (0)
   for algo in algorithms:
      df[f"{algo}_hit"] = (df[f"{algo}_MaxGroupSum"] == df["OptimalMakespan"]).astype(int)

   # Gráficos de score por N, M, B
   for group_by in ["N", "M", "B"]:
      df_grouped = df.groupby(group_by)[[f"{algo}_hit" for algo in algorithms]].mean().reset_index()
      plt.figure(figsize=(8,5))
      for algo in algorithms:
         plt.plot(df_grouped[group_by], df_grouped[f"{algo}_hit"], marker='o', label=algo)
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