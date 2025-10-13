package experiment;

import partition.LRMPartition;
import partition.Partition;
import utils.ReadInstances;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

/**
 * Class responsible for running all partition heuristics (LS, LPT, MULTIFIT, LRM)
 * on the given instance dataset and writing the results to a CSV file.
 *
 * <p>Each row in the CSV corresponds to one instance, with the recorded
 * makespan and execution time (in microseconds) for each algorithm.</p>
 */
public class ExperimentRunner {

    /**
     * Runs all algorithms for each instance and saves results to a CSV file.
     *
     * @param csvPath Output CSV path (e.g., "../results/results.csv")
     */
    public static void run(String csvPath) {
        List<ReadInstances.InstanceData> instances;
        try {
            instances = ReadInstances.readInstances();
        } catch (IOException e) {
            System.err.println("[ERROR] Failed to read instances: " + e.getMessage());
            return;
        }

        try (FileWriter writer = new FileWriter(csvPath)) {
            // CSV header
            writer.write("InstanceID,M,N,B,OptimalMakespan,"
                    + "LS_MaxGroupSum,LS_Time(us),"
                    + "LPT_MaxGroupSum,LPT_Time(us),"
                    + "MULTIFIT_MaxGroupSum,MULTIFIT_Time(us),"
                    + "LRM_MaxGroupSum,LRM_Time(us)\n");

            int instanceID = 1;
            for (ReadInstances.InstanceData instance : instances) {
                writeInstanceResults(writer, instance, instanceID);
                instanceID++;
            }

            System.out.println("✅ Experiment completed. Results saved to: " + csvPath);
        } catch (IOException e) {
            System.err.println("[ERROR] Failed to write CSV: " + e.getMessage());
        }
    }

    /**
     * Executes all algorithms for a given instance and writes results to CSV.
     */
    private static void writeInstanceResults(FileWriter writer, ReadInstances.InstanceData inst, int instanceID) throws IOException {
        int N = inst.N;
        var arr = inst.values;

        // --- LS ---
        long start = System.nanoTime();
        var ls = Partition.LS(arr, N);
        long end = System.nanoTime();
        long lsTime = (end - start) / 1000; // microseconds

        // --- LPT ---
        start = System.nanoTime();
        var lpt = Partition.LPT(arr, N);
        end = System.nanoTime();
        long lptTime = (end - start) / 1000;

        // --- MULTIFIT ---
        start = System.nanoTime();
        var mf = Partition.MULTIFIT(arr, N);
        end = System.nanoTime();
        long mfTime = (end - start) / 1000;

        // --- LRM ---
        start = System.nanoTime();
        var lrm = LRMPartition.lrmGeneric(arr, N);
        end = System.nanoTime();
        long lrmTime = (end - start) / 1000;

        // --- Write results ---
        writer.write(String.format("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d%n",
                instanceID,
                inst.M, inst.N, inst.B, inst.optimalSum,
                maxGroupSum(ls), lsTime,
                maxGroupSum(lpt), lptTime,
                maxGroupSum(mf), mfTime,
                maxGroupSum(lrm), lrmTime
        ));
        writer.flush();
    }

    /**
     * Utility method to get the maximum group sum (makespan).
     */
    private static int maxGroupSum(List<List<Integer>> groups) {
        int max = 0;
        for (List<Integer> g : groups) {
            int sum = g.stream().mapToInt(Integer::intValue).sum();
            if (sum > max) max = sum;
        }
        return max;
    }


}
