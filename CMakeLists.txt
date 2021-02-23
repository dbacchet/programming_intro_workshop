cmake_minimum_required(VERSION 3.10)

project(CppTutorial VERSION 0.0.1
                  DESCRIPTION "programming tutorial"
                  LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# generate the compilation database file
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_C_FLAGS "-Werror")
set(CMAKE_CXX_FLAGS "-Werror")

enable_testing()
# recurse subdirectories
add_subdirectory(cpp_step0)

