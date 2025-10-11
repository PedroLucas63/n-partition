#pragma once
#include <cmath>
#include <queue>
#include <set>
#include <stdexcept>
#include <tuple>

namespace partition {

template <unsigned n>
std::array<std::vector<int>, n> LS(std::vector<int> &arr) {
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  std::array<std::vector<int>, n> groups;

  using queue_element = std::pair<int, int>; // {sum, index}
  auto cmp = [](const queue_element &a, const queue_element &b) {
    return a.first > b.first;
  };
  std::priority_queue<queue_element, std::vector<queue_element>, decltype(cmp)>
      pq(cmp);

  for (int i = 0; i < n; i++) {
    pq.push({0, i});
  }

  for (auto &x : arr) {
    auto [sum, i] = pq.top();
    pq.pop();
    groups[i].push_back(x);
    pq.push({sum + x, i});
  }

  return groups;
}

template <unsigned n>
std::array<std::vector<int>, n> LPT(std::vector<int> &arr) {
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  std::sort(arr.begin(), arr.end(), std::greater<int>());
  return LS<n>(arr);
}

template <unsigned n>
std::array<std::vector<int>, n> MULTIFIT(std::vector<int> &arr, unsigned k) {
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  std::sort(arr.begin(), arr.end(), std::greater<int>());

  int sum = 0, max = 0;
  for (auto &x : arr) {          
    sum += x;
    max = std::max(max, x);
  }

  unsigned lowerBound = std::max<unsigned>(max, sum / n);
  unsigned upperBound = std::max<unsigned>(max, 2 * sum / n);

  std::vector<std::vector<int>> bestGroups;

  for (int i = 0; i < k; i++) {
    unsigned capacity = (lowerBound + upperBound) / 2;
    auto groups = FFD(arr, capacity);

    if (groups.size() > n) {
      lowerBound = capacity;
    } else {
      bestGroups = groups;
      upperBound = capacity;
    }
  }

  std::array<std::vector<int>, n> finalGroups;
  for (int i = 0; i < n; i++) {
    finalGroups[i] = bestGroups[i];
  }
  return finalGroups;
}

std::vector<std::vector<int>> FFD(std::vector<int> &arr, unsigned capacity) {
  struct Bin {
    unsigned remaining;
    unsigned idx;
    bool operator<(const Bin &other) const {
      return remaining < other.remaining;
    }
  };

  std::vector<std::vector<int>> groups;
  std::multiset<Bin> bins;

  for (auto &x : arr) {
    // First bin with remaining capacity >= x
    auto it = bins.lower_bound(Bin{unsigned(x), unsigned(0)});

    // No bin with remaining capacity >= x
    if (it == bins.end()) {
      groups.push_back({x});
      bins.insert(Bin{capacity - x, unsigned(groups.size() - 1)});
    } else {
      // Bin with remaining capacity >= x
      groups[it->idx].push_back(x);
      Bin newBin{it->remaining - x, it->idx};
      bins.erase(it);
      bins.insert(newBin);
    }
  }

  return groups;
}
} // namespace partition
