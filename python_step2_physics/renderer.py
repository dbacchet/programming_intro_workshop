import os
import numpy as np
from pyrr import Matrix44, Quaternion, Vector3, Vector4, vector

import moderngl

import moderngl_window as mglw


class Example(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Example"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = False

    # resource_dir = os.path.normpath(os.path.join(__file__, '../resources'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)

class Camera():
    def __init__(self, ratio):
        self._field_of_view_degrees = 45.0
        self._z_near = 1
        self._z_far = 500
        self._ratio = ratio

        self.position = Vector3([0.0, 0.0, -100.0])
        self.target = Vector3([0,0,0])
        self.azimuth = 0.0
        self.elevation = 0.0/180.0*3.1415
        self.distance = 100.0

        self.mat_lookat = Matrix44.identity()
        self.mat_projection = Matrix44.perspective_projection(
            self._field_of_view_degrees,
            self._ratio,
            self._z_near,
            self._z_far)

    def update(self):
        center = Matrix44.from_translation(self.target)
        azim = Matrix44.from_z_rotation(self.azimuth)
        elev = Matrix44.from_x_rotation(self.elevation)
        dist = Matrix44.from_translation([0,0,self.distance])
        self.mat_lookat = center * azim * elev * dist

def grid(size, steps):
    u = np.repeat(np.linspace(-size, size, steps), 2)
    v = np.tile([-size, size], steps)
    w = np.zeros(steps * 2)
    r = np.zeros(steps * 2) + 0.2
    g = np.zeros(steps * 2) + 0.2 
    b = np.zeros(steps * 2) + 0.2
    a = np.ones(steps * 2)
    vertices = np.concatenate([np.dstack([u, v, w,r,g,b,a]), np.dstack([v, u, w,r,g,b,a])])
    return vertices

def cylinder(radius, height, color_top = [1,0,0,1], color_side = [0.5,0,0,1], steps=10):
    """build a cylinder with triangles"""
    delta_a = 2*np.pi/steps;
    vertices = []
    for i in range(steps):
        a1 = delta_a*i
        a2 = delta_a*(i+1)
        p0 = [0,0,0]
        p1 = [radius*np.cos(a1),radius*np.sin(a1),0]
        p2 = [radius*np.cos(a2),radius*np.sin(a2),0]
        p3 = [0,0,height]
        p4 = [radius*np.cos(a1),radius*np.sin(a1),height]
        p5 = [radius*np.cos(a2),radius*np.sin(a2),height]
        # add triangles
        # top,bottom
        vertices.extend([p0+color_top,p1+color_top,p2+color_top])
        vertices.extend([p3+color_top,p4+color_top,p5+color_top])
        # side
        vertices.extend([p1+color_side,p2+color_side,p4+color_side])
        vertices.extend([p2+color_side,p5+color_side,p4+color_side])
    # small arrow
    a = 0.5
    b = 1-a
    ap0 = [radius*a, -radius*b, height*1.01]
    ap1 = [radius, 0, height*1.01]
    ap2 = [radius*a,  radius*b, height*1.01]
    vertices.extend([ap0+color_side,ap1+color_side,ap2+color_side])
    return np.array(vertices)

class SimpleRenderer(Example):
    gl_version = (3, 3)
    samples = 8
    title = "Renderer"

    objects = []
    callback = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog_vertexcolor = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform mat4 Mvp;

                in vec3 in_vert;
                in vec4 in_color;

                out vec4 v_color;

                void main() {
                    gl_Position = Mvp * vec4(in_vert, 1.0);
                    v_color = in_color;
                }
            ''',
            fragment_shader='''
                #version 330

                in vec4 v_color;
                out vec4 f_color;

                void main() {
                    f_color = v_color;
                }
            ''',
        )

        self.camera = Camera(self.aspect_ratio)
        self.mvp = self.prog_vertexcolor['Mvp']
        self.grid_vbo = self.ctx.buffer(grid(100, 41).astype('f4'))
        self.grid_vao = self.ctx.simple_vertex_array(self.prog_vertexcolor, self.grid_vbo, 'in_vert','in_color')

        self.cyl_vbo = self.ctx.buffer(cylinder(1,0.5,steps = 20).astype('f4'))
        self.cyl_vao = self.ctx.simple_vertex_array(self.prog_vertexcolor, self.cyl_vbo, 'in_vert','in_color')


    def mouse_drag_event(self, x: int, y: int, dx, dy):
        self.camera.azimuth += dx*0.01
        self.camera.elevation += dy*0.01

    def mouse_scroll_event(self, dx, dy):
        self.camera.distance *= (1-dy*0.05);

    def key_event(self, key, action, modifiers):
        pass

    def render(self, time, frame_time):
        if SimpleRenderer.callback and frame_time>0:
            SimpleRenderer.callback(frame_time)
        # print(time, frame_time)
        self.camera.update()

        self.ctx.clear(0.1, 0.1, 0.1)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # print('---------')
        # print(self.camera.elevation, self.camera.azimuth)
        # print(self.camera.mat_lookat*Vector4([0,0,0,1]))

        # grid
        self.mvp.write((self.camera.mat_projection * self.camera.mat_lookat.inverse).astype('f4'))
        self.grid_vao.render(moderngl.LINES)
        # objects
        for obj in SimpleRenderer.objects:
            # model matrix
            scale = Matrix44.from_scale([obj.radius, obj.radius, obj.radius])
            rotation = Matrix44.from_z_rotation(-np.arctan2(obj.vel.y, obj.vel.x))
            translation = Matrix44.from_translation([obj.pos.x, obj.pos.y,0])
            model = translation * rotation * scale
            # render object
            self.mvp.write((self.camera.mat_projection * self.camera.mat_lookat.inverse * model).astype('f4'))
            self.cyl_vao.render(moderngl.TRIANGLES)



if __name__ == '__main__':
    SimpleRenderer.run()
