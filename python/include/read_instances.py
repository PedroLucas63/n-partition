import os

class InstanceData:
    """Class to store the data of a single instance."""
    def __init__(self, M=0, N=0, B=0, optimal_sum=0, values=None):
        self.M = M                  # Number of elements
        self.N = N                  # Number of partitions
        self.B = B                  # Number of bits used to generate numbers
        self.optimal_sum = optimal_sum  # Known optimal partition sum
        self.values = values or []      # List of generated numbers

    def __repr__(self):
        """Short text representation (for debugging)."""
        return (f"InstanceData(M={self.M}, N={self.N}, B={self.B}, "
                f"optimal_sum={self.optimal_sum}, values={self.values[:5]}...)")



def read_instances(file_path="../instances/optimal_m_partition_instances.txt"):
    """
    Reads all instances from the given file.

    Expected file format:
        # Instance X
        M N B OPTIMAL_SUM
        num1 num2 num3 ...

    Args:
        file_path (str): Path to the instance file.

    Returns:
        list[InstanceData]: A list containing all parsed instances.
    """
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return []

    instances = []
    current = None
    reading_values = False

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            # Detect new instance header
            if line.startswith("# Instance"):
                # If we were reading an instance, store it before starting a new one
                if current and current.values:
                    instances.append(current)
                # Initialize a new instance
                current = InstanceData()
                reading_values = False
                continue

            # Read parameters line: M N B optimal_sum
            if not reading_values and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 4:
                    current.M = int(parts[0])
                    current.N = int(parts[1])
                    current.B = int(parts[2])
                    current.optimal_sum = int(parts[3])
                    reading_values = True
                continue

            # Read values (the array of numbers)
            if reading_values:
                values = list(map(int, line.split()))
                current.values.extend(values)

        # Add the last instance if file ends without a new header
        if current and current.values:
            instances.append(current)

    print(f"✅ {len(instances)} instances successfully read from {file_path}")
    return instances



def print_instances(instances):
    """
    Prints all instances to the console for verification.

    Args:
        instances (list[InstanceData]): List of instances to print.
    """
    for i, inst in enumerate(instances, start=1):
        print(f"Instance {i}:")
        print(f"  M: {inst.M}, N: {inst.N}, B: {inst.B}, optimal_sum: {inst.optimal_sum}")
        print(f"  Values: {' '.join(map(str, inst.values))}\n")

