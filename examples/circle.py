import random
from math import cos, pi, sin

import ModernGL
from miniglm import FloatArray, Vec2, Vec3
from ModernGL.ext.examples import run_example


class Obstacle:

    def __init__(self, _ctx, _pos = 0):
        self.ctx = _ctx
        self.pos = _pos
        self.heigth = random.random() * 100 % 81 + 10

        while self.pos > pi:
            self.pos -= pi

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 330

                uniform float Heigth;
                uniform float Angle;
                uniform float Pos;

                in vec2 in_vert;
                in vec3 in_color;

                out vec3 out_color;

                mat4 rotationMatrix(vec3 axis, float angle){
                    axis = normalize(axis);
                    float s = sin(angle);
                    float c = cos(angle);
                    float oc = 1.0 - c;

                    return mat4(
                        oc * axis.x * axis.x + c, oc * axis.x * axis.y - axis.z * s, oc * axis.z * axis.x + axis.y * s,  0.0,
                        oc * axis.x * axis.y + axis.z * s, oc * axis.y * axis.y + c, oc * axis.y * axis.z - axis.x * s,  0.0,
                        oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c, 0.0,
                        0.0, 0.0, 0.0, 1.0
                    );
                }

                void main() {
                    out_color = in_color;
                    float x = (-1 + 2 * ((in_vert.x + 250) / 500));
                    float y = -(-1 + 2 * ((in_vert.y + 500) / 500));
                    float h =  (-1 + 2 * ((Heigth) / 500));
                    gl_Position = rotationMatrix(vec3(0, 0, 1), -Angle - Pos) * vec4(x * 0.75, (y) * 0.75, 0, 1.0) + vec4(0, -1, 0, 0);
                }
            '''),

            self.ctx.fragment_shader('''
                #version 330

                in vec3 out_color;

                out vec4 color;

                void main() {
                    color = vec4(out_color, 1.0);
                }
            ''')

        ]
        )

        body = FloatArray((
            0.0, 0.0, 0.0, 0.0, 1.0,
            0.0, self.heigth, 0.0, 1.0, 0.0,
            10, 0.0, 1.0, 0.0, 0.0,

            0.0, self.heigth, 0.0, 0.0, 1.0,
            10, 0.0, 0.0, 1.0, 0.0,
            10, self.heigth, 1.0, 0.0, 0.0,
        ))

        self.vbo = self.ctx.buffer(bytes(body))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['in_vert', 'in_color'])
        self.Heigth = self.prog.uniforms['Heigth']
        self.Pos = self.prog.uniforms['Pos']
        self.Angle = self.prog.uniforms['Angle']


    def Render(self, angle):
        self.Heigth.value = self.heigth
        self.vao.render(ModernGL.TRIANGLE_STRIP)
        self.Pos.value = self.pos
        self.Angle.value = angle



class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 330

                uniform float Angle;
                uniform float Ratio;
                uniform float vertex_ID;
                uniform vec2 Push;

                in vec2 in_vert;

                out vec2 out_vert;
                out float out_vertex_ID;

                mat4 rotationMatrix(vec3 axis, float angle) {
                    axis = normalize(axis);
                    float s = sin(angle);
                    float c = cos(angle);
                    float oc = 1.0 - c;

                    return mat4(
                        oc * axis.x * axis.x + c, oc * axis.x * axis.y - axis.z * s, oc * axis.z * axis.x + axis.y * s, 0.0,
                        oc * axis.x * axis.y + axis.z * s, oc * axis.y * axis.y + c, oc * axis.y * axis.z - axis.x * s, 0.0,
                        oc * axis.z * axis.x - axis.y * s, oc * axis.y * axis.z + axis.x * s, oc * axis.z * axis.z + c, 0.0,
                        0.0, 0.0, 0.0, 1.0
                    );
                }


                void main() {
                    out_vertex_ID = vertex_ID;

                    if(vertex_ID == 0.0) {

                        vec4 rotated = vec4(in_vert, 0, 1.0) * rotationMatrix(vec3(0, 0, 1), Angle);
                        vec2 verts = 0.75 * rotated.xy * vec2(Ratio, 1) + vec2(0, -1);
                        out_vert = in_vert;
                        gl_Position = vec4(verts, 0.0, 1.0);

                    }else if(vertex_ID == 1.0) {

                        float x = (-1 + 2 * ((in_vert.x + Push.x) / 500));
                        float y = -(-1 + 2 * ((in_vert.y + Push.y) / 500));
                        gl_Position = vec4(x, y, 0.0, 1.0);

                    }
                }
            '''),

            self.ctx.fragment_shader('''
                #version 330

                in vec2 out_vert;
                in float out_vertex_ID;

                out vec4 color;

                void main() {
                    if(out_vertex_ID == 0.0) {

                        color = vec4(out_vert, 0.1, 1.0);

                    }else if(out_vertex_ID == 1.0) {

                        color = vec4(0.0, 0.0, 0.0, 1.0);

                    }
                }
            ''')
        ])


        self.Angle = self.prog.uniforms['Angle']
        self.Ratio = self.prog.uniforms['Ratio']
        self.Push = self.prog.uniforms['Push']
        self.vertex_ID = self.prog.uniforms['vertex_ID']
        ls = []

        for i in range(0, int(2 * pi * 51)):
            ls.append(cos(i / 50))  # + (random.random() / 50))
            ls.append(sin(i / 50))  # - (random.random() / 50))
            ls.append(0)
            ls.append(0)

        circle = FloatArray(ls)
        self.vbo = self.ctx.buffer(bytes(circle))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['in_vert'])
        self.angleValue = 0
        self.width = 500
        self.heigth = 500

        square = FloatArray((
            0.0, 0.0,
            0.0, 10,
            10, 0.0,

            0.0, 10,
            10, 0.0,
            10, 10,
        ))

        self.vbo1 = self.ctx.buffer(bytes(square))
        self.vao1 = self.ctx.simple_vertex_array(self.prog, self.vbo1, ['in_vert'])

        self.vy = 0
        self.jumping = False
        self.playerPos = Vec2((250, 303))
        self.jumpHeight = 0.0

        self.obstacles = [Obstacle(self.ctx, 2.14)]

    def render(self):
        self.update()
        self.ctx.clear(0.2, 0.4, 0.7)
        self.vertex_ID.value = 0.0
        self.vao.render(ModernGL.TRIANGLE_STRIP)
        self.vertex_ID.value = 1.0
        self.Push.value = self.playerPos.tup
        self.vao1.render()
        clear = False
        clear_i = []
        for i in range(len(self.obstacles)):
            self.obstacles[i].Render(self.angleValue)
            if sin(self.angleValue + self.obstacles[i].pos) < 0.05 and sin(self.angleValue + self.obstacles[i].pos) > -0.05:
                if self.jumpHeight < self.obstacles[i].heigth:
                    clear = True
                    clear_i.append(i)


        if clear:
            for i in clear_i:
                if i < len(self.obstacles):
                    self.obstacles.pop(i)


    def update(self):
        if random.uniform(0, 1000) < 50 and len(self.obstacles) < 5:
            self.obstacles.append(Obstacle(self.ctx, random.uniform(1 / 4 * pi,  2 * pi)))
        self.angleValue += 0.01
        self.Angle.value = self.angleValue
        self.Ratio.value = self.wnd.size[0] / self.wnd.size[1]
        self.ctx.viewport = self.wnd.viewport

        if self.wnd.key_down(' '):
            if not self.jumping:
                self.jumping = True
                self.vy = -7

        if self.wnd.key_pressed('Q'):
            print("adding")
            self.obstacles.append(Obstacle(self.ctx, random.uniform(0, pi)))

        if self.vy < 0:
            self.vy *= 0.95
        elif self.vy > 0:
            self.vy *= 1.05
        if self.playerPos.y < 207:
            self.vy = -self.vy

        self.jumpHeight = 303 - self.playerPos.y

        if self.playerPos.y > 303.5:
            self.vy = 0
            self.playerPos = Vec2((self.width / 2, 303))
            self.jumping = False

        self.playerPos = Vec2((self.playerPos.x, self.playerPos.y + self.vy))


run_example(Example, size = (500, 500))
