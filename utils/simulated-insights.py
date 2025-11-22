import sys
import pandas as pd


def global_analysis(csv_path):
   df = pd.read_csv(csv_path)

   # ============================================================
   # 1) Erro médio global por algoritmo
   # ============================================================
   mean_errors = (
      df.groupby("Algorithm")["MeanDistanceToIdeal"]
      .mean()
      .sort_values()
   )

   # ============================================================
   # 2) Ranking global baseado na média (1 = melhor)
   # ============================================================
   ranking = mean_errors.rank(method="min").astype(int)

   # ============================================================
   # 3) Pontuação global de vitórias
   #    Cada configuração (NumMachines, NumTasks) dá 1 ponto
   #    ao(s) algoritmo(s) com menor MeanDistanceToIdeal.
   # ============================================================
   victory_points = {algo: 0 for algo in df["Algorithm"].unique()}

   grouped = df.groupby(["NumMachines", "NumTasks"])
   for (_, _), group in grouped:
      min_dist = group["MeanDistanceToIdeal"].min()
      winners = group[group["MeanDistanceToIdeal"] == min_dist]["Algorithm"].unique()
      for w in winners:
         victory_points[w] += 1

   # ============================================================
   # PRINT FINAL
   # ============================================================
   print("\n==========================")
   print("     GLOBAL SUMMARY")
   print("==========================\n")

   print("Erro médio global (Mean Distance):\n")
   for algo, val in mean_errors.items():
      print(f"  {algo}: {val:.4f}")

   print("\nRanking global (1 = melhor):\n")
   for algo, val in ranking.items():
      print(f"  {algo}: {val}")

   print("\nPontuação de vitórias globais:\n")
   for algo, pts in sorted(victory_points.items(), key=lambda x: -x[1]):
      print(f"  {algo}: {pts} ponto(s)")

   print("\nAnalysis completed.\n")


if __name__ == "__main__":
   if len(sys.argv) != 2:
      print("Uso: python3 analyze_global.py arquivo.csv")
      sys.exit(1)

   global_analysis(sys.argv[1])
