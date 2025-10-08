from typing import List

def greedy(data: List[int], k: int) -> List[List[int]]:
   """
   Partition a list of integers into k groups using a greedy algorithm.

   The algorithm assigns each element to the subset with the current smallest sum.
   This produces a reasonably balanced distribution, but not necessarily optimal.

   Parameters
   ----------
   data : List[int]
      The list of integers to partition.
   k : int
      The number of groups to create.

   Returns
   -------
   List[List[int]]
      A list containing k groups (each subset is a list of integers).
   """
   if k <= 0:
      raise ValueError("K must be a positive integer")
   if k == 1:
      return [data]

   groups = [[] for _ in range(k)]
   sums = [0 for _ in range(k)]

   for value in data:
      min_idx = sums.index(min(sums))
      groups[min_idx].append(value)
      sums[min_idx] += value

   return groups


def lpt(data: List[int], k: int) -> List[List[int]]:
   """
   Partition a list of integers into k groups using the LPT (Longest Processing Time) heuristic.

   The algorithm sorts the list in descending order and then applies the greedy algorithm.
   This often produces a better balance than greedy alone.

   Parameters
   ----------
   data : List[int]
      The list of integers to partition.
   k : int
      The number of groups to create.

   Returns
   -------
   List[List[int]]
      A list containing k groups (each subset is a list of integers).
   """
   if k <= 0:
      raise ValueError("K must be a positive integer")
   if k == 1:
      return [data]

   sorted_data = sorted(data, reverse=True)
   return greedy(sorted_data, k)
