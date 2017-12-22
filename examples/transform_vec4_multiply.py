import ModernGL
import numpy as np

ctx = ModernGL.create_standalone_context()

prog = ctx.program([
    ctx.vertex_shader('''
        #version 330

        in vec4 in_vec_1;
        in vec4 in_vec_2;
        in vec4 in_vec_3;

        out vec4 out_vec; 
        
        void main() {
            out_vec = in_vec_1 * in_vec_2 + in_vec_3;
        }

    ''')
], ['out_vec'])

vertices = np.array([[1.0, 2.0, 3.0, 4.0], [1.0, 1.0, 1.0, 1.0], [3.0, 2.0, 1.0, 0.0]])

vbo1 = ctx.buffer(vertices.astype('f4').tobytes())
vbo2 = ctx.buffer(b'\x00' * int(vbo1.size / 3))

vao = ctx.simple_vertex_array(prog, vbo1, ['in_vec_1', 'in_vec_2', 'in_vec_3'])
vao.transform(vbo2)

output = np.frombuffer(vbo2.read(), dtype='f4')

print(output)