import ModernGL
import time, random, os
from math import cos, sin, pi
from miniglm import FloatArray, mat4_ortho, Vec2, mat4_perspective, mat4_look_at, mat4_ortho
from ModernGL.ext.examples import run_example
from ModernGL.ext.obj import Obj

def local(*path):
    return os.path.join(os.path.dirname(__file__), *path)


class Snake:
    """
        Snake class. Contains data regarding the length of the snake.
    """
    def __init__(self):
        """
            Constructor function which sets the length of the snake to 0, then creates the body, adding 3 parts to it,
            so the starter snake has the length of 3.
        """
        self.length = 0
        self.body = []
        self.initLength()
        self.addLength()
        self.addLength()
        self.addLength()

    def initLength(self):
        """
            Function, which adds the first bodypart to the body list. This function is required, because we place the head
            of the snake in the middle of the map at coordinates (25, 25).
        """
        self.length += 1
        self.body.append({
            "pos" : Vec2((25, 25))
        })
    
    def addLength(self):
        """
            Function, which adds a bodypart to the body list and increases the length of the snake.
        """
        self.length += 1
        self.body.append({
            "pos" : Vec2((self.getX(), self.getY()))
        })
    
    def update(self, _x, _y):
        """
            Function, which updates the position of each individual bodypart. Besides the head, each bodypart
            will get the position of the bodypart before it. The heads position is updated by the speeds on the
            oX and oY axes.
        """
        for i in range(self.length - 1, 0, -1):
            self.body[i]['pos'] = self.body[i - 1]['pos']
        self.body[0]['pos'] = Vec2((self.body[0]['pos'].tup[0] + _x, self.body[0]['pos'].tup[1] + _y))
    
    def check(self):
        """
            Function, which checks wether the head of the snake is colliding with any other bodypart.
        """
        for b in self.body[1:]:
            if self.getX() == b['pos'].tup[0] and self.getY() == b['pos'].tup[1]:
                self.reset()
                return True

        return False
    
    def reset(self):
        """
            Function, which resets the state of the snake.
        """
        self.__init__()
    
    def getX(self):
        """
            Function, which returns the X coordinate of the head.
        """
        return int(self.body[0]['pos'].tup[0])
    
    def getY(self):
        """
            Function, which returns the Y coordinate of the head.
        """
        return int(self.body[0]['pos'].tup[1])

class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()
        self.prog = self.ctx.program([
            self.ctx.vertex_shader(
                """
                    #version 330
                    uniform mat4 MVP;
                    uniform vec2 Push;
                    uniform float ID;
                    in vec3 in_verts;
                    out float ID_OUT;
                    void main(){
                        ID_OUT = ID;
                        gl_Position = MVP * vec4(in_verts.x + Push.x, in_verts.y + Push.y, in_verts.z, 1.0);
                        
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
                            color = vec4(0.4, .7 , 0.4, 1.0);
                        }else if(ID_OUT == 3.0){
                            color = vec4(1.0, 0.0, 0.0, 1.0);
                        }else if(ID_OUT == 4.0){
                            color = vec4(0.0, 0.0, 0.0, 1.0);
                        }
                    }
                """
                )
        ])

        self.Push = self.prog.uniforms['Push']
        self.Mvp = self.prog.uniforms['MVP']
        self.size = 50
        self.id = self.prog.uniforms['ID']
        
        sphere = Obj.open(local('data', 'sphere.obj'))

        self.vbo = self.ctx.buffer(sphere.pack('vx vy vz'))
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
        self.paused = False
        
        while self.foodx == 0 or self.foody == 0:
            self.foodx = int(random.random() * 100) % 49
            self.foody = int(random.random() * 100) % 49
        
        
        self.lasttime = wnd.time
    
    def render(self):
        
        self.update()
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(0.9, 0.9, 0.9)
        self.ctx.enable(ModernGL.DEPTH_TEST)
        lookat = mat4_look_at(
            (self.snake.getX() * 2.0, self.snake.getY() * 2.0 + 10, 10),
            (self.snake.getX() * 2.0, self.snake.getY() * 2.0, 0),
            (0, 0, 1)
        )

        proj = mat4_perspective(90.0, 1, 1.0, 1000.0)

        self.Mvp.value = (proj * lookat).tup

        self.id.value = 1.0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[j][i] == 1:
                    self.pushval = (i * 2.0, j * 2.0)
                    self.Push.value = self.pushval
                    self.vao.render(ModernGL.TRIANGLES)

        self.id.value = 2.0
        for b in self.snake.body[1:]:
            self.Push.value = (b['pos'].tup[0] * 2.0, b['pos'].tup[1] * 2.0)
            self.vao.render()

        self.id.value = 3.0
        self.Push.value = (self.foodx * 2.0, self.foody * 2.0)
        self.vao.render()

        self.id.value = 4.0
        self.Push.value = (self.snake.getX() * 2.0, self.snake.getY() * 2.0)
        self.vao.render()

    def update(self):
        if self.wnd.time - self.lasttime > 1 / self.gamespeed and not self.paused:
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

        if self.wnd.key_pressed('A') and self.speedx == 0:
            self.speedx = 1
            self.speedy = 0
        elif self.wnd.key_pressed('D') and self.speedx == 0:
            self.speedx = -1
            self.speedy = 0

        elif self.wnd.key_pressed('S') and self.speedy == 0:
            self.speedy = 1
            self.speedx = 0
        elif self.wnd.key_pressed('W') and self.speedy == 0:
            self.speedy = -1
            self.speedx = 0
        elif self.wnd.key_pressed(' '):
            if self.paused:
                self.paused = False
            else:
                self.paused = True

run_example(Example, size = (500, 500))
