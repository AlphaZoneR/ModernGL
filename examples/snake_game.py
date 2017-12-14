import ModernGL
import time, random
from math import cos, sin
from miniglm import FloatArray, mat4_ortho, Vec2, mat4_perspective, mat4_look_at, mat4_ortho
from ModernGL.ext.examples import run_example

class Snake:
    def __init__(self):
        self.length = 0
        self.body = []
        self.initLength()
        self.addLength()
        self.addLength()
        self.addLength()
    def initLength(self):
        self.length += 1
        self.body.append({
            "pos" : Vec2((25, 25))
        })
    def addLength(self):
        self.length += 1
        self.body.append({
            "pos" : Vec2((self.getX(), self.getY()))
        })
    def update(self, _x, _y):
        for i in range(self.length - 1, 0, -1):
            self.body[i]['pos'] = self.body[i - 1]['pos']
        self.body[0]['pos'] = Vec2((self.body[0]['pos'].tup[0] + _x, self.body[0]['pos'].tup[1] + _y))
    
    def check(self):
        for b in self.body[1:]:
            if self.getX() == b['pos'].tup[0] and self.getY() == b['pos'].tup[1]:
                self.reset()
                return True

        return False
    
    def reset(self):
        self.__init__()
    
    def getX(self):
        return int(self.body[0]['pos'].tup[0])
    
    def getY(self):
        return int(self.body[0]['pos'].tup[1])

class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()
        self.prog = self.ctx.program([
            self.ctx.vertex_shader(
                """
                    #version 330
                    uniform vec2 Push;
                    uniform float ID;
                    in vec2 in_verts;
                    out float ID_OUT;
                    void main(){
                        float x = -1 + 2 * ((in_verts.x + Push.x) / 500);
                        float y = -(-1 + 2 * ((in_verts.y + Push.y) / 500));
                        ID_OUT = ID;
                        gl_Position = vec4(x, y, 0, 1.0);
                        
                    }
                """
                ),
            self.ctx.fragment_shader(
                """
                    #version 330
                    in float ID_OUT;
                    out vec4 color;

                    void main(){
                        if(ID_OUT == 1.0){
                            color = vec4(0.2, 0.4, 0.7, 1.0);
                        }else if(ID_OUT == 2.0){
                            color = vec4(0.0, 0.0, 0.0, 1.0);
                        }else if(ID_OUT == 3.0){
                            color = vec4(1.0, 0.0, 0.0, 1.0);
                        }
                    }
                """
                )
        ])

        self.Push = self.prog.uniforms['Push']
        self.size = 50
        self.id = self.prog.uniforms['ID']
        square = FloatArray(
            (
                0.0, 0.0,
                0.0, 10,
                10, 0.0,

                0.0, 10,
                10, 0.0,
                10, 10,
            )
        )

        self.vbo = self.ctx.buffer(bytes(square))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['in_verts'])
        self.map = [[0 for j in range(self.size)] for i in range(self.size)]
        
        for i in range(self.size):
            self.map[i][0] = 1
            self.map[i][self.size - 1] = 1
            self.map[0][i] = 1
            self.map[self.size - 1][i] = 1
        
        self.snake = Snake()

        self.pushval = (0, 0)
        
        self.speedx = 0
        self.speedy = 0
        
        self.foodx = int(random.random() * 100) % 49
        self.foody = int(random.random() * 100) % 49
        
        self.gamespeed = 10

        while self.foodx == 0 or self.foody == 0:
            self.foodx = int(random.random() * 100) % 49
            self.foody = int(random.random() * 100) % 49
        
        
        self.lasttime = wnd.time
    
    def render(self):
        
        self.update()
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(0.9, 0.9, 0.9)
        
        self.id.value = 1.0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[j][i] == 1:
                    self.pushval = (i * 10, j * 10)
                    self.Push.value = self.pushval
                    self.vao.render()
        
        self.id.value = 2.0
        for b in self.snake.body:
            self.Push.value = (b['pos'].tup[0] * 10, b['pos'].tup[1] * 10)
            self.vao.render()

        self.id.value = 3.0
        self.Push.value = (self.foodx * 10, self.foody * 10)
        self.vao.render()

    def update(self):
        if self.wnd.time - self.lasttime > 1 / self.gamespeed:
            self.snake.update(self.speedx, self.speedy)
            if self.snake.check():
                self.gamespeed = 10
                self.speedx = 0
                self.speedy = 0
            self.lasttime = self.wnd.time
        
        if self.map[self.snake.getX()][self.snake.getY()] == 1:
                self.snake.reset()
                self.gamespeed = 10
                self.speedx = 0
                self.speedy = 0
        
        if self.snake.getX() == self.foodx and self.snake.getY() == self.foody:
            self.snake.addLength()
            self.gamespeed += 0.5
            self.foodx = int(random.random() * 100) % 49
            self.foody = int(random.random() * 100) % 49
            while self.foodx == 0 or self.foody == 0:
                self.foodx = int(random.random() * 100) % 49
                self.foody = int(random.random() * 100) % 49

        if self.wnd.key_pressed('D') and self.speedx == 0:
            self.speedx = 1
            self.speedy = 0
        elif self.wnd.key_pressed('A') and self.speedx == 0:
            self.speedx = -1
            self.speedy = 0
        elif self.wnd.key_pressed('S') and self.speedy == 0:
            self.speedy = 1
            self.speedx = 0
        elif self.wnd.key_pressed('W') and self.speedy == 0:
            self.speedy = -1
            self.speedx = 0

run_example(Example, size = (500, 500))
