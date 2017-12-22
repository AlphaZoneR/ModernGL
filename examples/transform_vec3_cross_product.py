import ModernGL
import numpy as np

ctx = ModernGL.create_standalone_context()

prog = ctx.program([
    ctx.vertex_shader('''
        #version 330

        in vec3 in_vec_1;
        in vec3 in_vec_2;
        out vec3 out_vec_cross; 
        
        void main() {
            out_vec_cross = cross(in_vec_1, in_vec_2);
        }

    ''')
], ['out_vec_cross'])

vertices = np.array([[1.0, 2.0, 3.0], [1.0, 1.0, 1.0]])

vbo1 = ctx.buffer(vertices.astype('f4').tobytes())
vbo2 = ctx.buffer(b'\x00' * int(vbo1.size / 2))

vao = ctx.simple_vertex_array(prog, vbo1, ['in_vec_1', 'in_vec_2'])
vao.transform(vbo2)

output = np.frombuffer(vbo2.read(), dtype='f4')

print(output)