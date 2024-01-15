# Install script for directory: /home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_driver

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/velodyne_driver" TYPE FILE FILES "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/devel/include/velodyne_driver/VelodyneNodeConfig.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/velodyne_driver" TYPE FILE FILES "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/devel/lib/python3/dist-packages/velodyne_driver/__init__.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/devel/lib/python3/dist-packages/velodyne_driver/cfg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/velodyne_driver" TYPE DIRECTORY FILES "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/devel/lib/python3/dist-packages/velodyne_driver/cfg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/velodyne-master/velodyne_driver/catkin_generated/installspace/velodyne_driver.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/velodyne_driver/cmake" TYPE FILE FILES
    "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/velodyne-master/velodyne_driver/catkin_generated/installspace/velodyne_driverConfig.cmake"
    "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/velodyne-master/velodyne_driver/catkin_generated/installspace/velodyne_driverConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/velodyne_driver" TYPE FILE FILES "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_driver/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/velodyne_driver" TYPE DIRECTORY FILES "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_driver/include/velodyne_driver/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/velodyne_driver" TYPE FILE FILES "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_driver/nodelet_velodyne.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/velodyne_driver/launch" TYPE DIRECTORY FILES "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_driver/launch/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/velodyne_driver" TYPE PROGRAM FILES "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/src/velodyne-master/velodyne_driver/src/vdump")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/velodyne-master/velodyne_driver/src/lib/cmake_install.cmake")
  include("/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/velodyne-master/velodyne_driver/src/driver/cmake_install.cmake")

endif()

