#include <iostream>
#include "partition.hpp" 
#include "ReadInstances.hpp"
#include <fstream>
#include <chrono>

/**
 * @brief Writes the partitioned groups and their sums to a CSV file.
 * 
 * @param os The output stream to write to.
 * @param instanceID The ID of the instance.
 * @param N The number of elements in the instance.
 * @param Kval The number of partitions in the instance.
 * @param B The bit size used in the instance.
 * @param groups The partitioned groups.
 * @param algorithmName The name of the algorithm used.
 * @param timeMicroseconds The time taken by the algorithm in microseconds.
 */
template <size_t K>
void writeGroupsCSV(std::ostream &os, size_t instanceID, int N, int Kval, int B, 
                    const std::array<std::vector<int>, K> &groups, const std::string &algorithmName,
                    long long timeMicroseconds) {
    int makespan = 0;
    os << instanceID << "," << N << "," << Kval << "," << B << "," << algorithmName;

    for (size_t i = 0; i < K; ++i) {
        int sum = 0;
        for (auto &x : groups[i]) sum += x;
        if (sum > makespan) makespan = sum;
        os << "," << sum;
    }

    os << "," << makespan << "," << timeMicroseconds << "\n";
}


/**
 * @brief Macro to generate switch cases for different template instantiations of K.
 * 
 * @param KVALUE The template value K.
 * @param ARR The array/vector to be partitioned.
 * @param INSTANCEID The instance ID for printing.
 * @param NVAL The N value of the instance.
 * @param KVAL The K value of the instance.
 * @param BVAL The B value of the instance.
 * @param OS The output stream to print results to.
 * 
 */

#define RUN_FOR_K_CSV(KVALUE, ARR, INSTANCEID, NVAL, KVAL, BVAL, OS) \
    case KVALUE: { \
        auto start = std::chrono::high_resolution_clock::now(); \
        auto g = partition::greedy<KVALUE>(ARR); \
        auto end = std::chrono::high_resolution_clock::now(); \
        auto greedyTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count(); \
        \
        start = std::chrono::high_resolution_clock::now(); \
        auto l = partition::lpt<KVALUE>(ARR); \
        end = std::chrono::high_resolution_clock::now(); \
        auto lptTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count(); \
        \
        start = std::chrono::high_resolution_clock::now(); \
        auto m = partition::multifit<KVALUE>(ARR); \
        end = std::chrono::high_resolution_clock::now(); \
        auto multifitTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count(); \
        \
        writeGroupsCSV(OS, INSTANCEID, NVAL, KVAL, BVAL, g, "Greedy", greedyTime); \
        writeGroupsCSV(OS, INSTANCEID, NVAL, KVAL, BVAL, l, "LPT", lptTime); \
        writeGroupsCSV(OS, INSTANCEID, NVAL, KVAL, BVAL, m, "Multifit", multifitTime); \
        break; \
    }

/**
 * @brief Class responsible for running partitioning experiments on multiple instances.
 * 
 * Reads instances from a file, executes the partitioning algorithms for each instance,
 * and prints the results to the console.
 * 
 * @patam outputFileName The name of the CSV file to write results to.
 */
class ExperimentRunner {
    std::ofstream outFile;  // CSV output file stream

public:
    ExperimentRunner(const std::string &outputFileName = "results.csv")
        : outFile(outputFileName, std::ios::out)
    {
        if (!outFile.is_open()) {
            throw std::runtime_error("Failed to open output file.");
        }

        // write CSV header
        outFile << "InstanceID,N,K,B,Algorithm";
        for (int i = 1; i <= 16; ++i) outFile << ",Group" << i << "Sum";
        outFile << ",Makespan,Time(us)\n"; 

    }

    void run() {
        auto instances = ReadInstances::readInstances();
        for (size_t i = 0; i < instances.size(); ++i) {
            runInstance(instances[i], i + 1);
        }
    }

private:
    void runInstance(ReadInstances::InstanceData &instance, size_t id) {
        runAlgorithmsByK(instance.K, instance.values, id, instance.N, instance.K, instance.B, outFile);
    }

    void runAlgorithmsByK(int K, std::vector<int> &arr, size_t instanceID, int Nval, int Kval, int Bval, std::ostream &os) {
        switch (K) {
            RUN_FOR_K_CSV(2, arr, instanceID, Nval, Kval, Bval, os)
            RUN_FOR_K_CSV(3, arr, instanceID, Nval, Kval, Bval, os)
            RUN_FOR_K_CSV(4, arr, instanceID, Nval, Kval, Bval, os)
            RUN_FOR_K_CSV(8, arr, instanceID, Nval, Kval, Bval, os)
            RUN_FOR_K_CSV(16, arr, instanceID, Nval, Kval, Bval, os)
            default:
                os << "[WARN] Unsupported K = " << K << "\n";
        }
    }
};
