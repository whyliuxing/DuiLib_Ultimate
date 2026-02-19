# cmake file for duidemo

aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR} RootSrc)
set(source_files ${RootSrc} duidemo.rc)

include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${PROJECT_SOURCE_DIR}/DuiLib)

add_executable(duidemo WIN32 ${source_files})
target_link_libraries(duidemo DuiLib user32 gdi32 comctl32)

set_target_properties(duidemo PROPERTIES
  LINK_FLAGS "/SUBSYSTEM:WINDOWS"
  FOLDER "Demos")

# 将 data（skin、plugins 等）拷贝到 exe 输出目录
demo_copy_data(duidemo)
