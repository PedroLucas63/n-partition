# utils/run_all_graphs.py
import os

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "results"))
csv_file = os.path.join(project_dir, "results.csv")

# Pasta de saída das imagens
imgs_dir = os.path.join(project_dir, "imgs")
os.makedirs(imgs_dir, exist_ok=True)

# Importa funções de plot
from error_over_instances import plot_error_over_instance
from error_over_k import plot_error_vs_k
from time_over_k import plot_time_vs_k
from plot_scatter_time_vs_k_n import plot_scatter_time_vs_k_n
from plot_scatter_error_vs_n_k import plot_scatter_error_vs_n_k

# Executa todos os gráficos

print("Gerando gráficos de erro vs K...")
plot_error_vs_k(csv_file, imgs_dir)

print("Gerando gráficos de tempo vs K...")
plot_time_vs_k(csv_file, imgs_dir)

print("Gerando gráficos de error vs instancias...")
plot_error_over_instance(csv_file, imgs_dir)

print("Gerando gráficos de dispersão de tempo vs K e N...")
plot_scatter_time_vs_k_n(csv_file, imgs_dir)

print("Gerando gráficos de dispersão de erro vs K e N...")
plot_scatter_error_vs_n_k(csv_file, imgs_dir)


print("Todos os gráficos foram gerados na pasta imgs!")
