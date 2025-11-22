#include "Partition.hpp"
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

using namespace std;
using namespace partition;

using TaskType = ValueType;

// Gera tarefas aleatórias
vector<TaskType> generate_tasks(size_t num_tasks, int min_time = 10,
                                int max_time = 7200) {
  random_device rd;
  mt19937 gen(rd());
  uniform_int_distribution<> dis(min_time, max_time);

  vector<TaskType> tasks(num_tasks);
  for (auto &t : tasks)
    t = static_cast<TaskType>(dis(gen));
  return tasks;
}

// Calcula makespan
template <size_t n>
TaskType makespan(const array<vector<TaskType>, n> &allocation) {
  TaskType max_time = 0;
  for (const auto &machine_tasks : allocation) {
    TaskType sum_time = accumulate(machine_tasks.begin(), machine_tasks.end(),
                                   static_cast<TaskType>(0));
    if (sum_time > max_time)
      max_time = sum_time;
  }
  return max_time;
}

// Calcula média da distância para makespan ideal
template <size_t n>
double mean_distance_to_ideal(const array<vector<TaskType>, n> &allocation) {
  TaskType total = 0;
  for (const auto &machine_tasks : allocation)
    total += accumulate(machine_tasks.begin(), machine_tasks.end(),
                        static_cast<TaskType>(0));

  double ideal = static_cast<double>(total) / n;
  double sum_dist = 0.0;
  for (const auto &machine_tasks : allocation) {
    double machine_sum =
        accumulate(machine_tasks.begin(), machine_tasks.end(), 0.0);
    sum_dist += abs(machine_sum - ideal);
  }
  return sum_dist / n;
}

// Função template para rodar simulação com número fixo de máquinas
template <size_t num_machines>
void run_simulation(ofstream &csv, size_t num_tasks, int winner_makespan[4]) {
  using array_type = array<vector<TaskType>, num_machines>;
  vector<TaskType> tasks = generate_tasks(num_tasks);

  array<TaskType, 4> makespans{};
  array<double, 4> distances{};
  array<double, 4> times_mean{};
  array<double, 4> times_min{};
  array<double, 4> times_max{};

  vector<string> algo_names = {"LS", "LPT", "MULTIFIT", "Genetic", "AnnealingLaha"};

  for (int algo_idx = 0; algo_idx < 4; ++algo_idx) {
    const int runs = 5;
    vector<double> run_times;
    array_type allocation;

    for (int run = 0; run < runs; ++run) {
      auto tasks_copy = tasks;
      auto start = chrono::steady_clock::now();

      switch (algo_idx) {
      case 0:
        allocation = LS<num_machines>(tasks_copy);
        break;
      case 1:
        allocation = LPT<num_machines>(tasks_copy);
        break;
      case 2:
        allocation = MULTIFIT<num_machines>(tasks_copy);
        break;
      case 3:
        allocation = geneticAlgorithm<num_machines>(tasks_copy);
        break;
      case 4:
        allocation = SimulatedAnnealing<num_machines>(tasks_copy);
        break;
      }

      auto end = chrono::steady_clock::now();
      run_times.push_back(chrono::duration<double>(end - start).count());
    }

    times_mean[algo_idx] =
        accumulate(run_times.begin(), run_times.end(), 0.0) / runs;
    times_min[algo_idx] = *min_element(run_times.begin(), run_times.end());
    times_max[algo_idx] = *max_element(run_times.begin(), run_times.end());

    makespans[algo_idx] = makespan<num_machines>(allocation);
    distances[algo_idx] = mean_distance_to_ideal<num_machines>(allocation);
  }

  int min_makespan_idx = distance(
      makespans.begin(), min_element(makespans.begin(), makespans.end()));
  winner_makespan[min_makespan_idx]++;

  for (int i = 0; i < 4; ++i) {
    csv << num_machines << "," << num_tasks << "," << algo_names[i] << ","
        << times_mean[i] << "," << times_min[i] << "," << times_max[i] << ","
        << makespans[i] << "," << distances[i] << "\n";
  }
}

int main() {
  ofstream csv("results.csv");
  csv << "NumMachines,NumTasks,Algorithm,TimeMean,TimeMin,TimeMax,Makespan,"
         "MeanDistanceToIdeal\n";

  int winner_makespan[4] = {0, 0, 0, 0};

  for (size_t num_tasks = 500; num_tasks <= 1000; num_tasks += 100) {
    run_simulation<30>(csv, num_tasks, winner_makespan);
    run_simulation<40>(csv, num_tasks, winner_makespan);
    run_simulation<50>(csv, num_tasks, winner_makespan);
  }

  csv.close();

  cout << "Simulação concluída. Resultados salvos em results.csv\n";
  cout << "Vitórias por algoritmo (menor makespan):\n";
  vector<string> algo_names = {"LS", "LPT", "MULTIFIT", "Genetic"};
  for (int i = 0; i < 4; ++i)
    cout << algo_names[i] << ": " << winner_makespan[i] << "\n";

  return 0;
}
