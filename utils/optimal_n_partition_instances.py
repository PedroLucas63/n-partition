import random

def generate_balanced_instances_with_bits(filename, n_values, k_values, b_values, repeat=10, seed=None):
    """
    Generates balanced N-partition problem instances with known optimal makespan,
    incorporating bit control (b), and saves them to a text file.

    Each instance is written as:
    N K B OPTIMAL_SUM
    N1 N2 N3 ... NN

    Parameters:
    - filename: output file name (.txt)
    - n_values: list of vector sizes (n)
    - k_values: list of number of partitions (k)
    - b_values: list of bits (b) controlling number magnitude
    - repeat: number of instances per parameter combination
    - seed: random seed (optional)
    """
    if seed is not None:
        random.seed(seed)

    with open(filename, "w") as f:
        instance_id = 1

        for n in n_values:
            for k in k_values:
                for b in b_values:
                    for r in range(repeat):
                        max_val = 2**b - 1
                        arr = []

                        # Choose an optimal sum target proportional to b
                        total_sum = random.randint(k * 10, k * max_val)
                        optimal_sum = total_sum // k

                        # Generate k balanced groups that sum to optimal_sum
                        for _ in range(k):
                            objective_sum = optimal_sum
                            while objective_sum > 0 and len(arr) < n:
                                x = random.randint(1, min(objective_sum, max_val))
                                arr.append(x)
                                objective_sum -= x

                        # If not enough elements, fill randomly
                        while len(arr) < n:
                            arr.append(random.randint(1, max_val))

                        f.write(f"# Instance {instance_id}\n")
                        f.write(f"{n} {k} {b} {optimal_sum}\n")
                        f.write(" ".join(map(str, arr)) + "\n\n")

                        instance_id += 1

    print(f"All {instance_id - 1} instances saved to '{filename}'.")


# -----------------------------
# Default parameters
n_values = [10, 20, 30, 40, 50]
k_values = [2, 3, 4, 8]
b_values = [8, 16, 20]
repeat = 30

# Generate instances and save to file
generate_balanced_instances_with_bits("../instances/optimal_n_partition_instances.txt", n_values, k_values, b_values, repeat, seed=42)
