# cmake file for UiFeatureEffect DLL

set(UiFeatureEffect_SRCS
  dllmain.cpp
  Effect.cpp
  stdafx.cpp
  UiFeatureEffect.cpp
  Image/ColorHelper.cpp
  Image/ImageProcess.cpp
  UiFeatureEffect.rc
)

add_library(UiFeatureEffect SHARED ${UiFeatureEffect_SRCS})
target_compile_definitions(UiFeatureEffect PRIVATE
  _USRDLL
  UiFeatureEffect_EXPORTS
)
target_include_directories(UiFeatureEffect PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}/Image
  ${CMAKE_CURRENT_SOURCE_DIR}/Graph
  ${CMAKE_CURRENT_SOURCE_DIR}/Motion
  ${CMAKE_CURRENT_SOURCE_DIR}/Interface
  ${CMAKE_CURRENT_SOURCE_DIR}/CPUID
  ${PROJECT_SOURCE_DIR}/DuiLib
)
target_link_libraries(UiFeatureEffect gdiplus)
set_target_properties(UiFeatureEffect PROPERTIES
  WINDOWS_EXPORT_ALL_SYMBOLS OFF
  FOLDER "Demos"
)

if(MSVC)
  target_link_options(UiFeatureEffect PRIVATE "/DEF:${CMAKE_CURRENT_SOURCE_DIR}/UiFeatureEffect.def")
endif()
