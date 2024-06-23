find_package(Python REQUIRED)

add_subdirectory(src)

file(GLOB build_wheel_SOURCE_FILES pyproject.toml setup.py)

add_custom_target(build_wheel
    COMMAND ${CMAKE_COMMAND} -E env PREBUILT_FILE=$<TARGET_FILE:grc> ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/setup.py bdist_wheel
    SOURCES ${build_wheel_SOURCE_FILES}
    )

add_dependencies(build_wheel grc)
