#include "Partition.hpp"
#include <iostream>
#include <numeric>
#include <random>

/// @brief Overload the << operator for vectors of integers.
/// @param os Output stream.
/// @param v Vector of integers.
/// @return Output stream.
std::ostream &operator<<(std::ostream &os, const std::vector<int> &v) {
  os << "[";
  for (auto &x : v) {
    os << x << " ";
  }
  os << "\b]";
  return os;
}

/**
 * @brief Print a groups array and a name string.
 *
 * @param groups A groups array containing the groups to print.
 * @param name A name string to print with the groups.
 *
 * This function prints the groups array with the corresponding name string.
 */
template <unsigned N>
void printGroups(const std::array<std::vector<int>, N> &groups,
                 const std::string &name) {
  std::cout << "\n=== " << name << " ===\n";

  for (int i = 0; i < N; i++) {
    int sum = std::accumulate(groups[i].begin(), groups[i].end(), 0);
    std::cout << "Group " << i << " (Sum: " << sum << "): " << groups[i]
              << "\n";
  }
}

/**
 * @brief Main function.
 *
 * This function generates N random numbers between 1 and N*100000,
 * distributes them between N groups, and then applies two different
 * algorithms (Greedy, LPT and Multifit) to find the optimal partition
 * of the numbers.
 */
int main(int, char **) {
  constexpr unsigned N = 3;
  constexpr unsigned MAX_OPTIMAL_SUM = 1000;
  std::vector<int> arr;

  std::random_device rd;
  std::mt19937 rng(rd());
  std::uniform_int_distribution<int> dist(N, N * MAX_OPTIMAL_SUM);
  int optimalSum = dist(rng) / N;

  for (int i = 0; i < N; i++) {
    int objectiveSum = optimalSum;

    while (objectiveSum != 0) {
      std::uniform_int_distribution<int> dist(1, objectiveSum);
      int x = dist(rng);
      arr.push_back(x);
      objectiveSum -= x;
    }
  }

  std::cout << "Data: " << arr << "\n";
  std::cout << "Optimal sum: " << optimalSum << "\n";

  auto ls = partition::LS<N>(arr);
  auto lpt = partition::LPT<N>(arr);
  auto mf = partition::MULTIFIT<N>(arr);

  printGroups<N>(ls, "List Scheduling");
  printGroups<N>(lpt, "Least Processing Time");
  printGroups<N>(mf, "MULTIFIT");

  return 0;
}
