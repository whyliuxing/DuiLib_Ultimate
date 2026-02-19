# cmake file for HiDPITest

aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR} RootSrc)
set(source_files ${RootSrc} HiDPITest.rc)

include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${PROJECT_SOURCE_DIR}/DuiLib)

add_executable(HiDPITest WIN32 ${source_files})
target_link_libraries(HiDPITest DuiLib user32 gdi32 comctl32)

set_target_properties(HiDPITest PROPERTIES
  LINK_FLAGS "/SUBSYSTEM:WINDOWS"
  FOLDER "Demos")

demo_copy_data(HiDPITest)
