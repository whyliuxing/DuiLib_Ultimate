# cmake file for gamebox
# XUnzip.cpp duplicates DuiLib unzip - exclude it

aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR} RootSrc)
list(FILTER RootSrc EXCLUDE REGEX "XUnzip\\.cpp$")
set(source_files ${RootSrc} GameBox.rc)

include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${PROJECT_SOURCE_DIR}/DuiLib)

add_executable(gamebox WIN32 ${source_files})
target_link_libraries(gamebox DuiLib user32 gdi32 comctl32)

set_target_properties(gamebox PROPERTIES
  LINK_FLAGS "/SUBSYSTEM:WINDOWS"
  FOLDER "Demos")

demo_copy_data(gamebox)
