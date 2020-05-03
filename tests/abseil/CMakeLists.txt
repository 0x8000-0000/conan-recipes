cmake_minimum_required(VERSION 3.15.1)
project(test_abseil
   VERSION 0.1
   DESCRIPTION "Test Abseil Packaging"
   LANGUAGES CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS NO_OUTPUT_DIRS)

add_executable(test1 test1.cpp)
target_compile_features(test1 PUBLIC cxx_std_17)
set_target_properties(test1 PROPERTIES CXX_EXTENSIONS OFF)
target_link_libraries(test1 PUBLIC CONAN_PKG::absl)
