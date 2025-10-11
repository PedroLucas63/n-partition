import partition.LRMPartition;
import partition.Partition;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Demonstration class for testing the Partition algorithms (Greedy and LPT).
 *
 * <p>This program generates a random list of integers such that the sum of each
 * group is approximately equal to a target "optimal sum". It then applies both
 * the Greedy and LPT (Longest Processing Time) heuristics to partition the data
 * into {@code K} groups, and prints the results.</p>
 */
public class Main {

    public static void main(String[] args) {
        final int n = 3;
        final int MAX_OPTIMAL_SUM = 1000;

        var random = new Random();
        int optimalSum = random.nextInt(n, n * MAX_OPTIMAL_SUM + 1) / n;
        var data = new ArrayList<Integer>();

        for (int i = 0; i < n; i++) {
            int objectiveSum = optimalSum;
            while (objectiveSum > 0) {
                int x = random.nextInt(1, objectiveSum + 1);
                data.add(x);
                objectiveSum -= x;
            }
        }

        System.out.println("Data: " + data);
        System.out.println("Optimal sum: " + optimalSum);

        // ------------------- Greedy -------------------
        long start = System.nanoTime();
        var ls = Partition.LS(data, n);
        long end = System.nanoTime();
        printGroups(ls, "List Scheduling");
        System.out.println("List Scheduling time: " + (end - start) / 1_000_000.0 + " ms");

        // ------------------- LPT -------------------
        start = System.nanoTime();
        var lpt = Partition.LPT(data, n);
        end = System.nanoTime();
        printGroups(lpt, "Least Processing Time");
        System.out.println("Least Processing Time time: " + (end - start) / 1_000_000.0 + " ms");

        // ------------------- MULTIFIT -------------------
        start = System.nanoTime();
        var mf = Partition.MULTIFIT(data, n);
        end = System.nanoTime();
        printGroups(lpt, "MULTIFIT");
        System.out.println("MULTIFIT time: " + (end - start) / 1_000_000.0 + " ms");

        // ------------------- LRM Generic -------------------
        start = System.nanoTime();
        var e = LRMPartition.lrmGeneric(data, n);
        end = System.nanoTime();
        printGroups(e, "LRM Generic");
        System.out.println("LRM Generic time: " + (end - start) / 1_000_000.0 + " ms");


    }

    /**
     * Utility method to print the groups and their sums.
     *
     * @param data the partitioned groups
     * @param name the algorithm name (for labeling output)
     */
    private static void printGroups(List<List<Integer>> data, String name) {
        System.out.println("\n=== " + name + " ===");
        for (int i = 0; i < data.size(); i++) {
            int sum = data.get(i).stream().reduce(Integer::sum).orElse(0);
            System.out.println("Group " + (i + 1) + " (Sum: " + sum + "): " + data.get(i));
        }
    }
}
