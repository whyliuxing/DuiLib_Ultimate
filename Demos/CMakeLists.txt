# cmake file for Demos

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# 将 data 目录（skin、plugins 等）拷贝到每个 demo 的输出目录，供运行时使用
function(demo_copy_data target_name)
  if(DUILIB_DATA_DIR AND EXISTS ${DUILIB_DATA_DIR})
    add_custom_command(TARGET ${target_name} POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E copy_directory
      ${DUILIB_DATA_DIR}
      $<TARGET_FILE_DIR:${target_name}>
      COMMENT "Copy data (skin, plugins) to ${target_name} output dir")
  endif()
endfunction()

add_subdirectory(duidemo)
add_subdirectory(ADMonSetup)
add_subdirectory(transwnd)
add_subdirectory(HiDPITest)
add_subdirectory(gamebox)
add_subdirectory(xlgamebox)
add_subdirectory(bdwallpaper)
add_subdirectory(animationWindow)