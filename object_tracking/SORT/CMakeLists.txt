project(sort)
cmake_minimum_required(VERSION 3.12)

set(CMAKE_BUILD_TYPE Debug)


# find dependent packages
find_package (Eigen3 3.3 REQUIRED)

# create Executable
set(SOURCES
	src/utils.cpp
	src/hungarian.cpp
	src/main.cpp
   )

add_executable(sortDemo ${SOURCES})
target_include_directories(sortDemo PUBLIC include ${EIGEN_INCLUDE_DIR})
target_link_libraries(sortDemo Eigen3::Eigen)
