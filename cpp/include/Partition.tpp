#pragma once
#include <cmath>
#include <cstdint>
#include <numeric>
#include <queue>
#include <random>
#include <set>
#include <stdexcept>
#include <tuple>
#include <unordered_set>

namespace partition {

template <int n> std::array<std::vector<int>, n> LS(std::vector<int> &arr) {
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

template <int n> std::array<std::vector<int>, n> LPT(std::vector<int> &arr) {
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  std::sort(arr.begin(), arr.end(), std::greater<int>());
  return LS<n>(arr);
}

template <int n>
std::array<std::vector<int>, n> MULTIFIT(std::vector<int> &arr, int k) {
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  std::sort(arr.begin(), arr.end(), std::greater<int>());

  int sum = std::accumulate(arr.begin(), arr.end(), 0);
  int max = arr.front();

  int lowerBound = std::max<int>(max, sum / n);
  int upperBound = std::max<int>(max, 2 * sum / n);

  std::vector<std::vector<int>> bestGroups;

  for (int i = 0; i < k; i++) {
    int capacity = (lowerBound + upperBound) / 2;
    auto groups = FFD(arr, capacity);

    if (groups.size() > n) {
      lowerBound = capacity;
    } else {
      bestGroups = groups;
      upperBound = capacity;
    }
  }

  std::array<std::vector<int>, n> finalGroups;
  for (int i = 0; size_t(i) < bestGroups.size(); i++) {
    finalGroups[i] = bestGroups[i];
  }
  return finalGroups;
}

std::vector<std::vector<int>> FFD(std::vector<int> &arr, int capacity) {
  struct Bin {
    int remaining;
    int idx;
    bool operator<(const Bin &other) const {
      return remaining < other.remaining;
    }
  };

  std::vector<std::vector<int>> groups;
  std::multiset<Bin> bins;

  for (auto &x : arr) {
    // First bin with remaining capacity >= x
    auto it = bins.lower_bound(Bin{int(x), int(0)});

    // No bin with remaining capacity >= x
    if (it == bins.end()) {
      groups.push_back({x});
      bins.insert(Bin{capacity - x, int(groups.size() - 1)});
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

template <int n> std::array<std::vector<int>, n> CGA(std::vector<int> &arr) {
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

  // Get makespan lowerbound
  int total = std::accumulate(arr.begin(), arr.end(), 0);
  int lowerbound = total % n == 0 ? total / n : total / n + 1;

  // Get best solution
  if (lowerbound < makespan) {
    std::array<int, n> groupSums = {};
    std::array<std::vector<int>, n> actualGroups = {};
    CGABacktracking<n>(arr, actualGroups, groupSums, makespan, lowerbound,
                       groups, 0);
  }

  return groups;
}

template <int n>
void CGABacktracking(const std::vector<int> &arr,
                     std::array<std::vector<int>, n> &groups,
                     std::array<int, n> &groupSums, int &makespan,
                     int &lowerbound,
                     std::array<std::vector<int>, n> &groupsCandidate, int i) {
  // Base case
  if (size_t(i) == arr.size()) {
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

    // Uperbound prune
    if (currentMax < makespan) {
      // Recursion
      groups[j].push_back(arr[i]);
      CGABacktracking<n>(arr, groups, groupSums, makespan, lowerbound,
                         groupsCandidate, i + 1);
      groups[j].pop_back(); // Backtrack

      // Lowerbound prune
      if (makespan == lowerbound) {
        return;
      }
    }

    groupSums[j] -= arr[i];
  }
}

template <int n>
std::array<std::vector<int>, n> geneticAlgorithm(std::vector<int> &arr) {
  // --- Constantes ---
  const int QUEUE_MAX_SIZE = 10;
  const int INITIAL_POPULATION_SIZE = 4;
  const int CROSSOVER_FACTOR = 2;
  const int MUTATION_PROBABILITY = 20; // percentage
  const int MAX_GENERATIONS_WITHOUT_IMPROVEMENT = 5;
  const int MAX_MUTATION_SWAPS = 3; // safety cap

  using Individual = std::pair<std::vector<int>, int>; // (genes, fitness)

  // Menor fitness = melhor indivíduo
  auto cmp = [](const Individual &a, const Individual &b) {
    return a.second < b.second;
  };

  std::multiset<Individual, decltype(cmp)> population(cmp);

  // RNG único e distributions
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<double> dist01(0.0, 1.0);
  // dist for mutation decision (0..99)
  std::uniform_int_distribution<int> distPercent(0, 99);

  // --- Função auxiliar: makespan (usa o genes passado) ---
  auto calculateMakespan = [&](const std::vector<int> &genes) {
    std::vector<int> tmp = genes;
    auto solution = LS<n>(tmp);

    std::array<int, n> sums;
    for (int i = 0; i < n; ++i)
      sums[i] = std::accumulate(solution[i].begin(), solution[i].end(), 0);

    return *std::max_element(sums.begin(), sums.end());
  };

  // --- Adicionar indivíduo (com poda para QUEUE_MAX_SIZE) ---
  auto addIndividual = [&](const std::vector<int> &genes) {
    int fitness = calculateMakespan(genes);
    population.insert({genes, fitness});
    if ((int)population.size() > QUEUE_MAX_SIZE) {
      auto it = std::prev(population.end()); // pior indivíduo (maior fitness)
      population.erase(it);
    }
  };

  // --- Seleção por roleta --- auto selectParents = [&]() ->
  auto selectParents = [&]() -> std::pair<Individual, Individual> {
    std::vector<const Individual *> index;
    index.reserve(population.size());

    for (auto &ind : population)
      index.push_back(&ind);

    std::vector<double> weights;
    weights.reserve(index.size());
    for (auto ptr : index)
      weights.push_back(1.0 / (ptr->second + 1e-9));

    double totalWeight = std::accumulate(weights.begin(), weights.end(), 0.0);
    for (auto &w : weights)
      w /= totalWeight;

    auto roulette = [&](const Individual *exclude) {
      while (true) {
        double r = dist01(gen);
        double acc = 0.0;

        for (size_t i = 0; i < weights.size(); i++) {
          acc += weights[i];

          if (r <= acc) {
            if (exclude == nullptr || index[i] != exclude)
              return *index[i];
            break;
          }
        }
      }
    };

    Individual p1 = roulette(nullptr);
    Individual p2 = roulette(&p1);

    return {p1, p2};
  };

  // --- População inicial ---
  std::vector<int> work = arr;
  for (int i = 0; i < INITIAL_POPULATION_SIZE; ++i) {
    addIndividual(work);
    std::shuffle(work.begin(), work.end(), gen);
  }

  // garante que population não está vazia
  if (population.empty()) {
    std::vector<int> tmp = arr;
    return LS<n>(tmp);
  }

  // multiset com todos os elementos possíveis (para crossover)
  std::unordered_multiset<int> elements(arr.begin(), arr.end());

  // --- Crossover (uniform-like, preserva multiconjunto) ---
  auto crossover = [&](const Individual &p1, const Individual &p2) {
    size_t L = p1.first.size();
    std::vector<int> child(L, -1);

    std::unordered_multiset<int> available(elements);

    for (size_t i = 0; i < L; ++i) {
      int candidate = (i % 2 == 0 ? p1.first[i] : p2.first[i]);
      auto it = available.find(candidate);
      if (it != available.end()) {
        child[i] = candidate;
        available.erase(it);
      }
    }

    // preencher os buracos com restantes (ordem arbitrária, mas completa)
    for (auto e : available) {
      auto pos = std::find(child.begin(), child.end(), -1);
      if (pos != child.end())
        *pos = e;
    }

    return child;
  };

  // --- Mutação (limitada, evita loop infinito) ---
  auto mutation = [&](std::vector<int> genes) {
    if (distPercent(gen) < MUTATION_PROBABILITY) {
      std::uniform_int_distribution<size_t> idxDist(0, genes.size() - 1);
      int swaps = 1 + (distPercent(gen) % MAX_MUTATION_SWAPS);

      for (int s = 0; s < swaps; ++s) {
        size_t a = idxDist(gen);
        size_t b = idxDist(gen);
        std::swap(genes[a], genes[b]);
      }
    }

    return genes;
  };

  // --- Evolução ---
  int generationsWithoutImprovement = 0;
  int bestFitness = std::numeric_limits<int>::max();

  // inicializa bestFitness a partir do melhor atual
  bestFitness = population.begin()->second;

  while (generationsWithoutImprovement < MAX_GENERATIONS_WITHOUT_IMPROVEMENT) {
    int offspringCount =
        std::max<int>(1, (int)population.size() / CROSSOVER_FACTOR);

    for (int i = 0; i < offspringCount; ++i) {
      auto parents = selectParents();
      auto child = crossover(parents.first, parents.second);
      child = mutation(child);
      addIndividual(child);
    }

    int currentBest = population.begin()->second;
    if (currentBest < bestFitness) {
      bestFitness = currentBest;
      generationsWithoutImprovement = 0;
    } else {
      ++generationsWithoutImprovement;
    }
  }

  // --- Retorna solução LS do melhor indivíduo ---
  const std::vector<int> &bestGenes = population.begin()->first;
  std::vector<int> bestCopy = bestGenes;
  return LS<n>(bestCopy);
}
} // namespace partition