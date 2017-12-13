import ModernGL
import numpy as np

ctx = ModernGL.create_standalone_context()

prog = ctx.program([
    ctx.vertex_shader(
    """
        #version 330

        in float in_float;
        out float out_float; 
        
        void main(){
            out_float = in_float * 3.14;
        }

    """
    )
    ], ['out_float'])

vbo1 = ctx.buffer(np.array([23.15],).astype('f4').tobytes())
vbo2 = ctx.buffer(b'\x00' * vbo1.size)

vao = ctx.simple_vertex_array(prog, vbo1, ['in_float'])
vao.transform(vbo2)

print(np.frombuffer(vbo2.read(), dtype='f4'))