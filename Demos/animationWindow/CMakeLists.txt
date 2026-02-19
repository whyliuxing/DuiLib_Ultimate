# cmake file for animationWindow
# Builds UiFeatureEffect DLL first, then animationwindow exe

add_subdirectory(UiFeatureEffect)

set(animationwindow_SRCS
  main.cpp
  FrameWnd.cpp
  stdafx.cpp
  Controls/AnimLayout.cpp
  UIEffect/IUiEffectManagerImpl.cpp
  Desktop.rc
)

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}/Controls
  ${CMAKE_CURRENT_SOURCE_DIR}/UIEffect
  ${PROJECT_SOURCE_DIR}/DuiLib
)

add_executable(animationwindow WIN32 ${animationwindow_SRCS})
target_link_libraries(animationwindow UiFeatureEffect DuiLib user32 gdi32 comctl32)
target_compile_definitions(animationwindow PRIVATE UILIB_STATIC)

set_target_properties(animationwindow PROPERTIES
  LINK_FLAGS "/SUBSYSTEM:WINDOWS"
  FOLDER "Demos"
)

demo_copy_data(animationwindow)
