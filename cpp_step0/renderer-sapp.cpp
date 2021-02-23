#include "renderer-sapp.h"

#include <stdlib.h> /* rand() */
#include "sokol_app.h"
#include "sokol_gfx.h"
#include "sokol_glue.h"
#define HANDMADE_MATH_IMPLEMENTATION
#define HANDMADE_MATH_NO_SSE
#include "HandmadeMath.h"

#include "vmath.h"
#include "renderer-sapp.glsl.h"

#include <vector>
#include <cstdio>

#define MAX_PARTICLES (512 * 1024)
#define NUM_PARTICLES_EMITTED_PER_FRAME (10)

class Camera {
  public:
    void init(void) {
        position = math::Vector3f(0, 0, -100);
        target = math::Vector3f(0, 0, 0);
        transform = math::matrix4_identity<float>();
        mat_projection =
            math::create_perspective(float(fov_deg / 180 * M_PI), sapp_widthf() / sapp_heightf(), z_near, z_far);
    }

    void update() {
        math::Matrix4f center = math::create_translation<float>(target);
        math::Matrix4f azim =
            math::create_transformation<float>({0, 0, 0}, math::quat_from_euler_321(0.0f, 0.0f, azimuth));
        math::Matrix4f elev =
            math::create_transformation<float>({0, 0, 0}, math::quat_from_euler_321(elevation, 0.0f, 0.0f));
        math::Matrix4f dist = math::create_translation<float>({0, 0, distance});
        transform = center * azim * elev * dist;
        inverse_transform = math::inverse(transform);
    }

    float fov_deg = 45.0f;
    float z_near = 1.0f;
    float z_far = 500.0f;
    float aspect_ratio = 16.0f / 9.0f;
    math::Vector3f position;
    math::Vector3f target;

    float azimuth = 0.0f;
    float elevation = 0.0f / 180.0f * M_PI;
    float distance = 100.0f;

    math::Matrix4f mat_projection;
    math::Matrix4f transform;
    math::Matrix4f inverse_transform;
};

static struct {
    sg_pass_action pass_action;
    sg_pipeline pip_vertexcolor;
    sg_bindings bind_vertexcolor;
    uint32_t num_grid_vertices = 0;
    sg_pipeline pip_inst;
    sg_bindings bind_inst;
    float rz = 0;
    int cur_num_particles;
    hmm_vec3 pos[MAX_PARTICLES];
    hmm_vec3 vel[MAX_PARTICLES];
    frame_callback callback = nullptr;
    Camera camera;
} state;

struct Color {
    uint8_t r = 180;
    uint8_t g = 180;
    uint8_t b = 180;
    uint8_t a = 255;
};

struct Vertex {
    hmm_vec3 pos;
    Color color = {180, 180, 180, 255};
};

std::vector<Vertex> create_grid(float len, float step) {
    std::vector<Vertex> vertices;
    const int32_t major = 5;
    int32_t nlines = len / step;
    Color col_x = {120, 20, 20, 255};
    Color col_y = {20, 120, 20, 255};
    Color col1 = {40, 40, 40, 255};
    Color col2 = {70, 70, 70, 255};
    col_x = {120, 20, 20, 255};
    col_y = {20, 120, 20, 255};
    col1 = {40, 40, 40, 255};
    col2 = {70, 70, 70, 255};
    // main axis
    vertices.push_back({{-len, 0, 0}, col_x});
    vertices.push_back({{len, 0, 0}, col_x});
    vertices.push_back({{0, -len, 0}, col_y});
    vertices.push_back({{0, len, 0}, col_y});
    // other lines
    for (int32_t i = 1; i <= nlines; i++) {
        vertices.push_back({{-len, i * step, 0}, i % major ? col1 : col2});
        vertices.push_back({{len, i * step, 0}, i % major ? col1 : col2});
        vertices.push_back({{-len, -i * step, 0}, i % major ? col1 : col2});
        vertices.push_back({{len, -i * step, 0}, i % major ? col1 : col2});
        vertices.push_back({{i * step, -len, 0}, i % major ? col1 : col2});
        vertices.push_back({{i * step, len, 0}, i % major ? col1 : col2});
        vertices.push_back({{-i * step, -len, 0}, i % major ? col1 : col2});
        vertices.push_back({{-i * step, len, 0}, i % major ? col1 : col2});
    }
    return vertices;
}

void init(void) {
    sg_setup((sg_desc){.context = sapp_sgcontext()});

    /* a pass action for the default render pass */
    state.pass_action = {0};
    state.pass_action.colors[0] = {.action = SG_ACTION_CLEAR, .value = {0.1f, 0.1f, 0.1f, 1.0f}};

    // //// //
    // grid //
    // //// //

    auto grid_vertices = create_grid(100, 5);
    state.bind_vertexcolor = {0};
    state.bind_vertexcolor.vertex_buffers[0] =
        sg_make_buffer((sg_buffer_desc){.type = SG_BUFFERTYPE_VERTEXBUFFER,
                                        .data = {grid_vertices.data(), grid_vertices.size() * sizeof(Vertex)},
                                        .label = "grid-vertices"});
    state.num_grid_vertices = grid_vertices.size();
    // a pipeline object
    sg_pipeline_desc vc_pip_desc = {0};
    vc_pip_desc.layout = {0};
    vc_pip_desc.layout.attrs[ATTR_vs_vertexcolor_pos] = {.buffer_index = 0, .format = SG_VERTEXFORMAT_FLOAT3};
    vc_pip_desc.layout.attrs[ATTR_vs_vertexcolor_color0] = {.buffer_index = 0, .format = SG_VERTEXFORMAT_UBYTE4N};
    vc_pip_desc.shader = sg_make_shader(vertexcolor_shader_desc(sg_query_backend()));
    vc_pip_desc.primitive_type = SG_PRIMITIVETYPE_LINES;
    // vc_pip_desc.index_type = SG_INDEXTYPE_UINT16;
    vc_pip_desc.cull_mode = SG_CULLMODE_NONE;
    vc_pip_desc.depth = {
        .compare = SG_COMPAREFUNC_LESS_EQUAL,
        .write_enabled = true,
    };
    vc_pip_desc.label = "vertexcolor-pipeline";
    state.pip_vertexcolor = sg_make_pipeline(vc_pip_desc);

    // /////// //
    // objects //
    // /////// //
    /* vertex buffer for static geometry, goes into vertex-buffer-slot 0 */
    const float r = 0.05f;
    const std::vector<Vertex> vertices = {
        // positions            colors
        {{0.0f, -r, 0.0f}, {255, 0, 0, 255}}, //
        {{r, 0.0f, r}, {0, 255, 0, 255}},     //
        {{r, 0.0f, -r}, {0, 0, 255, 255}},    //
        {{-r, 0.0f, -r}, {255, 255, 0, 255}}, //
        {{-r, 0.0f, r}, {0, 255, 255, 255}},  //
        {{0.0f, r, 0.0f}, {255, 0, 255, 255}} //
    };
    state.bind_inst.vertex_buffers[0] =
        sg_make_buffer((sg_buffer_desc){//.type = SG_BUFFERTYPE_VERTEXBUFFER,
                                        .data = {vertices.data(), vertices.size() * sizeof(Vertex)},
                                        .label = "geometry-vertices"});

    /* index buffer for static geometry */
    const uint16_t indices[] = {
        0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 1, //
        5, 1, 2, 5, 2, 3, 5, 3, 4, 5, 4, 1  //
    };
    state.bind_inst.index_buffer = sg_make_buffer(
        (sg_buffer_desc){.type = SG_BUFFERTYPE_INDEXBUFFER, .data = SG_RANGE(indices), .label = "geometry-indices"});

    /* empty, dynamic instance-data vertex buffer, goes into vertex-buffer-slot 1 */
    state.bind_inst.vertex_buffers[1] = sg_make_buffer(
        (sg_buffer_desc){.size = MAX_PARTICLES * sizeof(hmm_vec3), .usage = SG_USAGE_STREAM, .label = "instance-data"});

    /* a shader */
    sg_shader shd = sg_make_shader(instancing_shader_desc(sg_query_backend()));

    /* a pipeline object */
    sg_pipeline_desc pip_desc = {0};
    pip_desc.layout = {0};
    /* vertex buffer at slot 1 must step per instance */
    pip_desc.layout.buffers[1].step_func = SG_VERTEXSTEP_PER_INSTANCE,
    pip_desc.layout.attrs[ATTR_vs_instancing_pos] = {.buffer_index = 0, .format = SG_VERTEXFORMAT_FLOAT3};
    pip_desc.layout.attrs[ATTR_vs_instancing_color0] = {.buffer_index = 0, .format = SG_VERTEXFORMAT_UBYTE4N};
    pip_desc.layout.attrs[ATTR_vs_instancing_inst_pos] = {.buffer_index = 1, .format = SG_VERTEXFORMAT_FLOAT3};
    pip_desc.shader = shd;
    pip_desc.index_type = SG_INDEXTYPE_UINT16;
    pip_desc.cull_mode = SG_CULLMODE_BACK;
    pip_desc.depth = {
        .compare = SG_COMPAREFUNC_LESS_EQUAL,
        .write_enabled = true,
    };
    pip_desc.label = "instancing-pipeline";
    state.pip_inst = sg_make_pipeline(pip_desc);

    state.camera.init();
}

void event(const sapp_event *e) {
    // close window
    if (e->type == SAPP_EVENTTYPE_KEY_UP && e->key_code == SAPP_KEYCODE_ESCAPE) {

        sapp_request_quit();
    }
    if (e->type == SAPP_EVENTTYPE_MOUSE_DOWN && e->mouse_button == SAPP_MOUSEBUTTON_LEFT) {
        sapp_lock_mouse(true);
    }

    if (e->type == SAPP_EVENTTYPE_MOUSE_UP && e->mouse_button == SAPP_MOUSEBUTTON_LEFT) {
        sapp_lock_mouse(false);
    }
    if (e->type == SAPP_EVENTTYPE_MOUSE_SCROLL) {
        state.camera.distance *= (1 - e->scroll_y / 10);
    }
    if (e->type == SAPP_EVENTTYPE_MOUSE_MOVE) {
        // azimuth/elevation
        if (sapp_mouse_locked()) {
            state.camera.azimuth += -0.003f * e->mouse_dx;
            state.camera.elevation += -0.003f * e->mouse_dy;
        }
    }
}

void frame(void) {
    const float frame_time = 1.0f / 60.0f;
    if (state.callback) {
        state.callback(frame_time);
    }

    state.camera.update();

    /* emit new particles */
    for (int i = 0; i < NUM_PARTICLES_EMITTED_PER_FRAME; i++) {
        if (state.cur_num_particles < MAX_PARTICLES) {
            state.pos[state.cur_num_particles] = HMM_Vec3(0.0, 0.0, 0.0);
            state.vel[state.cur_num_particles] =
                HMM_Vec3(((float)(rand() & 0x7FFF) / 0x7FFF) - 0.5f, ((float)(rand() & 0x7FFF) / 0x7FFF) * 0.5f + 2.0f,
                         ((float)(rand() & 0x7FFF) / 0x7FFF) - 0.5f);
            state.cur_num_particles++;
        } else {
            break;
        }
    }

    /* update particle positions */
    for (int i = 0; i < state.cur_num_particles; i++) {
        state.vel[i].Y -= 1.0f * frame_time;
        state.pos[i].X += state.vel[i].X * frame_time;
        state.pos[i].Y += state.vel[i].Y * frame_time;
        state.pos[i].Z += state.vel[i].Z * frame_time;
        /* bounce back from 'ground' */
        if (state.pos[i].Y < -2.0f) {
            state.pos[i].Y = -1.8f;
            state.vel[i].Y = -state.vel[i].Y;
            state.vel[i].X *= 0.8f;
            state.vel[i].Y *= 0.8f;
            state.vel[i].Z *= 0.8f;
        }
    }

    /* update instance data */
    sg_update_buffer(state.bind_inst.vertex_buffers[1],
                     (sg_range){.ptr = state.pos, .size = (size_t)state.cur_num_particles * sizeof(hmm_vec3)});

    /* model-view-projection matrix */
    // hmm_mat4 proj = HMM_Perspective(60.0f, sapp_widthf() / sapp_heightf(), 0.1f, 500.0f);
    // hmm_mat4 view = HMM_LookAt(HMM_Vec3(0.0f, 15.0f, 120.0f), HMM_Vec3(0.0f, 0.0f, 0.0f), HMM_Vec3(0.0f,
    // 0.0f, 1.0f)); hmm_mat4 view_proj = HMM_MultiplyMat4(proj, view);
    math::Matrix4f view_proj = state.camera.mat_projection * state.camera.inverse_transform;
    // state.rz += 1.0f;
    vs_params_t vs_params;
    // vs_params.mvp = HMM_MultiplyMat4(view_proj, HMM_Rotate(state.rz, HMM_Vec3(0.0f, 0.0f, 1.0f)));
    vs_params.mvp = view_proj;
    ;

    /* ...and draw */
    sg_begin_default_pass(&state.pass_action, sapp_width(), sapp_height());
    // grid
    sg_apply_pipeline(state.pip_vertexcolor);
    sg_apply_bindings(&state.bind_vertexcolor);
    sg_apply_uniforms(SG_SHADERSTAGE_VS, SLOT_vs_params, SG_RANGE(vs_params));
    sg_draw(0, state.num_grid_vertices, 1);
    // objects
    sg_apply_pipeline(state.pip_inst);
    sg_apply_bindings(&state.bind_inst);
    sg_apply_uniforms(SG_SHADERSTAGE_VS, SLOT_vs_params, SG_RANGE(vs_params));
    sg_draw(0, 24, state.cur_num_particles);
    sg_end_pass();
    sg_commit();
}

void cleanup(void) {
    sg_shutdown();
}

sapp_desc create_renderer() {
    return (sapp_desc){
        .init_cb = init,
        .frame_cb = frame,
        .cleanup_cb = cleanup,
        .event_cb = event,
        .width = 1280,
        .height = 720,
        .sample_count = 4,
        .window_title = "Instancing (sokol-app)",
        .gl_force_gles2 = true,
    };
}

void start_renderer(frame_callback callback) {
    // set callbac
    state.callback = callback;
    // run app
    sapp_desc desc = create_renderer();
    sapp_run(&desc);
}
