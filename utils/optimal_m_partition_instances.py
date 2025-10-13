import os
import random

def generate_balanced_instances(
    file_path,
    m_values=[10, 20, 30, 40, 50],
    n_values=[2, 3, 4, 8],
    b_values=[8, 16, 20],
    repeat=30,
    seed=42
):
    # Set a random seed for reproducibility
    random.seed(seed)
    instance_id = 1

    # Open the output file where all generated instances will be stored
    with open(file_path, "w") as f:
        # Iterate over all combinations of parameters m, n, and b
        for m in m_values:
            for n in n_values:
                for b in b_values:
                    for _ in range(repeat):
                        # Define a range for the optimal sum
                        max_optimal_sum = max(m + 30, 2 ** b // (10 * n))
                        optimal_sum = random.randint(m, max_optimal_sum)

                        arr = []
                        for _ in range(n):
                            # Initialize the partition sum for this subset
                            objective_sum = optimal_sum

                            # Determine how many elements to generate for this partition
                            objective_count = max(1, m // n)
                            partition_values = []
                            
                            for i in range(objective_count - 1):
                                # Generate random positive numbers that sum to 'objective_sum'
                                x = random.randint(1, objective_sum - (objective_count - i - 1))
                                partition_values.append(x)
                                objective_sum -= x
                            
                            # Add the last piece (ensures the sum is correct)
                            partition_values.append(objective_sum)
                            
                            # Append this partition’s values to the global array
                            arr.extend(partition_values)

                        # Write instance metadata and data to file
                        f.write(f"# Instance {instance_id}\n")
                        f.write(f"{len(arr)} {n} {b} {optimal_sum}\n")
                        f.write(" ".join(map(str, arr)) + "\n\n")
                        instance_id += 1

    # Print how many instances were generated and where they were saved
    print(f"✅ Generated {instance_id - 1} instances in {file_path}")


if __name__ == "__main__":
    # Default parameter values
    m_values = [10, 20, 30, 40, 50, 100]
    n_values = [2, 3, 4, 8, 16]
    b_values = [8, 16, 20]
    repeat = 25

    # Define the output directory (../instances relative to this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
    instances_dir = os.path.join(parent_dir, "instances")
    os.makedirs(instances_dir, exist_ok=True)

    # Full path to the output file
    file_path = os.path.join(instances_dir, "optimal_m_partition_instances.txt")

    # Generate and save the instances
    generate_balanced_instances(file_path, m_values, n_values, b_values, repeat, seed=42)
