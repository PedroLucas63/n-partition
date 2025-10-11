#ifndef READINSTANCES_HPP
#define READINSTANCES_HPP

#include <vector>
#include <string>

namespace ReadInstances {

const std::string INSTANCE_PATH = "../instances/optimal_n_partition_instances.txt";

/**
 * @brief Structure to store one instance's data.
 */
struct InstanceData {
    int N;                   // Number of elements
    int K;                   // Number of partitions
    int B;                   // Number of bits used in number generation
    int OPTIMAL_SUM;          // Known optimal sum per partition
    std::vector<int> values; // List of generated numbers
};

/**
 * @brief Reads all instances from the specified file.
 * 
 * Each instance has the following format:
 *   # Instance X
 *   N K B OPTIMAL_SUM
 *   num1 num2 num3 ...
 * 
 * @param filePath Path to the instance file.
 * @return std::vector<InstanceData> A vector containing all instances.
 */
std::vector<InstanceData> readInstances(const std::string &filePath = INSTANCE_PATH);

} // namespace ReadInstances

#endif // READINSTANCES_HPP
