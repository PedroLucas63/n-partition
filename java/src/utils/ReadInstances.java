package utils;

import java.io.*;
import java.util.*;

public class ReadInstances {

    public static class InstanceData {
        public int M, N, B, optimalSum;
        public List<Integer> values = new ArrayList<>();

        @Override
        public String toString() {
            return String.format("Instance[M=%d, N=%d, B=%d, OPT=%d, values=%s]",
                    M, N, B, optimalSum, values);
        }
    }

    private static final String DEFAULT_PATH = "instances/optimal_m_partition_instances.txt";

    public static List<InstanceData> readInstances() throws IOException {
        return readInstances(DEFAULT_PATH);
    }

    public static List<InstanceData> readInstances(String filePath) throws IOException {
        File file = new File(filePath);
        if (!file.exists()) {
            file = new File("../" + filePath);
        }

        System.out.println("✅ File found: " + file.getAbsolutePath());
        return parseInstances(file);
    }

    private static List<InstanceData> parseInstances(File file) throws IOException {
        List<InstanceData> instances = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            InstanceData current = null;
            boolean expectingValues = false;

            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty()) continue;

                // Start of a new instance
                if (line.startsWith("#")) {
                    if (current != null && current.M > 0 && current.values.size() == current.M) {
                        instances.add(current);
                    }
                    current = new InstanceData();
                    expectingValues = false;
                    continue;
                }

                if (current == null) continue;

                // First non-comment line: parameters (M N B OPTIMAL_SUM)
                if (!expectingValues && current.M == 0) {
                    String[] parts = line.split("\\s+");
                    if (parts.length >= 4) {
                        try {
                            current.M = Integer.parseInt(parts[0]);
                            current.N = Integer.parseInt(parts[1]);
                            current.B = Integer.parseInt(parts[2]);
                            current.optimalSum = Integer.parseInt(parts[3]);
                            expectingValues = true;
                        } catch (NumberFormatException e) {
                            // Skip invalid parameter line
                            current = null;
                        }
                    }
                }
                // Second line: values
                else if (expectingValues) {
                    String[] nums = line.split("\\s+");
                    for (String num : nums) {
                        if (!num.trim().isEmpty()) {
                            try {
                                current.values.add(Integer.parseInt(num.trim()));
                            } catch (NumberFormatException e) {
                                // Skip invalid number
                            }
                        }
                    }

                    // After reading values, check if instance is complete
                    if (current.values.size() == current.M) {
                        instances.add(current);
                        current = null;
                        expectingValues = false;
                    }
                }
            }

            // Add the last instance if complete
            if (current != null && current.M > 0 && current.values.size() == current.M) {
                instances.add(current);
            }
        }

        System.out.printf("✅ Successfully read %d instances from %s%n", instances.size(), file.getName());
        return instances;
    }

    public static void printInstances(List<InstanceData> instances) {
        System.out.println("\n=== LOADED INSTANCES ===");
        for (int i = 0; i < instances.size(); i++) {
            InstanceData inst = instances.get(i);
            System.out.printf("Instance %d: M=%d, N=%d, B=%d, OPT=%d, values=%s%n",
                    i + 1, inst.M, inst.N, inst.B, inst.optimalSum, inst.values);
        }
    }
}