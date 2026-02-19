# cmake file for xlgamebox
# XUnzip.cpp duplicates DuiLib unzip - exclude it

aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR} RootSrc)
list(FILTER RootSrc EXCLUDE REGEX "XUnzip\\.cpp$")
set(source_files ${RootSrc} XLGameBox.rc)

include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${PROJECT_SOURCE_DIR}/DuiLib)

add_executable(xlgamebox WIN32 ${source_files})
target_link_libraries(xlgamebox DuiLib user32 gdi32 comctl32)

set_target_properties(xlgamebox PROPERTIES
  LINK_FLAGS "/SUBSYSTEM:WINDOWS"
  FOLDER "Demos")

demo_copy_data(xlgamebox)
