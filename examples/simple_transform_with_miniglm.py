import ModernGL, os
from miniglm import Vec3, mat4_perspective, mat4_look_at
from math import cos, sin
from ModernGL.ext.obj import Obj
from ModernGL.ext.examples import run_example

def local(*path):
    return os.path.join(os.path.dirname(__file__), *path)


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()
        self.prog = self.ctx.program([
            self.ctx.vertex_shader(
                """
                    #version 330
                    uniform int ID;
                    uniform mat4 MVP;
                    uniform vec3 pos;
                    in vec3 in_verts;
                    out float obj_id;

                    void main(){
                        gl_Position = MVP * vec4(in_verts + pos, 1.0);
                        obj_id = ID;
                    }

                """
            ),
            self.ctx.fragment_shader(
                """
                    #version 330
                    in float obj_id;
                    out vec4 color;

                    void main(){
                        if(obj_id == 1){
                            color = vec4(0.1, 0.0, 0.6, 1);
                        }else{
                            color = vec4(0.5, 0.0, 0.6, 1);
                        }
                        
                    }
                """
            )
        ])

        self.MVP = self.prog.uniforms['MVP']
        self.posUniform = self.prog.uniforms['pos']
        self.ID = self.prog.uniforms['ID']
        self.pos = Vec3((0, 0, 0))

        obj = Obj.open(local('data', 'sphere.obj'))
        self.vbo = self.ctx.buffer(obj.pack('vx vy vz'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['in_verts'])

        tree = Obj.open(local('data', 'crate.obj'))
        self.vbo1 = self.ctx.buffer(tree.pack('vx vy vz'))
        self.vao1 = self.ctx.simple_vertex_array(self.prog, self.vbo1, ['in_verts'])

        self.speed = 0.05

    def render(self):
        if self.wnd.key_down('S'):
            self.pos = Vec3((self.pos.tup[0] + self.speed, self.pos.tup[1], self.pos.tup[2]))
        if self.wnd.key_down('W'):
            self.pos = Vec3((self.pos.tup[0] - self.speed, self.pos.tup[1], self.pos.tup[2]))
        if self.wnd.key_down('D'):
            self.pos = Vec3((self.pos.tup[0], self.pos.tup[1] + self.speed, self.pos.tup[2]))
        if self.wnd.key_down('A'):
            self.pos = Vec3((self.pos.tup[0], self.pos.tup[1] - self.speed, self.pos.tup[2]))
        if self.wnd.key_down('E'):
            self.pos = Vec3((self.pos.tup[0], self.pos.tup[1], self.pos.tup[2] + self.speed))
        if self.wnd.key_down('Q'):
            self.pos = Vec3((self.pos.tup[0], self.pos.tup[1], self.pos.tup[2] - self.speed))
        
        

        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(0.1, 0.1, 0.1)
        self.ctx.enable(ModernGL.DEPTH_TEST)
        self.posUniform.value = self.pos.tup
        
        proj = mat4_perspective(45.0, self.wnd.size[0] / self.wnd.size[1], 0.1, 1000.0)
        lookat = mat4_look_at(
            (cos(0) * 5, sin(0) * 5, 2),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        self.MVP.write(bytes(proj * lookat))
        self.ID.value = int(1)
        self.vao.render()
        self.ID.value = int(2)
        self.posUniform.value = Vec3((0, 3, -1)).tup
        self.vao1.render()


run_example(Example)
