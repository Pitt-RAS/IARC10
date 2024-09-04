cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(MyOpenCVProject VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find OpenCV package
find_package(OpenCV REQUIRED)

# Specify the include directories
include_directories(${OpenCV_INCLUDE_DIRS})

# Add the executable
add_executable(MyOpenCVProject main.cpp)

# Link the executable to the OpenCV libraries
target_link_libraries(MyOpenCVProject ${OpenCV_LIBS})
