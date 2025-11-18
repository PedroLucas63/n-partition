#ifndef PARTITION_HPP
#define PARTITION_HPP

#include <algorithm>
#include <array>
#include <vector>

namespace partition {
/**
 * @brief Template function to partition a given array into n groups.
 *
 * @param n The number of groups to partition the array into.
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <int n> std::array<std::vector<int>, n> LS(std::vector<int> &arr);

/**
 * @brief Template function to partition a given array into n groups.
 * @param n The number of groups to partition the array into.
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <int n> std::array<std::vector<int>, n> LPT(std::vector<int> &arr);

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
template <int n>
std::array<std::vector<int>, n> MULTIFIT(std::vector<int> &arr, int k = 7);

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
std::vector<std::vector<int>> FFD(std::vector<int> &arr, int capacity);

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
template <int n> std::array<std::vector<int>, n> CGA(std::vector<int> &arr);

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
template <int n>
void CGABacktracking(const std::vector<int> &arr,
                     std::array<std::vector<int>, n> &groups,
                     std::array<int, n> &groupSums, int &makespan,
                     int &lowerbound,
                     std::array<std::vector<int>, n> &groupsCandidate, int i);


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
template <int n>
std::array<std::vector<int>, n> geneticAlgorithm(std::vector<int> &arr);
} // namespace partition

#include "Partition.tpp"

#endif // PARTITION_HPP
