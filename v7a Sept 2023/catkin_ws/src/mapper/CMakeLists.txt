cmake_minimum_required(VERSION 3.0.2)
project(mapper)

find_package(catkin REQUIRED COMPONENTS
  octomap_ros
  pcl_conversions
  pcl_ros
  roscpp
  sensor_msgs
)

catkin_package(
  # INCLUDE_DIRS include
  # LIBRARIES mapper
  CATKIN_DEPENDS octomap_ros pcl_conversions pcl_ros roscpp sensor_msgs
  # DEPENDS system_lib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(mapper_node src/mapper_node.cpp)
target_link_libraries(mapper_node ${catkin_LIBRARIES})

## Mark executables and/or libraries for installation
install(TARGETS mapper_node
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
