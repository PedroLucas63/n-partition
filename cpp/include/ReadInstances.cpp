#include "ReadInstances.hpp"
#include <fstream>
#include <sstream>
#include <iostream>

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
    bool readingNumbers = false;

    while (std::getline(file, line)) {
        if (line.empty()) {
            // End of current instance
            if (!current.values.empty()) {
                instances.push_back(current);
                current.values.clear();
            }
            readingNumbers = false;
            continue;
        }

        // Ignore comments
        if (line[0] == '#') continue;

        std::stringstream ss(line);
        if (!readingNumbers) {
            // Header line: N K B OPTIMAL_SUM
            if (!(ss >> current.N >> current.K >> current.B >> current.OPTIMAL_SUM))
                continue;
            readingNumbers = true;
        } else {
            // Line containing the list of numbers
            int num;
            while (ss >> num)
                current.values.push_back(num);
        }
    }

    // Handle last instance (if file doesn't end with a blank line)
    if (!current.values.empty()) {
        instances.push_back(current);
    }

    file.close();
    return instances;
}

} // namespace ReadInstances
