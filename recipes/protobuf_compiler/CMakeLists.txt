cmake_minimum_required(VERSION 3.13)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

if(WIN32 AND BUILD_SHARED_LIBS)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

add_subdirectory("source_subfolder/cmake")
