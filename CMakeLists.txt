cmake_minimum_required(VERSION 3.20.0)

project(DuiLib VERSION 1.0.0 LANGUAGES CXX)

# set(CMAKE_GENERATOR_TOOLSET "v100" CACHE STRING "VS2010 Toolset" FORCE)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


add_definitions(-DCMAKE)
add_definitions(-DUNICODE -D_UNICODE)

add_compile_options(/W3 /WX-) 
add_definitions(/D_UNICODE /DUNICODE)

set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_VERSION 5.01)

file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 资源数据目录：优先使用 data，若不存在则使用 bin（向后兼容）
if(EXISTS ${CMAKE_SOURCE_DIR}/data)
  set(DUILIB_DATA_DIR ${CMAKE_SOURCE_DIR}/data CACHE PATH "DuiLib resource data directory (skin, plugins, etc.)")
elseif(EXISTS ${CMAKE_SOURCE_DIR}/bin)
  set(DUILIB_DATA_DIR ${CMAKE_SOURCE_DIR}/bin CACHE PATH "DuiLib resource data directory (skin, plugins, etc.)")
  message(STATUS "Using bin as data dir - rename to 'data' for the new layout")
else()
  message(WARNING "Neither data nor bin directory found - demos may fail to find skin resources")
endif()

# 选项：是否构建 Demos
# 独立作为 project 运行时默认 ON，作为子项目被 add_subdirectory 引入时默认 OFF
if(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
  set(_default_build_demos ON)   # 顶层项目，默认构建 demo
else()
  set(_default_build_demos OFF)  # 子项目，默认不构建 demo
endif()
option(BUILD_DEMOS "Build DuiLib demos" ${_default_build_demos})
# 选项：DuiLib 构建为动态库还是静态库（默认 OFF = 静态库）
option(BUILD_SHARED_DUILIB "Build DuiLib as shared library (DLL)" OFF)

# sub projects
add_subdirectory(DuiLib)
if(BUILD_DEMOS)
  add_subdirectory(Demos)
endif()

# build with powershell
# mkdir build ; cd build
# cmake -G "Visual Studio 10 2010" -A Win32 ..
# cmake --build ../build