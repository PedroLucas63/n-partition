# utils/run_all_graphs.py
import os

import os

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
csv_file = os.path.join(project_dir, "results.csv")

# Pasta de saída das imagens
imgs_dir = os.path.join(project_dir, "imgs")
os.makedirs(imgs_dir, exist_ok=True)

# Importa funções de plot
from error_over_instances import plot_error_over_instance
from error_over_k import plot_error_vs_k
from time_over_k import plot_time_vs_k
from error_over_n import plot_error_vs_n


# Executa todos os gráficos
print("Gerando gráficos de erro vs N...")
plot_error_vs_n(csv_file, imgs_dir)

print("Gerando gráficos de erro vs K...")
plot_error_vs_k(csv_file, imgs_dir)

print("Gerando gráficos de tempo vs K...")
plot_time_vs_k(csv_file, imgs_dir)

print("Gerando gráficos de error vs instancias...")
plot_error_over_instance(csv_file, imgs_dir)

print("Todos os gráficos foram gerados na pasta imgs!")
