#ifndef PARTITION_HPP
#define PARTITION_HPP

#include <algorithm>
#include <array>
#include <vector>

namespace partition {
/**
 * @brief Template function to partition a given array into K groups.
 *
 * @param K The number of groups to partition the array into.
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <unsigned K>
std::array<std::vector<int>, K> greedy(std::vector<int> &arr);

/**
 * @brief Template function to partition a given array into K groups.
 * @param K The number of groups to partition the array into.
 * @param arr The array to partition.
 * @return An array of vectors containing the partitioned groups of the array.
 */
template <unsigned K>
std::array<std::vector<int>, K> lpt(std::vector<int> &arr);
} // namespace partition

#include "Partition.tpp"

#endif // PARTITION_HPP
