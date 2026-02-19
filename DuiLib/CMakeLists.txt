# cmake file for DuiLib

set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/lib)
set(RUNTIME_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR} RootSrc)
aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR}/Control ControlSrc)
aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR}/Core CoreSrc)
aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR}/Layout LayoutSrc)
aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR}/Utils UtilsSrc)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/Control)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/Core)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/Layout)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/Utils)

if(BUILD_SHARED_DUILIB)
  add_library(DuiLib SHARED ${ControlSrc} ${CoreSrc} ${LayoutSrc} ${UtilsSrc} ${RootSrc})
  target_compile_definitions(DuiLib PRIVATE DUILIB_EXPORTS)
  add_custom_command(TARGET DuiLib POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    $<TARGET_FILE:DuiLib> ${CMAKE_BINARY_DIR}/bin)
else()
  add_library(DuiLib STATIC ${ControlSrc} ${CoreSrc} ${LayoutSrc} ${UtilsSrc} ${RootSrc})
  target_compile_definitions(DuiLib PUBLIC UILIB_STATIC)
endif()

target_link_libraries(DuiLib comctl32)
set_target_properties(DuiLib PROPERTIES
    DEBUG_POSTFIX ""
    OUTPUT_NAME "DuiLib"
)
# 使用父目录作为 include 路径，使消费者可写 #include "DuiLib/UIlib.h"，避免与其他库的 UIlib.h 冲突
target_include_directories(DuiLib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/..)