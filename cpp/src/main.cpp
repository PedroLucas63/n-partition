#include "Partition.hpp"
#include "ReadInstances.hpp"
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

/// @brief Overload the << operator for vectors of integers.
/// @param os Output stream.
/// @param v Vector of integers.
/// @return Output stream.
std::ostream &operator<<(std::ostream &os,
                         const std::vector<partition::ValueType> &v) {
  os << "[";
  for (auto &x : v) {
    os << x << " ";
  }
  os << "\b]";
  return os;
}

/**
 * @brief Writes the partitioned groups and their sums to a CSV file.
 *
 * Now supports a variable number of genetic runs.
 *
 * @tparam K Number of partitions (template)
 */
template <size_t K>
void writeInstanceCSV(
    std::ostream &os, size_t instanceID, int M, int N, int B,
    partition::ValueType optimalMakespan,
    const std::array<std::vector<partition::ValueType>, K> &ls,
    long long lsTime,
    const std::array<std::vector<partition::ValueType>, K> &lpt,
    long long lptTime,
    const std::array<std::vector<partition::ValueType>, K> &multifit,
    long long multifitTime,
    const std::array<std::vector<partition::ValueType>, K> &cga,
    long long cgaTime,
    const std::array<std::vector<partition::ValueType>, K> &sa, 
    long long saTime,
    const std::vector<std::array<std::vector<partition::ValueType>, K>>
        &geneticRuns,
    const std::vector<long long> &geneticTimes) {

  auto maxGroupSum =
      [](const std::array<std::vector<partition::ValueType>, K> &groups) {
        partition::ValueType maxSum = 0;
        for (auto &group : groups) {
          partition::ValueType sum = 0;
          for (partition::ValueType x : group)
            sum += x;
          if (sum > maxSum)
            maxSum = sum;
        }
        return maxSum;
      };

  os << instanceID << "," << M << "," << N << "," << B << "," << optimalMakespan
     << "," << maxGroupSum(ls) << "," << lsTime << "," << maxGroupSum(lpt)
     << "," << lptTime << "," << maxGroupSum(multifit) << "," << multifitTime
     << "," << maxGroupSum(cga) << "," << cgaTime
     << "," << maxGroupSum(sa) << "," << saTime;

  // append genetic runs results (count = geneticRuns.size())
  for (size_t i = 0; i < geneticRuns.size(); ++i) {
    os << "," << maxGroupSum(geneticRuns[i]) << "," << geneticTimes[i];
  }

  os << "\n";
}

/**
 * @brief Macro to generate switch cases for different template instantiations
 * of K.
 *
 * It will execute standard algorithms (LS, LPT, MULTIFIT, CGA, SA) once and the
 * genetic algorithm R times (R = geneticRunsCount local variable).
 *
 * The macro assumes it is expanded inside a scope where:
 *  - ARR is the input vector
 *  - INSTANCEID, MVAL, NVAL, BVAL, OPTIMAL, OS are visible
 *  - geneticRunsCount is an `int` with the desired number of genetic runs
 */
#define RUN_FOR_K_CSV(KVALUE, ARR, INSTANCEID, MVAL, NVAL, BVAL, OPTIMAL, OS)  \
  case KVALUE: {                                                               \
    auto start = std::chrono::steady_clock::now();                             \
    auto g = partition::LS<KVALUE>(ARR);                                       \
    auto end = std::chrono::steady_clock::now();                               \
    auto greedyTime =                                                          \
        std::chrono::duration_cast<std::chrono::microseconds>(end - start)     \
            .count();                                                          \
                                                                               \
    start = std::chrono::steady_clock::now();                                  \
    auto l = partition::LPT<KVALUE>(ARR);                                      \
    end = std::chrono::steady_clock::now();                                    \
    auto lptTime =                                                             \
        std::chrono::duration_cast<std::chrono::microseconds>(end - start)     \
            .count();                                                          \
                                                                               \
    start = std::chrono::steady_clock::now();                                  \
    auto m = partition::MULTIFIT<KVALUE>(ARR);                                 \
    end = std::chrono::steady_clock::now();                                    \
    auto multifitTime =                                                        \
        std::chrono::duration_cast<std::chrono::microseconds>(end - start)     \
            .count();                                                          \
                                                                               \
    start = std::chrono::steady_clock::now();                                  \
    auto c = partition::CGA<KVALUE>(ARR);                                      \
    end = std::chrono::steady_clock::now();                                    \
    auto cgaTime =                                                             \
        std::chrono::duration_cast<std::chrono::microseconds>(end - start)     \
            .count();                                                          \
                                                                               \
    start = std::chrono::steady_clock::now();                                  \
    auto sa = partition::SimulatedAnnealing<KVALUE>(ARR);                      \
    end = std::chrono::steady_clock::now();                                    \
    auto saTime =                                                              \
        std::chrono::duration_cast<std::chrono::microseconds>(end - start)     \
            .count();                                                          \
                                                                               \
                                                                               \
    /* Run genetic algorithm geneticRunsCount times and store results */       \
    std::vector<std::array<std::vector<partition::ValueType>, KVALUE>>         \
        geneticRuns;                                                           \
    std::vector<long long> geneticTimes;                                       \
    geneticRuns.reserve(geneticRunsCount);                                     \
    geneticTimes.reserve(geneticRunsCount);                                    \
    for (int gi = 0; gi < geneticRunsCount; ++gi) {                            \
      start = std::chrono::steady_clock::now();                                \
      auto gn = partition::geneticAlgorithm<KVALUE>(ARR);                      \
      end = std::chrono::steady_clock::now();                                  \
      auto gTime =                                                             \
          std::chrono::duration_cast<std::chrono::microseconds>(end - start)   \
              .count();                                                        \
      geneticRuns.push_back(std::move(gn));                                    \
      geneticTimes.push_back(gTime);                                           \
    }                                                                          \
                                                                               \
    writeInstanceCSV<KVALUE>(OS, INSTANCEID, MVAL, NVAL, BVAL, OPTIMAL, g,     \
                             greedyTime, l, lptTime, m, multifitTime, c,       \
                             cgaTime, sa, saTime, geneticRuns, geneticTimes);              \
    break;                                                                     \
  }

/**
 * @brief Class responsible for running partitioning experiments on multiple
 * instances. The number of genetic runs is configurable.
 */
class ExperimentRunner {
  std::ofstream outFile; // CSV output file stream
  std::string inputFilePath_;
  int geneticRunsCount_; // number of genetic algorithm runs per instance

public:
  ExperimentRunner(
      int geneticRunsCount = 5,
      const std::string &inputFilePath = "../instances/instances.txt",
      const std::string &outputFileName = "../results/balanced-results.csv")
      : outFile(outputFileName, std::ios::out), inputFilePath_(inputFilePath),
        geneticRunsCount_(geneticRunsCount) {
    if (!outFile.is_open()) {
      throw std::runtime_error("Failed to open output file.");
    }

    // write CSV header dynamically based on geneticRunsCount_
    outFile << "InstanceID,M,N,B,OptimalMakespan,"
            << "LS_MaxGroupSum,LS_Time(us),"
               "LPT_MaxGroupSum,LPT_Time(us),"
               "MULTIFIT_MaxGroupSum,MULTIFIT_Time(us),"
               "CGA_MaxGroupSum,CGA_Time(us),"
               "SA_MaxGroupSum,SA_Time(us)";

    for (int i = 1; i <= geneticRunsCount_; ++i) {
      outFile << ",Genetic_" << i << "_MaxGroupSum,Genetic_" << i
              << "_Time(us)";
    }
    outFile << "\n";
  }

  void run() {
    std::cout << "Reading instances...\n";
    auto instances = ReadInstances::readInstances(inputFilePath_);

    std::cout << "Running experiments...\n";
    for (size_t i = 0; i < instances.size(); ++i) {
      runInstance(instances[i], i + 1);
    }
  }

private:
  void runInstance(ReadInstances::InstanceData &instance, size_t id) {
    std::cout << "Running instance " << id << "\n";
    runAlgorithmsByK(instance.values, id, instance.M, instance.N, instance.B,
                     instance.optimalSum, outFile);
  }

  void runAlgorithmsByK(std::vector<partition::ValueType> &arr,
                        size_t instanceID, int Mval, int Nval, int Bval,
                        partition::ValueType optimalSum, std::ostream &os) {
    // make geneticRunsCount available for the macro
    int geneticRunsCount = geneticRunsCount_;

    switch (Nval) {
      RUN_FOR_K_CSV(2, arr, instanceID, Mval, Nval, Bval, optimalSum, os)
      RUN_FOR_K_CSV(3, arr, instanceID, Mval, Nval, Bval, optimalSum, os)
      RUN_FOR_K_CSV(4, arr, instanceID, Mval, Nval, Bval, optimalSum, os)
      RUN_FOR_K_CSV(5, arr, instanceID, Mval, Nval, Bval, optimalSum, os)
      RUN_FOR_K_CSV(8, arr, instanceID, Mval, Nval, Bval, optimalSum, os)
    default:
      os << "[WARN] Unsupported K = " << Nval << "\n";
    }
  }
};

int main(int argc, char **argv) {
  try {
    int geneticRuns = 5;
    std::string inPath = ReadInstances::INSTANCE_PATH;
    std::string outPath = "../results/balanced-results.csv";

    if (argc > 1) {
      int parsed = std::atoi(argv[1]);
      if (parsed > 0)
        geneticRuns = parsed;
      else
        std::cerr << "[WARN] invalid genetic runs arg, using default = 5\n";
    }
    if (argc > 2) {
      inPath = argv[2];
    }
    if (argc > 3) {
      outPath = argv[3];
    }

    std::cout << "Using genetic runs = " << geneticRuns << "\n";
    std::cout << "Output CSV = " << outPath << "\n";

    ExperimentRunner runner(geneticRuns, inPath, outPath);
    runner.run();
    std::cout << "Experiment completed. Results saved to '" << outPath
              << "'.\n";
  } catch (const std::exception &e) {
    std::cerr << "[ERROR] " << e.what() << "\n";
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
