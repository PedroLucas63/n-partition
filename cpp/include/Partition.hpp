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
template <unsigned n> std::array<std::vector<int>, n> LS(std::vector<int> &arr);

/**
 * @brief Template function to partition a given array into n groups.
 * @param n The number of groups to partition the array into.
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <unsigned n>
std::array<std::vector<int>, n> LPT(std::vector<int> &arr);

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
template <unsigned n>
std::array<std::vector<int>, n> MULTIFIT(std::vector<int> &arr, unsigned k = 7);

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
std::vector<std::vector<int>> FFD(std::vector<int> &arr, unsigned capacity);

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
template <unsigned n>
std::array<std::vector<int>, n> CGA(std::vector<int> &arr);

/**
 * @brief Template function to partition a given array into n groups using a
 * Complete Greedy Algorithm with Backtracking (CGABacktracking) approach.
 *
 * This function implements a complete greedy algorithm with backtracking to
 * find the optimal partition of the array into n groups.
 *
 * @param arr The array to partition.
 * @param groups The groups to partition the array into.
 * @param groupSums The sums of each group.
 * @param i The current index of the array to process.
 * @param minSum The minimum sum of the groups found so far.
 * @return A pair containing the minimum sum of the groups and the partitioned
 * groups.
 */
template <unsigned n>
std::pair<int, std::array<std::vector<int>, n>>
CGABacktracking(std::vector<int> &arr, std::array<std::vector<int>, n> &groups,
                std::array<int, n> &groupSums, int i, int minSum);
} // namespace partition

#include "Partition.tpp"

#endif // PARTITION_HPP
