# cmake file for ADMonSetup

aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR} RootSrc)
set(source_files ${RootSrc} ADMonSetup.rc)

include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${PROJECT_SOURCE_DIR}/DuiLib)

add_executable(ADMonSetup WIN32 ${source_files})
target_link_libraries(ADMonSetup DuiLib user32 gdi32 comctl32)

set_target_properties(ADMonSetup PROPERTIES
  LINK_FLAGS "/SUBSYSTEM:WINDOWS"
  FOLDER "Demos")

demo_copy_data(ADMonSetup)
