import ModernGL
from miniglm import Vec2Array
from ModernGL.ext.examples import run_example


"""
    Renders a blue triangle
"""


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 330

                in vec2 in_vert;

                void main() {
                    gl_Position = vec4(in_vert.x * 720 / 1280, in_vert.y, 0.0, 1.0);
                }
            '''),
            self.ctx.fragment_shader('''
                #version 330

                out vec4 f_color;

                void main() {
                    f_color = vec4(0.3, 0.5, 1.0, 1.0);
                }
            '''),
        ])

        vertices = Vec2Array([
            0.0, 0.6,
            -0.6, -0.6,
            0.6, -0.6,
        ])

        self.vbo = self.ctx.buffer(bytes(vertices))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['in_vert'])

    def render(self):
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.vao.render()


run_example(Example)
