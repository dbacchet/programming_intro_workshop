# with sokol_app
if (APPLE)
    add_library(sokol_sapp sokol_impl_sapp.mm)
    # - on macOS with GL: Cocoa, QuartzCore, OpenGL
    target_compile_definitions(sokol_sapp PRIVATE SOKOL_GLCORE33)
    target_link_libraries(sokol_sapp "-framework Cocoa"
                                     "-framework QuartzCore"
                                     "-framework OpenGL")
    # - on macOS with Metal: Cocoa, QuartzCore, Metal, MetalKit
    # target_compile_definitions(sokol_sapp PRIVATE SOKOL_METAL)
    # target_link_libraries(sokol_sapp "-framework Cocoa"
    #                                  "-framework QuartzCore"
    #                                  "-framework Metal"
    #                                  "-framework MetalKit")
else()
    find_package(Threads REQUIRED)
    set(OpenGL_GL_PREFERENCE GLVND)
    find_package(OpenGL REQUIRED)
    add_library(sokol_sapp sokol_impl_sapp.cpp)
    # - on Linux: X11, Xi, Xcursor, GL, dl, pthread, m(?)
    target_compile_definitions(sokol_sapp PRIVATE SOKOL_GLCORE33)
    target_link_libraries(sokol_sapp Threads::Threads OpenGL::OpenGL "-lX11" "-lXi" "-lXcursor" "-ldl")
endif()


add_executable(renderer-sapp renderer-sapp.cpp sample_app.cpp)
target_link_libraries(renderer-sapp PUBLIC 
                                         sokol_sapp)

