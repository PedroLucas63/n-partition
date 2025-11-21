#ifndef PARTITION_HPP
#define PARTITION_HPP

#include <algorithm>
#include <array>
#include <vector>
#include <cstdint>

namespace partition {

// Define ValueType as uint64_t;
using ValueType = uint64_t;

/**
 * @brief Template function to partition a given array into n groups.
 *
 * @param n The number of groups to partition the array into.
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <std::size_t n>
std::array<std::vector<ValueType>, n> LS(std::vector<ValueType> &arr);

/**
 * @brief Template function to partition a given array into n groups.
 * @param n The number of groups to partition the array into.
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <std::size_t n>
std::array<std::vector<ValueType>, n> LPT(std::vector<ValueType> &arr);

/**
 * @brief Template function to partition a given array into n groups using a
 * multifit approach.
 *
 * This function implements a dynamic programming approach to find the optimal
 * partition of the array into n groups.
 *
 * @param n The number of groups to partition the array into.
 * @param arr The array to partition.
 * @param k The number of iterations to run the algorithm (default is 7).
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <std::size_t n>
std::array<std::vector<ValueType>, n> MULTIFIT(std::vector<ValueType> &arr,
                                               std::size_t k = 7);

/**
 * @brief Template function to partition a given array into groups using the
 * FFD algorithm.
 *
 * This function implements the FFD algorithm to find the optimal partition of
 * the array into groups.
 *
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
std::vector<std::vector<ValueType>> FFD(std::vector<ValueType> &arr,
                                        ValueType capacity);

/**
 * @brief Template function to partition a given array into n groups using a
 * Complete Greedy Algorithm (CGA) approach.
 *
 * This function implements a complete greedy algorithm to find the optimal
 * partition of the array into n groups.
 *
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <std::size_t n>
std::array<std::vector<ValueType>, n> CGA(std::vector<ValueType> &arr);

/**
 * @brief A backtracking algorithm to find the optimal partition of the array
 * into n groups using a Complete Greedy Algorithm (CGA) approach.
 *
 * This function implements a backtracking algorithm to find the optimal
 * partition of the array into n groups. It uses a complete greedy
 * algorithm to find the optimal partition.
 *
 * @param arr The array to partition.
 * @param groups The current partition of the array.
 * @param groupSums The sum of each group in the current partition.
 * @param makespan The maximum difference between the sums of the groups.
 * @param lowerbound The lower bound of the makespan.
 * @param groupsCandidate The current candidate partition.
 * @param i The current index in the array.
 */
template <std::size_t n>
void CGABacktracking(const std::vector<ValueType> &arr,
                     std::array<std::vector<ValueType>, n> &actualGroups,
                     std::array<ValueType, n> &groupSums, ValueType &makespan,
                     ValueType &lowerbound,
                     std::array<std::vector<ValueType>, n> &groupsCandidate,
                     std::size_t i);

/**
 * @brief Template function to partition a given array into n groups using a
 * genetic algorithm approach.
 *
 * This function implements a genetic algorithm to find the optimal partition
 * of the array into n groups.
 *
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <std::size_t n>
std::array<std::vector<ValueType>, n>
geneticAlgorithm(std::vector<ValueType> &arr);

template <std::size_t n>
std::array<std::vector<ValueType>, n>
geneticAlgorithm2(std::vector<ValueType> &arr);
} // namespace partition

#include "Partition.tpp"

#endif // PARTITION_HPP
