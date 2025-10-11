cmake_minimum_required(VERSION 3.15)
project(n-partition VERSION 0.1.0 LANGUAGES CXX)

# Define o padrão do C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Inclui diretórios de cabeçalhos
include_directories(${PROJECT_SOURCE_DIR}/include)

# Adiciona o executável
add_executable(n-partition
   include/ReadInstances.cpp
   include/ExperimentRunner.cpp
   src/main.cpp
)