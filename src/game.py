from src.vectors import Vector2
import src.msg_pb2 as msg
import time
import random

class Field():
    def __init__(self, size_x:float, size_y:float):
        self.size_x = size_x
        self.size_y = size_y

class Player():
    def __init__(self, id:int, field:Field, max_vel:float):
        self.id = id
        self.f_max_width = field.size_x
        self.f_max_height = field.size_y
        self.max_vel = max_vel
        self.pos = Vector2(0.,0.)
        self.vel = Vector2(random.random(),random.random())
        self.time_start = time.time()
        self.time_a = time.time()
    
    def update(self, players:list):
        time_b = time.time()
        time_delta = time_b - self.time_a
        self.time_a = time_b
        self.pos += self.vel * time_delta
        
        # check boundaries
        if self.pos.x() <= 0:
            self.pos.set_x(self.f_max_width)
        if self.pos.y() <= 0:
            self.pos.set_y(self.f_max_height)
        if self.pos.x() >= self.f_max_width:
            self.pos.set_x(0)
        if self.pos.y() >= self.f_max_height:
            self.pos.set_y(0)
            
    def get_protobuf(self):
        self.msg_pos = msg.Position()
        self.msg_pos.sensorId = self.id
        self.msg_pos.timestamp_usec = int(self.time_a*1000000.)
        self.msg_pos.position.x = self.pos.x()
        self.msg_pos.position.y = self.pos.y()
        self.msg_pos.position.z = 0
        return self.msg_pos
        
        
class Game():
    def __init__(self, player_count:int, field:Field):
        self.players = []
        self.field = field
        for i in range(player_count):
            p = Player(id=i, field=self.field, max_vel=5)
            self.players.append(p)
            
    def update(self):
        for p in self.players:
            p.update(self.players)
            
    def get_protobuf(self):
        positions = []
        for p in self.players:
            positions.append(p.get_protobuf())
        return positions