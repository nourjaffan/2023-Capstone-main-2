execute_process(COMMAND "/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/DynamixelSDK-3.7.51/ros/dynamixel_sdk/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/nour1/Downloads/2023-Capstone-main/v7a Sept 2023/new_catkin_ws/build/DynamixelSDK-3.7.51/ros/dynamixel_sdk/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
