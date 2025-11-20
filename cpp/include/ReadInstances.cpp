#include "ReadInstances.hpp"
#include <fstream>
#include <iostream>
#include <sstream>

namespace ReadInstances {

std::vector<InstanceData> readInstances(const std::string &filePath) {
  std::ifstream file(filePath);
  std::vector<InstanceData> instances;

  if (!file.is_open()) {
    std::cerr << "[ERROR] Could not open file: " << filePath << std::endl;
    return instances;
  }

  std::string line;
  InstanceData current;
  bool readingValues = false;
  int valuesCount = 0;

  while (std::getline(file, line)) {
    // Skip empty lines
    if (line.empty())
      continue;

    // Check if it's an instance header
    if (line.find("# Instance") != std::string::npos) {
      // If we were reading an instance, save it before starting a new one
      if (readingValues && valuesCount == current.M) {
        instances.push_back(current);
      }

      // Reset for new instance
      current = InstanceData();
      readingValues = false;
      valuesCount = 0;
      continue;
    }

    // Read the parameters line (N K B optimalSum)
    if (!readingValues && line.find("#") == std::string::npos) {
      std::istringstream iss(line);
      if (iss >> current.M >> current.N >> current.B >> current.optimalSum) {
        if (current.M <= 0) {
          std::cerr << "[ERRO] Valor de M inválido: " << current.M << "\n";
          continue;
        }
        current.values.clear();
        readingValues = true;
      } else {
        std::cerr << "[ERRO] Linha mal formatada: " << line << "\n";
      }
      continue;
    }

    // Read the values line
    if (readingValues) {
      std::istringstream iss(line);
      partition::ValueType value;
      while (iss >> value) {
        current.values.push_back(value);
        valuesCount++;
      }

      // Check if we read all expected values
      if (valuesCount == current.N) {
        instances.push_back(current);
        readingValues = false;
      }
    }
  }

  // Don't forget to add the last instance if file ends without another header
  if (readingValues && valuesCount == current.M) {
    instances.push_back(current);
  } else if (readingValues) {
    std::cerr << "[ERRO] Instância incompleta ignorada.\n";
  }

  file.close();
  return instances;
}

// Função auxiliar para testar a leitura
void printInstances(const std::vector<InstanceData> &instances) {
  for (size_t i = 0; i < instances.size(); i++) {
    const auto &instance = instances[i];
    std::cout << "Instance " << (i + 1) << ":\n";
    std::cout << "  N: " << instance.M << ", M: " << instance.M
              << ", B: " << instance.B
              << ", optimalSum: " << instance.optimalSum << "\n";
    std::cout << "  Values: ";
    for (partition::ValueType value : instance.values) {
      std::cout << value << " ";
    }
    std::cout << "\n\n";
  }
}

} // namespace ReadInstances
