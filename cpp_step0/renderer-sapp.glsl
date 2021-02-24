//------------------------------------------------------------------------------
//  shaders for instancing-sapp sample
//------------------------------------------------------------------------------
@ctype mat4 math::Matrix4f

@vs vs_vertexcolor
uniform vs_params {
    mat4 mvp;
};

in vec3 pos;
in vec4 color0;

out vec4 color;

void main() {
    vec4 pos = vec4(pos, 1.0);
    gl_Position = mvp * pos;
    color = color0;
}
@end

@fs fs_vertexcolor
in vec4 color;
out vec4 frag_color;
void main() {
    frag_color = color;
}
@end

@program vertexcolor vs_vertexcolor fs_vertexcolor

@vs vs_instancing
uniform vs_params {
    mat4 mvp;
};

in vec3 pos;
in vec4 color0;
in vec4 inst_tf_c1;
in vec4 inst_tf_c2;
in vec4 inst_tf_c3;
in vec4 inst_tf_c4;

out vec4 color;

void main() {
    vec4 pos = vec4(pos, 1.0);
    mat4 inst_tf = mat4(inst_tf_c1, inst_tf_c2, inst_tf_c3, inst_tf_c4);
    gl_Position = mvp * inst_tf * pos;
    color = color0;
}
@end

@fs fs_instancing
in vec4 color;
out vec4 frag_color;
void main() {
    frag_color = color;
}
@end

@program instancing vs_instancing fs_instancing

