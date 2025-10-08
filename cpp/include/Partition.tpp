#pragma once
#include <cmath>

namespace partition {

template <unsigned K>
std::array<std::vector<int>, K> greedy(std::vector<int> &arr) {
  if (K <= 0) {
    throw std::invalid_argument("K must be a positive integer");
  } else if (K == 1) {
    return {{arr}};
  }

  std::array<std::vector<int>, K> groups;
  std::array<int, K> sums{};

  for (auto &x : arr) {
    int i = 0;
    int minSum = sums[0];

    for (int j = 1; j < K; j++) {
      if (sums[j] < minSum) {
        i = j;
        minSum = sums[j];
      }
    }

    groups[i].push_back(x);
    sums[i] += x;
  }

  return groups;
}

template <unsigned K>
std::array<std::vector<int>, K> lpt(std::vector<int> &arr) {
  if (K <= 0) {
    throw std::invalid_argument("K must be a positive integer");
  } else if (K == 1) {
    return {{arr}};
  }

  std::sort(arr.begin(), arr.end(), std::greater<int>());
  return greedy<K>(arr);
}
} // namespace partition
