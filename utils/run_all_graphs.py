# utils/run_all_graphs.py
import os

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
csv_file = os.path.join(project_dir, "results.csv")

# Pasta de saída das imagens
imgs_dir = os.path.join(project_dir, "imgs")
os.makedirs(imgs_dir, exist_ok=True)

# Importa funções de plot
from plot.error_over_instances import plot_error_over_instance
from plot.error_over_n import plot_error_vs_n
from plot.time_over_n import plot_time_vs_n
from plot.plot_scatter_time_vs_n_m import plot_scatter_time_vs_n_m
from plot.plot_scatter_error_vs_m_n import plot_scatter_error_vs_m_n

# Executa todos os gráficos

print("Gerando gráficos de erro vs N...")
plot_error_vs_n(csv_file, imgs_dir)

print("Gerando gráficos de tempo vs N...")
plot_time_vs_n(csv_file, imgs_dir)

print("Gerando gráficos de error vs instancias...")
plot_error_over_instance(csv_file, imgs_dir)

print("Gerando gráficos de dispersão de tempo vs N e M...")
plot_scatter_time_vs_n_m(csv_file, imgs_dir)

print("Gerando gráficos de dispersão de erro vs N e M...")
plot_scatter_error_vs_m_n(csv_file, imgs_dir)


print("Todos os gráficos foram gerados na pasta imgs!")
