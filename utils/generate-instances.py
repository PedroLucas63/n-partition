import random
from include.partition import CGA

def balanced_strategy(
  n: int,
  m: int,
  b: int,
):
   lb = 2 ** (b-1) * m
   total_sum = random.randint(lb, 2 * lb)
   q = m // n
   r = m % n
   group_sum = total_sum // n
   
   values = []
   
   for _ in range(n):
      if r > 0:
         group_size = q + 1
         r = r - 1
      else:
         group_size = q
      
      remaining_sum = group_sum
      
      for i in range(group_size):
         if i == group_size - 1:
            values.append(remaining_sum)
         else:
            value = random.randint(1, remaining_sum - (group_size - i - 1))
            values.append(value)
            remaining_sum -= value
   
   return group_sum, values         
   
def random_strategy(
  n: int,
  m: int,
  b: int,
):
   values = []
   
   for _ in range(m):
      value = random.randint(1, 2 ** b - 1)
      values.append(value)
   
   groups = CGA(values, n)
   makespan = max(map(sum, groups))
   
   return makespan, values

def generate(
  n: int,
  m: int,
  b: int,
  repeat: int,
  strategy: str,
):
   if strategy == "balanced":
      alg = balanced_strategy
   elif strategy == "random":
      alg = random_strategy
   else:
      raise ValueError("Invalid strategy")
   
   return [alg(n, m, b) for _ in range(repeat)]

def generate_instances(
  file_path,
  n_values=[2, 3, 4, 5],
  max_m=20,
  b_values=[4, 8, 16],
  repeat=5,
  strategy="balanced",
):
   instance_id = 1
   with open(file_path, "w") as f:
      for n in n_values:
         for m in range(n, max_m + 1):
            for b in b_values:
               print(f"Generating instances for config {n} {m} {b}")
               instances = generate(n, m, b, repeat, strategy)
               for makespan, values in instances:
                  f.write(f"# Instance {instance_id}\n")
                  f.write(f"{m} {n} {b} {makespan}\n")
                  f.write(" ".join(map(str, values)) + "\n\n")
                  instance_id += 1

if __name__ == "__main__":
   print("Generating balanced instances...")
   generate_instances("balanced.txt")
   
   print("Generating random instances...")
   generate_instances("random.txt", strategy="random")