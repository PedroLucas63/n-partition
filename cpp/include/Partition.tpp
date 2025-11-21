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

template <std::size_t n>
std::array<std::vector<ValueType>, n> LS(std::vector<ValueType> &arr) {
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  std::array<std::vector<ValueType>, n> groups;

  using queue_element = std::pair<ValueType, std::size_t>; // {sum, index}
  auto cmp = [](const queue_element &a, const queue_element &b) {
    return a.first > b.first;
  };
  std::priority_queue<queue_element, std::vector<queue_element>, decltype(cmp)>
      pq(cmp);

  for (std::size_t i = 0; i < n; i++) {
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

template <std::size_t n>
std::array<std::vector<ValueType>, n> LPT(std::vector<ValueType> &arr) {
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  std::sort(arr.begin(), arr.end(), std::greater<ValueType>());
  return LS<n>(arr);
}

template <std::size_t n>
std::array<std::vector<ValueType>, n> MULTIFIT(std::vector<ValueType> &arr,
                                               std::size_t k) {
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  std::sort(arr.begin(), arr.end(), std::greater<ValueType>());

  ValueType sum = std::accumulate(arr.begin(), arr.end(), ValueType{0});
  ValueType max = arr.front();

  ValueType lowerBound = std::max<ValueType>(max, sum / n);
  ValueType upperBound = std::max<ValueType>(max, 2 * sum / n);

  auto bestGroups = FFD(arr, upperBound);

  for (std::size_t i = 0; i < k && lowerBound < upperBound; i++) {
    ValueType capacity = (lowerBound + upperBound) / 2;
    auto groups = FFD(arr, capacity);

    if (groups.size() > n) {
      lowerBound = capacity;
    } else {
      bestGroups = groups;
      upperBound = capacity;
    }
  }

  std::array<std::vector<ValueType>, n> finalGroups;
  for (std::size_t i = 0; size_t(i) < bestGroups.size(); i++) {
    finalGroups[i] = bestGroups[i];
  }
  return finalGroups;
}

template <std::size_t n>
std::array<std::vector<ValueType>, n> CGA(std::vector<ValueType> &arr) {
  // Check if n is valid
  if (n <= 0) {
    throw std::invalid_argument("n must be a positive integer");
  } else if (n == 1) {
    return {{arr}};
  }

  // Get one solution
  auto groupsCandidate = LPT<n>(arr);

  // Get makespan
  std::array<ValueType, n> sums;
  std::transform(groupsCandidate.begin(), groupsCandidate.end(), sums.begin(),
                 [](const std::vector<ValueType> &group) {
                   return std::accumulate(group.begin(), group.end(),
                                          ValueType{0});
                 });
  ValueType makespan = *std::max_element(sums.begin(), sums.end());

  // Get makespan lowerbound
  ValueType total = std::accumulate(arr.begin(), arr.end(), ValueType{0});
  ValueType lowerbound = (total + n - 1) / n;

  // Get best solution
  if (lowerbound < makespan) {
    std::array<ValueType, n> groupSums = {};
    std::array<std::vector<ValueType>, n> actualGroups = {};
    CGABacktracking<n>(arr, actualGroups, groupSums, makespan, lowerbound,
                       groupsCandidate, 0);
  }

  return groupsCandidate;
}

template <std::size_t n>
void CGABacktracking(const std::vector<ValueType> &arr,
                     std::array<std::vector<ValueType>, n> &actualGroups,
                     std::array<ValueType, n> &groupSums, ValueType &makespan,
                     ValueType &lowerbound,
                     std::array<std::vector<ValueType>, n> &groupsCandidate,
                     std::size_t i) {
  // Base case
  if (size_t(i) == arr.size()) {
    ValueType currentMax =
        *std::max_element(groupSums.begin(), groupSums.end());

    // Update
    if (currentMax < makespan) {
      makespan = currentMax;
      groupsCandidate = actualGroups;
    }
    return;
  }

  // Sort groups (greedy)
  std::array<ValueType, n> groupsIndices;
  std::iota(groupsIndices.begin(), groupsIndices.end(), 0);
  std::sort(groupsIndices.begin(), groupsIndices.end(),
            [&groupSums](std::size_t i, std::size_t j) {
              return groupSums[i] < groupSums[j];
            });

  // Backtracking
  std::unordered_set<ValueType> triedSums;
  for (std::size_t j : groupsIndices) {
    // Not already tried
    if (triedSums.count(groupSums[j])) {
      continue;
    }
    triedSums.insert(groupSums[j]);

    // Evaluation
    groupSums[j] += arr[i];
    ValueType currentMax =
        *std::max_element(groupSums.begin(), groupSums.end());

    // Uperbound prune
    if (currentMax < makespan) {
      // Recursion
      actualGroups[j].push_back(arr[i]);
      CGABacktracking<n>(arr, actualGroups, groupSums, makespan, lowerbound,
                         groupsCandidate, i + 1);
      actualGroups[j].pop_back(); // Backtrack
    }

    groupSums[j] -= arr[i];

    // Lowerbound prune
    if (makespan == lowerbound) {
      return;
    }
  }
}

template <std::size_t n>
std::array<std::vector<ValueType>, n>
geneticAlgorithm(std::vector<ValueType> &arr) {
  // --- Constantes ---
  const int QUEUE_MAX_SIZE = 50;
  const int INITIAL_POPULATION_SIZE = 20;
  const int CROSSOVER_FACTOR = 2;
  const int MUTATION_PROBABILITY = 40; // percentage
  const int MAX_GENERATIONS_WITHOUT_IMPROVEMENT = 5;

  // -- Calcula o makespan ótimo --
  ValueType sum = std::accumulate(arr.begin(), arr.end(), 0);
  const ValueType makespan_opt = (sum + n - 1) / n;

  using Individual =
      std::pair<std::vector<ValueType>, ValueType>; // (genes, fitness)

  // Menor fitness = melhor indivíduo
  auto cmp = [](const Individual &a, const Individual &b) {
    return a.second < b.second;
  };

  std::multiset<Individual, decltype(cmp)> population(cmp);

  // RNG único e distributions
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<double> dist01(0.0, 1.0);
  std::uniform_int_distribution<int> distPercent(0, 99);

  // --- Função auxiliar: makespan (usa o genes passado) ---
  auto calculateMakespan = [&](const std::vector<ValueType> &genes) {
    std::vector<ValueType> tmp = genes;
    auto solution = LS<n>(tmp);

    std::array<ValueType, n> sums;
    for (std::size_t i = 0; i < n; ++i)
      sums[i] =
          std::accumulate(solution[i].begin(), solution[i].end(), ValueType{0});

    return *std::max_element(sums.begin(), sums.end());
  };

  // --- Adicionar indivíduo (com poda para QUEUE_MAX_SIZE) ---
  auto addIndividual = [&](const std::vector<ValueType> &genes) {
    ValueType fitness = calculateMakespan(genes);
    population.insert({genes, fitness});

    if ((int)population.size() > QUEUE_MAX_SIZE) {
      auto it = std::prev(population.end());
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
  std::vector<ValueType> work = arr;
  for (int i = 0; i < INITIAL_POPULATION_SIZE; ++i) {
    addIndividual(work);
    std::shuffle(work.begin(), work.end(), gen);
  }

  // garante que population não está vazia
  if (population.empty()) {
    std::vector<ValueType> tmp = arr;
    return LS<n>(tmp);
  }

  // multiset com todos os elementos possíveis (para crossover)
  std::multiset<ValueType, std::greater<ValueType>> elements(arr.begin(),
                                                             arr.end());

  // --- Crossover (uniform-like, preserva multiconjunto) ---
  auto crossover = [&](const Individual &p1, const Individual &p2) {
    size_t L = p1.first.size();
    std::vector<ValueType> child(L, -1);

    std::multiset<ValueType, std::greater<ValueType>> available(elements);

    const size_t K = 2;

    for (size_t start = 0; start < L; start += K) {
      // define o bloco
      size_t end = std::min(start + K, L);

      // calcular diferenças dos blocos
      ValueType min1 = std::numeric_limits<ValueType>::max();
      ValueType max1 = std::numeric_limits<ValueType>::min();
      ValueType min2 = std::numeric_limits<ValueType>::max();
      ValueType max2 = std::numeric_limits<ValueType>::min();

      for (size_t i = start; i < end; ++i) {
        min1 = std::min(min1, p1.first[i]);
        max1 = std::max(max1, p1.first[i]);
        min2 = std::min(min2, p2.first[i]);
        max2 = std::max(max2, p2.first[i]);
      }
      ValueType diff1 = max1 - min1;
      ValueType diff2 = max2 - min2;

      // escolher bloco com menor diferença
      const auto &chosen = (diff1 <= diff2 ? p1.first : p2.first);

      // inserir deste bloco apenas valores disponíveis
      for (size_t i = start; i < end; ++i) {
        ValueType v = chosen[i];
        auto it = available.find(v);
        if (it != available.end()) {
          child[i] = v;
          available.erase(it);
        }
      }
    }

    // preencher os buracos com restantes
    for (auto e : available) {
      auto pos = std::find(child.begin(), child.end(), -1);
      if (pos != child.end())
        *pos = e;
    }

    return child;
  };

  // --- Mutação ---
  auto mutation = [&](std::vector<ValueType> genes) {
    std::uniform_int_distribution<size_t> idxDist(0, genes.size() - 1);

    size_t a = idxDist(gen);
    size_t b = idxDist(gen);
    if (a > b)
      std::swap(a, b);
    std::reverse(genes.begin() + a, genes.begin() + b);

    return genes;
  };

  // --- Evolução ---
  int generationsWithoutImprovement = 0;
  ValueType bestFitness = std::numeric_limits<int>::max();

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

    ValueType currentBest = population.begin()->second;
    if (currentBest < bestFitness) {
      bestFitness = currentBest;
      generationsWithoutImprovement = 0;
    } else {
      ++generationsWithoutImprovement;
    }

    if (bestFitness == makespan_opt) {
      break;
    }
  }

  // --- Retorna solução LS do melhor indivíduo ---
  const std::vector<ValueType> &bestGenes = population.begin()->first;
  std::vector<ValueType> bestCopy = bestGenes;
  return LS<n>(bestCopy);
}
} // namespace partition