add_subdirectory(src/grc)
add_subdirectory(tests)

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/src/grc/grc.conf.in
    ${CMAKE_CURRENT_BINARY_DIR}/grc.conf
@ONLY)
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/src/grc/00-grc-docs.conf.in
    ${CMAKE_CURRENT_BINARY_DIR}/00-grc-docs.conf
@ONLY)

install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/grc.conf
    DESTINATION ${GR_PREFSDIR}
)
install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/00-grc-docs.conf
    DESTINATION ${GR_PREFSDIR}
)

find_program(HAVE_XDG_UTILS xdg-desktop-menu)

if(UNIX AND HAVE_XDG_UTILS AND ENABLE_POSTINSTALL)
    configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/src/grc/scripts/freedesktop/grc_setup_freedesktop.in
        ${CMAKE_CURRENT_BINARY_DIR}/grc_setup_freedesktop
        FILE_PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
    @ONLY)
   install (
        CODE "execute_process(COMMAND ${CMAKE_CURRENT_BINARY_DIR}/grc_setup_freedesktop install ${CMAKE_CURRENT_SOURCE_DIR}/src/grc/scripts/freedesktop)"
    )
endif(UNIX AND HAVE_XDG_UTILS AND ENABLE_POSTINSTALL)

if(UNIX AND ENABLE_TESTING)
    find_program(APPSTREAMCLI appstream-util)
    if(APPSTREAMCLI)
        GR_ADD_TEST(metainfo_test "${APPSTREAMCLI}" validate-relax "${CMAKE_CURRENT_SOURCE_DIR}/src/grc/scripts/freedesktop/org.gnuradio.grc.metainfo.xml")
    endif(APPSTREAMCLI)
endif(UNIX AND ENABLE_TESTING)
