project(hungarianAlgorithm)
cmake_minimum_required(VERSION 3.12)

set(CMAKE_BUILD_TYPE Debug)


# find dependent packages
find_package (Eigen3 3.3 REQUIRED)

# create Executable
set(SOURCES
	src/main.cpp
	src/hungarian_algorithm.cpp
   )

add_executable(hungarian_algorithm ${SOURCES})
target_include_directories(hungarian_algorithm PUBLIC include ${EIGEN_INCLUDE_DIR})
target_link_libraries(hungarian_algorithm Eigen3::Eigen)
