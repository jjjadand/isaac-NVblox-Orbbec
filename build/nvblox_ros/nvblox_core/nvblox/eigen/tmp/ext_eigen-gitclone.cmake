
if(NOT "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen-stamp/ext_eigen-gitinfo.txt" IS_NEWER_THAN "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen-stamp/ext_eigen-gitclone-lastrun.txt")
  message(STATUS "Avoiding repeated git clone, stamp file is up to date: '/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen-stamp/ext_eigen-gitclone-lastrun.txt'")
  return()
endif()

execute_process(
  COMMAND ${CMAKE_COMMAND} -E rm -rf "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to remove directory: '/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen'")
endif()

# try the clone 3 times in case there is an odd git clone issue
set(error_code 1)
set(number_of_tries 0)
while(error_code AND number_of_tries LESS 3)
  execute_process(
    COMMAND "/usr/bin/git"  clone --no-checkout --config "advice.detachedHead=false" "https://gitlab.com/libeigen/eigen.git" "ext_eigen"
    WORKING_DIRECTORY "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src"
    RESULT_VARIABLE error_code
    )
  math(EXPR number_of_tries "${number_of_tries} + 1")
endwhile()
if(number_of_tries GREATER 1)
  message(STATUS "Had to git clone more than once:
          ${number_of_tries} times.")
endif()
if(error_code)
  message(FATAL_ERROR "Failed to clone repository: 'https://gitlab.com/libeigen/eigen.git'")
endif()

execute_process(
  COMMAND "/usr/bin/git"  checkout 3.4.0 --
  WORKING_DIRECTORY "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to checkout tag: '3.4.0'")
endif()

set(init_submodules TRUE)
if(init_submodules)
  execute_process(
    COMMAND "/usr/bin/git"  submodule update --recursive --init 
    WORKING_DIRECTORY "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen"
    RESULT_VARIABLE error_code
    )
endif()
if(error_code)
  message(FATAL_ERROR "Failed to update submodules in: '/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen'")
endif()

# Complete success, update the script-last-run stamp file:
#
execute_process(
  COMMAND ${CMAKE_COMMAND} -E copy
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen-stamp/ext_eigen-gitinfo.txt"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen-stamp/ext_eigen-gitclone-lastrun.txt"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to copy script-last-run stamp file: '/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen-stamp/ext_eigen-gitclone-lastrun.txt'")
endif()

