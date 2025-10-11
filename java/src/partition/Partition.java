package partition;

import java.util.*;

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
     * Partitions a list of integers into {@code n} groups using a List Scheduling approach.
     *
     * <p>The method iteratively assigns each integer to the group
     * with the current minimum sum. This does not guarantee an optimal solution,
     * but it produces a reasonably balanced distribution in practice.</p>
     *
     * @param arr the list of integers to be partitioned
     * @param n the number of groups (must be greater than zero)
     * @return a list containing {@code n} sublists, each representing a group
     * @throws IllegalArgumentException if {@code n <= 0}
     */
    public static List<List<Integer>> LS(List<Integer> arr, int n) throws IllegalArgumentException {
        if (n <= 0) {
            throw new IllegalArgumentException("K must be a positive integer");
        } else if (n == 1) {
            return List.of(new ArrayList<>(arr));
        }

        // Initialize groups and their sums
        List<List<Integer>> groups = new ArrayList<>(n);
        var pq = new PriorityQueue<int[]>(Comparator.comparingInt(a -> a[0]));

        for (int i = 0; i < n; i++) {
            groups.add(new ArrayList<>());
            pq.add(new int[]{0, i});
        }

        // Distribute elements greedily
        for (int x : arr) {
            int[] top = pq.poll();
            assert top != null;
            int sum = top[0], idx = top[1];
            groups.get(idx).add(x);
            pq.add(new int[]{sum + x, idx});
        }

        return groups;
    }

    /**
     * Applies the Longest Processing Time (LPT) heuristic to partition a list of integers
     * into {@code n} groups.
     *
     * <p>The method first sorts the list in descending order (largest numbers first),
     * then delegates to the {@link #LS(List, int)} method to distribute the elements.
     * This heuristic is commonly used in load balancing and scheduling problems.</p>
     *
     * @param arr the list of integers to be partitioned
     * @param n the number of groups (must be greater than zero)
     * @return a list containing {@code n} sublists, each representing a group
     * @throws IllegalArgumentException if {@code n <= 0}
     */
    public static List<List<Integer>> LPT(List<Integer> arr, int n) throws IllegalArgumentException {
        if (n <= 0) {
            throw new IllegalArgumentException("n must be a positive integer");
        } else if (n == 1) {
            return List.of(new ArrayList<>(arr));
        }

        // Sort in descending order (largest elements first)
        arr.sort(Comparator.reverseOrder());

        // Delegate to the greedy algorithm
        return LS(arr, n);
    }

    /**
     * Applies the MULTIFIT heuristic to partition a list of integers into {@code n} groups.
     *
     * <p>This method provides a simplified interface that uses a default of seven binary
     * search iterations to estimate the optimal bin capacity. It delegates to the
     * {@link #MULTIFIT(List, int, int)} method for the actual computation.</p>
     *
     * <p>The MULTIFIT algorithm is a hybrid approach that combines binary search with
     * the First-Fit Decreasing (FFD) heuristic, often used in bin packing and load
     * balancing problems. It aims to find the smallest possible bin capacity such that
     * all elements can be packed into {@code n} bins.</p>
     *
     * @param arr the list of integers to be partitioned
     * @param n the number of groups (bins) to create (must be greater than zero)
     * @return a list of {@code n} sublists, each representing a group
     * @throws IllegalArgumentException if {@code n <= 0}
     * @see #MULTIFIT(List, int, int)
     * @see #FFD(List, int)
     */
    public static List<List<Integer>> MULTIFIT(List<Integer> arr, int n) throws IllegalArgumentException {
        return MULTIFIT(arr, n, 7);
    }

    /**
     * Applies the MULTIFIT heuristic with a configurable number of binary search iterations.
     *
     * <p>The MULTIFIT algorithm iteratively adjusts the bin capacity between lower and
     * upper bounds. In each iteration, it applies the {@link #FFD(List, int)} method
     * (First-Fit Decreasing) to test whether all items can fit into {@code n} bins
     * with the current capacity. The search continues until the best feasible
     * capacity is found.</p>
     *
     * <p>The algorithm was first introduced by Coffman, Garey, and Johnson (1978)
     * and is known for providing a good approximation for the bin packing problem.</p>
     *
     * @param arr the list of integers to be partitioned
     * @param n the number of bins to use (must be greater than zero)
     * @param k the number of binary search iterations (default is typically 7)
     * @return a list of sublists, where each sublist represents one bin or group
     * @throws IllegalArgumentException if {@code n <= 0}
     * @see #FFD(List, int)
     */
    public static List<List<Integer>> MULTIFIT(List<Integer> arr, int n, int k) throws IllegalArgumentException {
        if (n <= 0) {
            throw new IllegalArgumentException("n must be a positive integer");
        } else if (n == 1) {
            return List.of(new ArrayList<>(arr));
        }

        arr.sort(Comparator.reverseOrder());

        int sum = 0, max = 0;
        for (int x : arr) {
            sum += x;
            max = Math.max(max, x);
        }

        int lowerBound = Math.max(max, sum / n);
        int upperBound = Math.max(max, 2 * sum / n);

        List<List<Integer>> bestGroups = new ArrayList<>();

        for (int i = 0; i < k; i++) {
            int capacity = (lowerBound + upperBound) / 2;
            var groups = FFD(arr, capacity);

            if (groups.size() > n) {
                lowerBound = capacity;
            } else {
                bestGroups = groups;
                upperBound = capacity;
            }
        }

        return bestGroups;
    }

    /**
     * Applies the First-Fit Decreasing (FFD) heuristic to partition a list of integers
     * into groups with a given capacity.
     *
     * <p>The algorithm first considers each item in descending order (as provided),
     * and assigns it to the first bin that has enough remaining capacity.
     * If no such bin exists, a new bin is created. This greedy approach
     * is efficient and widely used for bin packing problems.</p>
     *
     * @param arr the list of integers to be partitioned
     * @param capacity the maximum capacity allowed per bin
     * @return a list of sublists, each representing a bin containing one or more items
     * @see #MULTIFIT(List, int, int)
     */
    public static List<List<Integer>> FFD(List<Integer> arr, int capacity) {
        record Bin(int remaining, int idx) implements Comparable<Bin> {
            @Override
            public int compareTo(Bin o) {
                return Integer.compare(remaining, o.remaining);
            }
        }

        List<List<Integer>> groups = new ArrayList<>();
        TreeSet<Bin> bins = new TreeSet<>();

        for (int x : arr) {
            Bin it = bins.ceiling(new Bin(x, 0));

            if (it == null) {
                groups.add(new ArrayList<>(x));
                bins.add(new Bin(capacity - x, groups.size() - 1));
            } else {
                groups.get(it.idx).add(x);
                bins.remove(it);
                bins.add(new Bin(it.remaining - x, it.idx));
            }
        }

        return groups;
    }
}
