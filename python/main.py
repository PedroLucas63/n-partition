from include.partition import LS, LPT, MULTIFIT
from random import randint
from typing import List

def printGroups(groups: List[List[int]], name: str):
   """
   Prints the results of the partitioning algorithm.

   Parameters
   ----------
   groups : List[List[int]]
      The list of subsets obtained from the partitioning algorithm.
   name : str
      The name of the partitioning algorithm used (e.g. "Greedy", "LPT").

   Returns
   -------
   None
   """
   print(f"\n{'='*3} {name} {'='*3}")

   for i in range(len(groups)):
      print(f"Group {i+1} (Sum: {sum(groups[i])}): {groups[i]}")

def main():
   """
   Main entry point for the partitioning algorithm testing.

   The function generates a list of random integers with a sum of
   n * (randint(n, n * 1000) // 3, where n is the number of subsets.
   It then applies the greedy and LPT partitioning algorithms to the data
   and prints the results.

   Parameters
   ----------
   None

   Returns
   -------
   None
   """
   n = 3
   MAX_OPTIMAL_SUM = 1000
   
   optimalSum = randint(n, n * MAX_OPTIMAL_SUM) // n
   data = []
   
   for _ in range(n):
      objectiveSum = optimalSum
      
      while objectiveSum != 0:
         x = randint(1, objectiveSum)
         data.append(x)
         objectiveSum -= x

   print(f"Data: {data}")
   print(f"Optimal sum: {optimalSum}")
   
   ls = LS(data, n)
   lpt = LPT(data, n)
   mf = MULTIFIT(data, n)
   
   printGroups(ls, "List Scheduling")
   printGroups(lpt, "Longest Processing Time")
   printGroups(mf, "MULTIFIT")
   
if __name__ == "__main__":
   main()