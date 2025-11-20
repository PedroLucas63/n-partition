#ifndef READINSTANCES_HPP
#define READINSTANCES_HPP

#include <vector>
#include <string>
#include "Partition.hpp"

namespace ReadInstances {

const std::string INSTANCE_PATH = "../instances/random.txt";

/**
 * @brief Structure to store one instance's data.
 */
struct InstanceData {
    int M;                   // Number of elements
    int N;                   // Number of partitions
    int B;                   // Number of bits used in number generation
    partition::ValueType optimalSum;          // Known optimal sum per partition
    std::vector<partition::ValueType> values; // List of generated numbers
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


/**
 * @brief Prints all instances to the console for verification.
 * 
 * @param instances A vector of InstanceData to print.
 */
void printInstances(const std::vector<InstanceData>& instances);

} // namespace ReadInstances

#endif // READINSTANCES_HPP
