package partition;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class LRMPartition {

    /**
     * Applies the Longest-Remaining-Magnitude (LRM) heuristic to partition a list of integers
     * into {@code k} balanced groups.
     *
     * <p>The method first sorts the input list in descending order and distributes the numbers
     * into {@code k} batches in a round-robin manner. It then computes the sum (mean) of each batch
     * and delegates to the internal LRM procedure, which iteratively constructs the final {@code k} groups.</p>
     *
     * <p>The internal LRM distributes elements based on two strategies:
     * <ul>
     *   <li>Normal iteration: chooses the batch with the largest spread (max - min) and takes an element from it.</li>
     *   <li>Adjustment iteration: selects the batch whose first element is closest to the overall target mean,
     *       aiming to balance the group sums.</li>
     * </ul>
     * </p>
     *
     * <p>This heuristic is designed to reduce the spread of subset sums in balanced multi-way partitioning problems,
     * providing a more uniform distribution than naive greedy or LPT approaches.</p>
     *
     * @param numbers the list of integers to be partitioned
     * @param k the number of groups (must be greater than zero)
     * @return a list containing {@code k} sublists, each representing a balanced group
     */
    public static List<List<Integer>> lrmGeneric(List<Integer> numbers, int k) {
        List<Integer> sorted = new ArrayList<>(numbers);
        sorted.sort(Collections.reverseOrder());

        // Initialize k batches (p1, p2, p3, ...)
        List<LinkedList<Integer>> batches = new ArrayList<>();
        for (int i = 0; i < k; i++) {
            batches.add(new LinkedList<>());
        }

        for (int i = 0; i < sorted.size(); i++) {
            batches.get(i % k).add(sorted.get(i));
        }


        // Calculates the average (sum) of each batch
        List<Integer> means = new ArrayList<>();
        for (List<Integer> batch : batches) {
            int sum = batch.stream().mapToInt(Integer::intValue).sum();
            means.add(sum);
        }

        // Convert to List<List<Integer>> before calling the other LRM
        List<List<Integer>> data = new ArrayList<>(batches);

        return lrmGeneric(data, means, k);
    }

    /**
     * Internal LRM method that constructs the final groups from batches and their means.
     *
     * <p>This method iteratively distributes elements from the batches into {@code k} groups.
     * It alternates between normal iterations (maximizing spread reduction) and adjustment iterations
     * (balancing groups toward the target mean).</p>
     *
     * @param batches the list of {@code k} batches containing integers
     * @param means the precomputed sums of each batch
     * @param k the number of groups to create
     * @return a list containing {@code k} balanced groups
     */
    public static List<List<Integer>> lrmGeneric(List<List<Integer>> batches, List<Integer> means, int k) {

        int targetMean = means.stream().mapToInt(Integer::intValue).sum();

        // 1. Creates the final k groups
        List<List<Integer>> groups = new ArrayList<>();
        for (int i = 0; i < k; i++) {
            groups.add(new ArrayList<>());
        }

        boolean added;
        int iteration = 0;


        do {
            added = false;
            for (int i = 0; i < k; i++) {
                int batchIndex = -1;

                // If it is a normal round, choose the largest spread.
                if (iteration % k != 0) {
                    int maxSpread = Integer.MIN_VALUE;
                    for (int j = 0; j < batches.size(); j++) {
                        if (!batches.get(j).isEmpty()) {
                            int spread = Collections.max(batches.get(j)) - Collections.min(batches.get(j));
                            if (spread > maxSpread) {
                                maxSpread = spread;
                                batchIndex = j;
                            }
                        }
                    }
                }

                // If it is the “adjustment” round → choose the batch closest to the average
                else {
                    double minDiff = Double.MAX_VALUE;
                    for (int j = 0; j < batches.size(); j++) {
                        if (!batches.get(j).isEmpty()) {
                            int peekValue = batches.get(j).getFirst(); // first element of the batch
                            double diff = Math.abs(peekValue - targetMean);
                            if (diff < minDiff) {
                                minDiff = diff;
                                batchIndex = j;
                            }
                        }
                    }
                }

                // Adds the selected value to the current group
                if (batchIndex >= 0 && !batches.get(batchIndex).isEmpty()) {
                    int value = batches.get(batchIndex).removeFirst();
                    groups.get(i).add(value);
                    added = true;
                }
            }
            iteration++;
        } while (added);


        return groups;
    }


    /**
     * Applies the Longest-Remaining-Magnitude (LRM) heuristic to partition a list of integers
     * into {@code k} balanced groups.
     *
     * <p>The method sorts the input list in descending order and distributes the numbers into
     * {@code k} batches. It computes the sum of each batch and delegates to the internal LRM
     * procedure to construct the final groups.</p>
     *
     * @param numbers the list of integers to be partitioned
     * @param k the number of groups (must be greater than zero)
     * @return a list containing {@code k} balanced sublists
     * @throws IllegalArgumentException if {@code k <= 0}
     */
    public static List<List<Integer>> lrm(List<Integer> numbers, int k) {
        // Sort numbers descending
        List<Integer> sorted = new ArrayList<>(numbers);
        sorted.sort(Collections.reverseOrder());

        // Initialize k batches
        List<LinkedList<Integer>> batches = new ArrayList<>();
        for (int i = 0; i < k; i++) {
            batches.add(new LinkedList<>());
        }

        // Distribute numbers evenly into batches
        int batchSize = (int) Math.ceil((double) sorted.size() / k);
        for (int i = 0; i < sorted.size(); i++) {
            int batchIndex = i / batchSize;
            if (batchIndex >= k) batchIndex = k - 1;
            batches.get(batchIndex).add(sorted.get(i));
        }

        // Compute sum (mean) of each batch
        List<Integer> means = batches.stream()
                .map(batch -> batch.stream().mapToInt(Integer::intValue).sum())
                .collect(Collectors.toList());

        // Convert to List<List<Integer>> and call internal LRM
        List<List<Integer>> data = new ArrayList<>(batches);
        return lrm(data, means, k);
    }

    /**
     * Internal LRM procedure that builds the final groups using batch spreads and sums.
     *
     * <p>Each iteration selects the three main batches with the largest spreads (max - min),
     * removes elements from the ends of the first two batches, and chooses a compensating element
     * from the third batch that minimizes the difference to the target sum.</p>
     *
     * @param data the list of batches
     * @param means the sum of each batch
     * @param k the number of groups to create
     * @return a list containing {@code k} balanced groups
     */
    public static List<List<Integer>> lrm(List<List<Integer>> data, List<Integer> means, int k) {
        int sum = means.stream().mapToInt(Integer::intValue).sum();
        List<List<Integer>> groups = new ArrayList<>();

        while (groups.size() < k) {
            // 1. Compute spreads (max - min)
            List<Integer> spreads = data.stream()
                    .map(g -> g.isEmpty() ? 0 : Collections.max(g) - Collections.min(g))
                    .collect(Collectors.toList());

            // 2. Sort indices by spread (largest first)
            List<Integer> indices = IntStream.range(0, spreads.size())
                    .boxed()
                    .sorted((i, j) -> spreads.get(j) - spreads.get(i))
                    .collect(Collectors.toList());

            // 3. Select the three main batches
            LinkedList<Integer> p1 = new LinkedList<>(data.get(indices.get(0)));
            LinkedList<Integer> p2 = new LinkedList<>(data.get(indices.get(1)));
            LinkedList<Integer> p3 = new LinkedList<>(data.get(indices.get(2)));

            // 4. Remove elements from the ends
            int leftmost = p1.removeFirst();
            int rightmost = p2.removeLast();

            // 5. Choose the compensating element in p3
            int index = 0;
            int diff = Integer.MAX_VALUE;
            for (int i = 0; i < p3.size(); i++) {
                int currentDiff = Math.abs(leftmost + rightmost + p3.get(i) - sum);
                if (currentDiff < diff) {
                    diff = currentDiff;
                    index = i;
                }
            }
            int middle = p3.remove(index);

            // 6. Build the group
            List<Integer> group = new ArrayList<>();
            group.add(leftmost);
            group.add(middle);
            group.add(rightmost);
            groups.add(group);

            // 7. Update original batches
            data.set(indices.get(0), new ArrayList<>(p1));
            data.set(indices.get(1), new ArrayList<>(p2));
            data.set(indices.get(2), new ArrayList<>(p3));
        }

        return groups;
    }


}
