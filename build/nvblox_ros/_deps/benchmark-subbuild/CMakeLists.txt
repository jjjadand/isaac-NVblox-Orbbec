# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.22.1)

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(benchmark-populate NONE)



include(ExternalProject)
ExternalProject_Add(benchmark-populate
                     "UPDATE_DISCONNECTED" "False" "PREFIX" "benchmark" "URL" "https://github.com/google/benchmark/archive/refs/tags/v1.8.2.tar.gz" "URL_HASH" "SHA256=2aab2980d0376137f969d92848fbb68216abb07633034534fc8c65cc4e7a0e93" "DOWNLOAD_DIR" "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-src/external/benchmark"
                    SOURCE_DIR          "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/benchmark-src"
                    BINARY_DIR          "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/benchmark-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
)


