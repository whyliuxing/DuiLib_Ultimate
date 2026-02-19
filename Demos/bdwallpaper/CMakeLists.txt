# cmake file for bdwallpaper

aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR} RootSrc)
aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR}/helper/jsoncpp JsonCppSrc)
set(source_files ${RootSrc} ${JsonCppSrc} BDWallPaper.rc)

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}/helper
  ${CMAKE_CURRENT_SOURCE_DIR}/controlex
  ${CMAKE_CURRENT_SOURCE_DIR}/helper/jsoncpp
  ${PROJECT_SOURCE_DIR}/DuiLib
)

add_executable(bdwallpaper WIN32 ${source_files})
target_link_libraries(bdwallpaper DuiLib user32 gdi32 comctl32 wininet urlmon)

set_target_properties(bdwallpaper PROPERTIES
  LINK_FLAGS "/SUBSYSTEM:WINDOWS"
  FOLDER "Demos")

demo_copy_data(bdwallpaper)
