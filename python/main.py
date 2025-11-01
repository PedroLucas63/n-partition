import time
import csv
from include.read_instances import read_instances
from include.partition import LS, LPT, MULTIFIT  # funções que implementam os algoritmos

def write_results(writer, instance_id, M, N, B, optimal, ls_res, lpt_res, mf_res, ls_time, lpt_time, mf_time):
   def max_group_sum(groups):
        return max(sum(g) for g in groups)
   writer.writerow([
      instance_id, M, N, B, optimal,
      max_group_sum(ls_res), int(round(ls_time)),
      max_group_sum(lpt_res), int(round(lpt_time)),
      max_group_sum(mf_res), int(round(mf_time))
   ])

def run_experiments(output_path="../results/results.csv"):
   instances = read_instances()
   with open(output_path, "w", newline="") as f:
      writer = csv.writer(f)
      writer.writerow(["InstanceID","M","N","B","OptimalMakespan",
                        "LS_MaxGroupSum","LS_Time(us)",
                        "LPT_MaxGroupSum","LPT_Time(us)",
                        "MULTIFIT_MaxGroupSum","MULTIFIT_Time(us)"])
      
      for i, inst in enumerate(instances, start=1):
         arr = inst.values
         start = time.perf_counter()
         ls_res = LS(arr, inst.N)
         ls_time = (time.perf_counter() - start) * 1e6

         start = time.perf_counter()
         lpt_res = LPT(arr, inst.N)
         lpt_time = (time.perf_counter() - start) * 1e6

         start = time.perf_counter()
         mf_res = MULTIFIT(arr, inst.N)
         mf_time = (time.perf_counter() - start) * 1e6

         write_results(writer, i, inst.M, inst.N, inst.B, inst.optimal_sum,
                        ls_res, lpt_res, mf_res, ls_time, lpt_time, mf_time)

if __name__ == "__main__":
   run_experiments()