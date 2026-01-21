include(FetchContent)
FetchContent_Declare(
  ext_stdgpu
  SYSTEM
  PREFIX stdgpu
  GIT_REPOSITORY https://github.com/stotko/stdgpu.git
  GIT_TAG 1f0b2d51718692ec9046fe1b36173a591c611bdb
  UPDATE_COMMAND ""
)

# stdgpu build options
set(STDGPU_BUILD_SHARED_LIBS OFF)
set(STDGPU_BUILD_EXAMPLES OFF)
set(STDGPU_BUILD_TESTS OFF)
set(STDGPU_ENABLE_CONTRACT_CHECKS OFF)

# Download the files
FetchContent_MakeAvailable(ext_stdgpu)
