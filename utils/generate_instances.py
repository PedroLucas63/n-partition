import random

def generate_instances_to_file(filename, n_values, k_values, b_values, repeat=10, seed=None):
    """
    Generates N-partition problem instances and saves them to a file.

    Each instance is written as:
    N K B
    N1 N2 N3 ... NN

    Parameters:
    - filename: name of the output .txt file
    - n_values: list of vector sizes (n)
    - k_values: list of number of partitions (k)
    - b_values: list of bits (B) for generating numbers
    - repeat: how many instances to generate for each combination
    - seed: random seed (optional)
    """
    if seed is not None:
        random.seed(seed)

    with open(filename, "w") as f:
        for n in n_values:
            for k in k_values:
                for b in b_values:
                    for r in range(repeat):
                        numbers = [random.randint(1, 2**b - 1) for _ in range(n)]
                        f.write(f"{n} {k} {b}\n")
                        f.write(" ".join(map(str, numbers)) + "\n")

# -----------------------------
# Default thesis parameters
n_values = [10,20,30,40,50]
k_values = [2,3,4,8,16]
b_values = [5,8,16,20,24,28,32]
repeat = 10

# Generate instances and save to a file
generate_instances_to_file("../n_partition_instances.txt", n_values, k_values, b_values, repeat, seed=42)

print("All instances saved to 'n_partition_instances.txt'.")
