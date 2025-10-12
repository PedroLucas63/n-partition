#include <iostream>
#include "partition.hpp" 
#include "ReadInstances.hpp"
#include <fstream>
#include <chrono>


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
 * @brief Writes the partitioned groups and their sums to a CSV file.
 * 
 * @param os The output stream to write to.
 * @param instanceID The ID of the instance.
 * @param N The number of elements in the instance.
 * @param Kval The number of partitions in the instance.
 * @param B The bit size used in the instance.
 * @param ls The groups formed by the LS algorithm.
 * @param lsTime The time taken by the LS algorithm in microseconds.
 * @param lpt The groups formed by the LPT algorithm.
 * @param lptTime The time taken by the LPT algorithm in microseconds.
 * @param multifit The groups formed by the MULTIFIT algorithm.
 * @param multifitTime The time taken by the MULTIFIT algorithm in microseconds.
 * @param optimalMakespan The optimal makespan for the instance.
 */
template <size_t K>
void writeInstanceCSV(std::ostream &os, size_t instanceID, int N, int Kval, int B, int optimalMakespan,
                    const std::array<std::vector<int>, K> &ls, long long lsTime,
                    const std::array<std::vector<int>, K> &lpt, long long lptTime,
                    const std::array<std::vector<int>, K> &multifit, long long multifitTime) {

  auto maxGroupSum = [](const std::array<std::vector<int>, K> &groups) {
    int maxSum = 0;
    for (auto &group : groups) {
      int sum = 0;
      for (int x : group) sum += x;
      if (sum > maxSum) maxSum = sum;
    }
    return maxSum;
  };

  os << instanceID << "," << N << "," << Kval << "," << B << "," << optimalMakespan
    << "," << maxGroupSum(ls) << "," << lsTime
    << "," << maxGroupSum(lpt) << "," << lptTime
    << "," << maxGroupSum(multifit) << "," << multifitTime << "\n";
}

/**
 * @brief Macro to generate switch cases for different template instantiations of K.
 * 
 * @param KVALUE The template value K.
 * @param ARR The array/vector to be partitioned.
 * @param INSTANCEID The instance ID for printing.
 * @param NVAL The N value of the instance.
 * @param KVAL The K value of the instance.
 * @param BVAL The B value of the instance.
 * @param OPTIMAL The optimal makespan of the instance.
 * @param OS The output stream to print results to.
 * 
 */

#define RUN_FOR_K_CSV(KVALUE, ARR, INSTANCEID, NVAL, KVAL, BVAL, OPTIMAL, OS) \
  case KVALUE: { \
    auto start = std::chrono::high_resolution_clock::now(); \
    auto g = partition::LS<KVALUE>(ARR); \
    auto end = std::chrono::high_resolution_clock::now(); \
    auto greedyTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count(); \
    \
    start = std::chrono::high_resolution_clock::now(); \
    auto l = partition::LPT<KVALUE>(ARR); \
    end = std::chrono::high_resolution_clock::now(); \
    auto lptTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count(); \
    \
    start = std::chrono::high_resolution_clock::now(); \
    auto m = partition::MULTIFIT<KVALUE>(ARR); \
    end = std::chrono::high_resolution_clock::now(); \
    auto multifitTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count(); \
    \
    writeInstanceCSV(OS, INSTANCEID, NVAL, KVAL, BVAL, OPTIMAL, g, greedyTime, l, lptTime, m, multifitTime); \
    break; \
  }




/**
 * @brief Class responsible for running partitioning experiments on multiple instances.
 * 
 * Reads instances from a file, executes the partitioning algorithms for each instance,
 * and prints the results to the console.
 * 
 * @patam outputFileName The name of the CSV file to write results to.
 */
class ExperimentRunner {
  std::ofstream outFile;  // CSV output file stream

public:
  ExperimentRunner(const std::string &outputFileName = "../../results.csv")
      : outFile(outputFileName, std::ios::out)
  {
    if (!outFile.is_open()) {
        throw std::runtime_error("Failed to open output file.");
    }

    // write CSV header
    outFile << "InstanceID,N,K,B,OptimalMakespan,LS_MaxGroupSum,LS_Time(us),LPT_MaxGroupSum,LPT_Time(us),MULTIFIT_MaxGroupSum,MULTIFIT_Time(us)\n";
  }

  void run() {
    auto instances = ReadInstances::readInstances();
    // ReadInstances::printInstances(instances);

    for (size_t i = 0; i < instances.size(); ++i) {
      runInstance(instances[i], i + 1);
    }
  }

private:
  void runInstance(ReadInstances::InstanceData &instance, size_t id) {

    runAlgorithmsByK(instance.K, instance.values, id, instance.N, instance.K, instance.B, instance.optimalSum, outFile);
  }

  void runAlgorithmsByK(int K, std::vector<int> &arr, size_t instanceID, int Nval, int Kval, int Bval, int optimalSum, std::ostream &os) {
    switch (K) {
      RUN_FOR_K_CSV(2, arr, instanceID, Nval, Kval, Bval, optimalSum, os)
      RUN_FOR_K_CSV(3, arr, instanceID, Nval, Kval, Bval, optimalSum, os)
      RUN_FOR_K_CSV(4, arr, instanceID, Nval, Kval, Bval, optimalSum, os)
      RUN_FOR_K_CSV(8, arr, instanceID, Nval, Kval, Bval, optimalSum, os)
      RUN_FOR_K_CSV(16, arr, instanceID, Nval, Kval, Bval, optimalSum, os)
      RUN_FOR_K_CSV(24, arr, instanceID, Nval, Kval, Bval, optimalSum, os)
    default:
      os << "[WARN] Unsupported K = " << K << "\n";
    }
  }
};


int main(int, char **) {
  try {
    ExperimentRunner runner("../results/results.csv");
    runner.run();
    std::cout << "Experiment completed. Results saved to 'results.csv'.\n";
  } catch (const std::exception &e) {
    std::cerr << "[ERROR] " << e.what() << "\n";
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}