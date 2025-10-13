import experiment.ExperimentRunner;

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
        String outputPath = "results/results.csv";
        ExperimentRunner.run(outputPath);
    }

}
