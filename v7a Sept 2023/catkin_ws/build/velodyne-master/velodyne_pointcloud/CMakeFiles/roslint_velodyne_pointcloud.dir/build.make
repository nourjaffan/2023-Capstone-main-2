# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build"

# Utility rule file for roslint_velodyne_pointcloud.

# Include the progress variables for this target.
include velodyne-master/velodyne_pointcloud/CMakeFiles/roslint_velodyne_pointcloud.dir/progress.make

roslint_velodyne_pointcloud: velodyne-master/velodyne_pointcloud/CMakeFiles/roslint_velodyne_pointcloud.dir/build.make
	cd "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_pointcloud" && "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/catkin_generated/env_cached.sh" /usr/bin/python3 -m roslint.cpplint_wrapper "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_pointcloud/include/velodyne_pointcloud/calibration.h" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_pointcloud/include/velodyne_pointcloud/datacontainerbase.h" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_pointcloud/include/velodyne_pointcloud/organized_cloudXYZIRT.h" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_pointcloud/include/velodyne_pointcloud/pointcloudXYZIRT.h" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_pointcloud/include/velodyne_pointcloud/rawdata.h" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_pointcloud/include/velodyne_pointcloud/transform.h" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_pointcloud/tests/test_calibration.cpp"
.PHONY : roslint_velodyne_pointcloud

# Rule to build all files generated by this target.
velodyne-master/velodyne_pointcloud/CMakeFiles/roslint_velodyne_pointcloud.dir/build: roslint_velodyne_pointcloud

.PHONY : velodyne-master/velodyne_pointcloud/CMakeFiles/roslint_velodyne_pointcloud.dir/build

velodyne-master/velodyne_pointcloud/CMakeFiles/roslint_velodyne_pointcloud.dir/clean:
	cd "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/velodyne-master/velodyne_pointcloud" && $(CMAKE_COMMAND) -P CMakeFiles/roslint_velodyne_pointcloud.dir/cmake_clean.cmake
.PHONY : velodyne-master/velodyne_pointcloud/CMakeFiles/roslint_velodyne_pointcloud.dir/clean

velodyne-master/velodyne_pointcloud/CMakeFiles/roslint_velodyne_pointcloud.dir/depend:
	cd "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_pointcloud" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/velodyne-master/velodyne_pointcloud" "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/velodyne-master/velodyne_pointcloud/CMakeFiles/roslint_velodyne_pointcloud.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : velodyne-master/velodyne_pointcloud/CMakeFiles/roslint_velodyne_pointcloud.dir/depend

