import ModernGL
import numpy as np

ctx = ModernGL.create_standalone_context()

prog = ctx.program([
    ctx.vertex_shader('''
        #version 330

        in vec2 in_verts;
        out vec2 out_verts; 

        void main() {
            out_verts = in_verts * 2;
        }

    ''')
], ['out_verts'])

vertices = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])

vbo1 = ctx.buffer(vertices.astype('f4').tobytes())
vbo2 = ctx.buffer(b'\x00' * vbo1.size)

vao = ctx.simple_vertex_array(prog, vbo1, ['in_verts'])
vao.transform(vbo2)

output = np.frombuffer(vbo2.read(), dtype = 'f4')

print(output)