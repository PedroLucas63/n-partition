import os
import random

def generate_balanced_instances_strict(
    file_path,
    n_values=[10, 20, 30, 40, 50],
    k_values=[2, 3, 4, 8],
    b_values=[8, 16, 20],
    repeat=30,
    seed=42
):
    random.seed(seed)
    instance_id = 1

    with open(file_path, "w") as f:
        for n in n_values:
            for k in k_values:
                for b in b_values:
                    for _ in range(repeat):
                        max_optimal_sum = max(n + 10, 2 ** b // (10 * k))
                        optimal_sum = random.randint(n, max_optimal_sum)

                        arr = []
                        for _ in range(k):
                            objective_sum = optimal_sum
                            while objective_sum > 0:
                                x = random.randint(1, objective_sum)
                                arr.append(x)
                                objective_sum -= x

                        f.write(f"# Instance {instance_id}\n")
                        f.write(f"{len(arr)} {k} {b} {optimal_sum}\n")
                        f.write(" ".join(map(str, arr)) + "\n\n")
                        instance_id += 1

    print(f"✅ Geradas {instance_id - 1} instâncias em {file_path}")



if __name__ == "__main__":
    # Parâmetros padrão
    n_values = [10, 20, 30, 40, 50]
    k_values = [2, 3, 4, 8]
    b_values = [8, 16, 20]
    repeat = 30

    # Caminho da pasta onde será salvo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
    instances_dir = os.path.join(parent_dir, "instances")
    os.makedirs(instances_dir, exist_ok=True)

    file_path = os.path.join(instances_dir, "optimal_n_partition_instances.txt")

    # Gerar as instâncias
    generate_balanced_instances_strict(file_path, n_values, k_values, b_values, repeat, seed=42)
