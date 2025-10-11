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
} // namespace partition

#include "Partition.tpp"

#endif // PARTITION_HPP
