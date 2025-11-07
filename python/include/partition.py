from typing import List
import heapq
import copy
import math

def LS(arr: List[int], n: int) -> List[List[int]]:
   """
   Partition a list of integers into n groups using a list scheduling algorithm.

   The algorithm assigns each element to the subset with the current smallest sum.
   This produces a reasonably balanced distribution, but not necessarily optimal.

   Parameters
   ----------
   arr : List[int]
      The list of integers to partition.
   n : int
      The number of groups to create.

   Returns
   -------
   List[List[int]]
      A list containing n groups (each subset is a list of integers).
   """
   if n <= 0:
      raise ValueError("n must be a positive integer")
   if n == 1:
      return [arr]

   groups = [[] for _ in range(n)]
   pq = [(0, i) for i in range(n)]
   heapq.heapify(pq)

   for x in arr:
      sum, i = heapq.heappop(pq)
      groups[i].append(x)
      heapq.heappush(pq, (sum + x, i))

   return groups

def LPT(arr: List[int], n: int) -> List[List[int]]:
   """
   Partition a list of integers into k groups using the LPT (Longest Processing Time) heuristic.

   The algorithm sorts the list in descending order and then applies the greedy algorithm.
   This often produces a better balance than greedy alone.

   Parameters
   ----------
   arr : List[int]
      The list of integers to partition.
   n : int
      The number of groups to create.

   Returns
   -------
   List[List[int]]
      A list containing k groups (each subset is a list of integers).
   """
   if n <= 0:
      raise ValueError("K must be a positive integer")
   if n == 1:
      return [arr]

   return LS(sorted(arr, reverse=True), n)

def MULTIFIT(arr: List[int], n: int, k: int = 7) -> List[List[int]]:
   """
   Partition a list of integers into k groups using the MULTIFIT (MULTI-FIT) heuristic.

   The algorithm first sorts the list in descending order and then iteratively constructs the final k groups.
   In each iteration, it computes the average capacity of the groups and delegates to the internal FFD
   procedure to construct new groups. If the number of groups exceeds k, it updates the lower bound for the next iteration.
   Otherwise, it updates the upper bound and stores the current groups as the best solution.

   Parameters
   ----------
   arr : List[int]
      The list of integers to partition.
   n : int
      The number of groups to create.
   k : int
      The number of iterations to run the algorithm (default is 7).

   Returns
   -------
   List[List[int]]
      A list containing k groups (each subset is a list of integers).
   """
   if n <= 0:
      raise ValueError("K must be a positive integer")
   if n == 1:
      return [arr]
   
   arr = sorted(arr, reverse=True)
   
   sum = 0
   max_val = 0
   for x in arr:
      sum += x
      max_val = max(max_val, x)

   lowerBound = max(max_val, sum // n)
   upperBound = max(max_val, 2 * sum // n)

   bestGroups = []
   
   for _ in range(k):
      capacity = (lowerBound + upperBound) // 2
      groups = FFD(arr, capacity)

      if len(groups) > n:
         lowerBound = capacity
      else:
         bestGroups = groups
         upperBound = capacity
   
   return bestGroups

def FFD(arr: List[int], capacity: int) -> List[List[int]]:
   """
   First-Fit Decreasing (FFD) algorithm to partition a list of integers into groups
   with a given capacity.

   The algorithm assigns each element to the subset with the current smallest remaining
   capacity, in order to balance the groups.

   Parameters
   ----------
   arr : List[int]
      The list of integers to partition.
   capacity : int
      The capacity of each group.

   Returns
   -------
   List[List[int]]
      A list containing the partitioned groups of the array.
   """
   groups = []
   remaining = []
   
   for x in arr:
      placed = False
      for i in range(len(groups)):
         if remaining[i] >= x:
            groups[i].append(x)
            remaining[i] -= x
            placed = True
            break
      if not placed:
         groups.append([x])
         remaining.append(capacity - x)
   
   return groups

def CGA(arr: List[int], n: int) -> List[List[int]]:
   """
   Complete Greedy Algorithm (CGA) to partition a list of integers into n groups.
   
   The algorithm first applies the Longest Processing Time (LPT) heuristic to find an initial solution.
   Then, it uses backtracking to explore all possible solutions and find the best one.
   
   Parameters
   ----------
   arr : List[int]
      The list of integers to partition.
   n : int
      The number of groups to create.
   
   Returns
   -------
   List[List[int]]
      A list containing the best partitioned groups of the array.
   """
   # Check if n is valid
   if n <= 0:
      raise ValueError("K must be a positive integer")
   if n == 1:
      return [arr]
   
   # Get one solution (heurística inicial)
   groups = LPT(arr, n)
   
   # get sums of groups
   sums = list(map(sum, groups))

   # Get makespan
   makespan = max(sums)

   # Get makespan lowerbound
   total = sum(sums)
   lowerbound = math.ceil(float(total) / n)
   
   # Get best solution
   if lowerbound < makespan:
      groupsSums = [0] * n
      actualGroups = [[] for _ in range(n)]
      makespan, groups = CGABacktracking(
         arr, 
         actualGroups, 
         groupsSums, 
         makespan, 
         lowerbound,
         copy.deepcopy(groups),
         0
      )
   
   # Return best solution
   return groups


def CGABacktracking(
   arr: List[int], 
   groups: List[List[int]], 
   groupSums: List[int], 
   makespan: int, 
   lowerbound: int,
   groupsCandidate: List[List[int]], 
   i: int
):
   """
   Backtracking algorithm to find the optimal partition of the array
   into n groups using a Complete Greedy Algorithm (CGA) approach.

   The algorithm iteratively assigns each element to the group with the
   current minimum sum, in order to balance the groups. It uses a
   backtracking approach to explore all possible combinations of groups.

   Parameters
   ----------
   arr : List[int]
      The list of integers to partition.
   groups : List[List[int]]
      The current partition of the array.
   groupSums : List[int]
      The sum of each group in the current partition.
   makespan : int
      The maximum difference between the sums of the groups.
   lowerbound : int
      The lower bound of the makespan.
   groupsCandidate : List[List[int]]
      The current candidate partition.
   i : int
      The current index in the array.

   Returns
   -------
   int
      The maximum difference between the sums of the groups.
   List[List[int]]
      The current candidate partition.
   """
   # Base case
   if i == len(arr):
      currentMax = max(groupSums)
      # Update
      if currentMax < makespan:
         makespan = currentMax
         groupsCandidate = copy.deepcopy(groups)
      return makespan, groupsCandidate

   # Sort groups by carga atual
   groupsIndices = list(range(len(groups)))
   groupsIndices.sort(key=lambda idx: groupSums[idx])
   
   # Tried sums
   triedSums = set()
   
   # Backtracking
   for j in groupsIndices:
      # Not already tried
      if groupSums[j] in triedSums:
         continue
      triedSums.add(groupSums[j])
      
      # Evaluation
      groupSums[j] += arr[i]
      currentMax = max(groupSums)

      # Uperbound prune
      if currentMax < makespan:
         # Recursion
         groups[j].append(arr[i])
         makespan, groupsCandidate = CGABacktracking(
            arr, groups, groupSums, makespan, lowerbound, groupsCandidate, i + 1
         )
         groups[j].pop() # Backtrack
         
         # Lowerbound prune
         if makespan == lowerbound:
            return makespan, groupsCandidate
      
      # Backtrack 
      groupSums[j] -= arr[i]
   
   return makespan, groupsCandidate