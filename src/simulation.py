from vectors import Vector2
import random

class Field():
    def __init__(self, size_x:float, size_y:float):
        self.size_x = size_x
        self.size_y = size_y

class Player():
    def __init__(self, field:Field, max_vel:float):
        self.f_max_x = field.size_x
        self.f_max_y = field.size_y
        self.max_vel = max_vel
        self.pos = Vector2(random.random()*self.f_max_x,random.random()*self.f_max_y)
        #ToDo: switch to length = max_vel
        self.vel = Vector2(random.random()*max_vel,random.random()*max_vel)
    
    def update(self):
        self.pos += self.vel
        
        # check boundaries
        if self.pos.x() <= 0:
            self.pos.set_x(self.f_max_x)
        if self.pos.y() <= 0:
            self.pos.set_y(self.f_max_y)
        if self.pos.x() >= self.f_max_x:
            self.pos.set_x(0)
        if self.pos.y() >= self.f_max_y:
            self.pos.set_y(0)
            
if __name__ == "__main__":
    sensors = []
    
    field = Field(10, 30)
    
    for i in range(10):
        p = Player(field=field, max_vel=5)
        sensors.append(p)
    
    for i in range(100):
        print()
        for p in sensors:
            p.update()
            print(p.pos)