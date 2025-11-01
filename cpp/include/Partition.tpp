#pragma once
#include <cmath>
#include <cstdint>
#include <numeric>
#include <queue>
#include <set>
#include <stdexcept>
#include <tuple>
#include <unordered_set>

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

template <unsigned n>
std::array<std::vector<int>, n> CGA(std::vector<int> &arr) {
  // Check if n is valid
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  // Get one solution
  auto groups = LPT<n>(arr);

  // Get makespan
  std::array<int, n> sums;
  std::transform(groups.begin(), groups.end(), sums.begin(),
                 [](const std::vector<int> &group) {
                   return std::accumulate(group.begin(), group.end(), 0);
                 });
  int makespan = *std::max_element(sums.begin(), sums.end());

  // Get best solution
  std::array<int, n> groupSums = {};
  std::array<std::vector<int>, n> actualGroups = {};

  CGABacktracking<n>(arr, actualGroups, groupSums, makespan, groups, 0);

  return groups;
}

template <unsigned n>
void CGABacktracking(const std::vector<int> &arr,
                     std::array<std::vector<int>, n> &groups,
                     std::array<int, n> &groupSums, int &makespan,
                     std::array<std::vector<int>, n> &groupsCandidate, int i) {
  // Base case
  if (i == arr.size()) {
    int currentMax = *std::max_element(groupSums.begin(), groupSums.end());
    // Update
    if (currentMax < makespan) {
      makespan = currentMax;
      groupsCandidate = groups;
    }
    return;
  }

  // Sort groups (greedy)
  std::array<int, n> groupsIndices;
  std::iota(groupsIndices.begin(), groupsIndices.end(), 0);
  std::sort(groupsIndices.begin(), groupsIndices.end(),
            [&groupSums](int i, int j) { return groupSums[i] < groupSums[j]; });

  // Backtracking
  std::unordered_set<int> triedSums;
  for (int j : groupsIndices) {
    // Not already tried
    if (triedSums.count(groupSums[j])) {
      continue;
    }
    triedSums.insert(groupSums[j]);

    // Evaluation
    groupSums[j] += arr[i];
    int currentMax = *std::max_element(groupSums.begin(), groupSums.end());

    // Prune
    if (currentMax < makespan) {
      // Recursion
      groups[j].push_back(arr[i]);
      CGABacktracking<n>(arr, groups, groupSums, makespan, groupsCandidate,
                         i + 1);
      groups[j].pop_back();
    }

    groupSums[j] -= arr[i];
  }
}

} // namespace partition
