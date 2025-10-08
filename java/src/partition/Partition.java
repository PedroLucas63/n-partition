package partition;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 * Utility class for partitioning a list of integers into {@code k} groups
 * using a greedy (approximate) strategy.
 *
 * <p>The algorithm works as follows:
 * each element from the input list is assigned to the group
 * that currently has the smallest sum, in order to balance the groups.</p>
 *
 * <p>Example usage:</p>
 * <pre>{@code
 * List<Integer> numbers = List.of(10, 20, 30, 40, 50);
 * List<List<Integer>> groups = Partition.greedy(numbers, 3);
 * }</pre>
 *
 * The result will be a list of 3 groups with approximately balanced sums.
 */
public class Partition {

    /**
     * Partitions a list of integers into {@code k} groups using a greedy approach.
     *
     * <p>The method iteratively assigns each integer to the group
     * with the current minimum sum. This does not guarantee an optimal solution,
     * but it produces a reasonably balanced distribution in practice.</p>
     *
     * @param data the list of integers to be partitioned
     * @param k the number of groups (must be greater than zero)
     * @return a list containing {@code k} sublists, each representing a group
     * @throws IllegalArgumentException if {@code k <= 0}
     */
    public static List<List<Integer>> greedy(List<Integer> data, int k) throws IllegalArgumentException {
        if (k <= 0) {
            throw new IllegalArgumentException("K must be a positive integer");
        } else if (k == 1) {
            List<List<Integer>> singleGroup = new ArrayList<>();
            singleGroup.add(new ArrayList<>(data));
            return singleGroup;
        }

        // Initialize groups and their sums
        List<List<Integer>> groups = new ArrayList<>(k);
        List<Integer> sums = new ArrayList<>(k);

        for (int i = 0; i < k; i++) {
            groups.add(new ArrayList<>());
            sums.add(0);
        }

        // Distribute elements greedily
        for (int x : data) {
            int i = 0;
            int minSum = sums.getFirst();

            for (int j = 1; j < k; j++) {
                if (sums.get(j) < minSum) {
                    i = j;
                    minSum = sums.get(j);
                }
            }

            groups.get(i).add(x);
            sums.set(i, sums.get(i) + x);
        }

        return groups;
    }

    /**
     * Applies the Longest Processing Time (LPT) heuristic to partition a list of integers
     * into {@code k} groups.
     *
     * <p>The method first sorts the list in descending order (largest numbers first),
     * then delegates to the {@link #greedy(List, int)} method to distribute the elements.
     * This heuristic is commonly used in load balancing and scheduling problems.</p>
     *
     * @param data the list of integers to be partitioned
     * @param k the number of groups (must be greater than zero)
     * @return a list containing {@code k} sublists, each representing a group
     * @throws IllegalArgumentException if {@code k <= 0}
     */
    public static List<List<Integer>> lpt(List<Integer> data, int k) throws IllegalArgumentException {
        if (k <= 0) {
            throw new IllegalArgumentException("K must be a positive integer");
        } else if (k == 1) {
            List<List<Integer>> singleGroup = new ArrayList<>();
            singleGroup.add(new ArrayList<>(data));
            return singleGroup;
        }

        // Sort in descending order (largest elements first)
        data.sort(Comparator.reverseOrder());

        // Delegate to the greedy algorithm
        return greedy(data, k);
    }
}
