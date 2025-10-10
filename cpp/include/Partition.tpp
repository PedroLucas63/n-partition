#pragma once
#include <cmath>
#include <stdexcept>

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

template <unsigned K>
std::array<std::vector<int>, K> multifit(std::vector<int> &arr) {
  if (K <= 0) {
    throw std::invalid_argument("K must be a positive integer");
  } else if (K == 1) {
    return {{arr}};
  }

  std::sort(arr.begin(), arr.end(), std::greater<int>());

  int sum = 0, max = 0;
  for (auto &x : arr) {
    sum += x;
    max = std::max(max, x);
  }

  unsigned lowerbound = std::max<unsigned>(max, sum / K);
  unsigned upperbound = 2 * sum / K;

  std::vector<std::vector<int>> bestGroups;

  while (upperbound - lowerbound > 1) {
    unsigned capacity = (lowerbound + upperbound) / 2;
    auto groups = ffd(arr, capacity);

    if (groups.size() > K) {
      lowerbound = capacity + 1;
    } else {
      bestGroups = groups;
      upperbound = capacity;
    }
  }

  std::array<std::vector<int>, K> finalGroups;
  for (int i = 0; i < K; i++) {
    finalGroups[i] = bestGroups[i];
  }
  return finalGroups;
}

std::vector<std::vector<int>> ffd(std::vector<int> &arr, unsigned capacity) {
  std::vector<std::vector<int>> groups;
  std::vector<int> sums{};

  for (auto &x : arr) {
    int i = -1;

    for (int j = 0; j < groups.size(); j++) {
      if (sums[j] + x <= capacity) {
        i = j;
        break;
      }
    }

    if (i == -1) {
      groups.push_back({x});
      sums.push_back(x);
    } else {
      groups[i].push_back(x);
      sums[i] += x;
    }
  }

  return groups;
}
} // namespace partition
