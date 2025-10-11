# utils/plot_error_over_time.py

import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_error_over_instance(csv_file, imgs_dir):
    """
    Gera gráficos separados para LS, LPT e MULTIFIT mostrando a evolução do erro percentual
    ao longo das instâncias e salva as imagens na pasta imgs_dir/error_over_time.

    Args:
        csv_file (str): Caminho para o arquivo CSV com os resultados.
        imgs_dir (str): Pasta base onde os gráficos serão salvos.
    """
    # Verifica se o arquivo existe
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"O arquivo {csv_file} não foi encontrado!")

    # Lê o CSV
    df = pd.read_csv(csv_file)

    # Calcula erro percentual
    df["LS_Error(%)"] = 100 * (df["LS_MaxGroupSum"] / df["OptimalMakespan"] - 1)
    df["LPT_Error(%)"] = 100 * (df["LPT_MaxGroupSum"] / df["OptimalMakespan"] - 1)
    df["MULTIFIT_Error(%)"] = 100 * (df["MULTIFIT_MaxGroupSum"] / df["OptimalMakespan"] - 1)

    # Cria pasta específica
    output_dir = os.path.join(imgs_dir, "error_over_time")
    os.makedirs(output_dir, exist_ok=True)

    # Cores e marcadores para cada heurística
    heuristics = {
        "LS": {"color": "tab:blue", "marker": "o"},
        "LPT": {"color": "tab:orange", "marker": "s"},
        "MULTIFIT": {"color": "tab:green", "marker": "^"}
    }

    # Loop para gerar um gráfico por heurística
    for algo, style in heuristics.items():
        plt.figure(figsize=(12, 5))
        plt.plot(
            df["InstanceID"],
            df[f"{algo}_Error(%)"],
            linestyle='-',
            markersize=4,
            linewidth=2,
            label=algo
        )
        plt.title(f"Evolução do erro percentual ao longo das instâncias - {algo}", fontsize=14)
        plt.xlabel("Instâncias", fontsize=12)
        plt.ylabel("Erro (%)", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()

        # Salva a figura
        output_file = os.path.join(output_dir, f"{algo}_error_over_instances.png")
        plt.savefig(output_file, dpi=150)
        plt.close()
