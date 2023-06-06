from src.vectors import Vector2
import src.msg_pb2 as msg
import time
import random


class Field():
    def __init__(self, size_x: float, size_y: float):
        self.size_x = size_x
        self.size_y = size_y


class Player():
    def __init__(self, id: int, field: Field, max_vel: float):
        self.id = id
        self.f_max_width = field.size_x
        self.f_max_height = field.size_y
        self.max_vel = max_vel
        self.time_a = time.time()
        # assign random values for speed and position for the players
        self.pos = Vector2(random.randint(0, self.f_max_width)
                           * 1.0, random.randint(0, self.f_max_height)*1.0)
        self.vel = Vector2((random.random()-0.5)*max_vel,
                           (random.random()-0.5)*max_vel)
        # cap speed to maximal velocity
        self.vel = self.vel.norm() * self.max_vel

    def update(self, players: list):
        time_b = time.time()
        time_delta = time_b - self.time_a
        self.time_a = time_b
        self.pos += (self.vel * time_delta)

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
        # transfer all the information into the protobuf format
        self.msg_pos = msg.Position()
        self.msg_pos.sensorId = self.id
        self.msg_pos.timestamp_usec = int(self.time_a*1000000.)
        self.msg_pos.position.x = self.pos.x()
        self.msg_pos.position.y = self.pos.y()
        self.msg_pos.position.z = 0
        return self.msg_pos


class PlayerBoid(Player):
    def __init__(self, id: int, field: Field, max_vel: float, sight: float):
        Player.__init__(self, id, field, max_vel)
        self.sight = sight

    @staticmethod
    def find_center(players):
        # get the center of positions of the given player list
        center = Vector2(0., 0.)
        for p in players:
            center += p.pos
        return center / len(players)

    @staticmethod
    def find_move_direction(players):
        # get the average velocity vector of the given player list
        velocity = Vector2(0., 0.)
        for p in players:
            velocity += p.vel
        return velocity / len(players)

    def update(self, players: list):
        # get time delta for speed calculation
        time_b = time.time()
        time_delta = time_b - self.time_a
        self.time_a = time_b

        # get closest players
        relevant_players = []
        for p in players:
            distance = self.pos.distance_to(p.pos)
            if distance < self.sight:
                relevant_players.append(p)

        # alignment
        self.vel += self.find_move_direction(relevant_players) * 0.002
        # coherence
        self.vel += (self.find_center(relevant_players) - self.pos) * 0.1
        # seperation
        for p in relevant_players:
            distance = self.pos.distance_to(p.pos)
            if distance > 0:
                self.vel -= (p.pos - self.pos) * (1 / distance) * 0.1

        # avoid the outer walls
        avoid_walls = 0.03
        if self.pos.x() <= self.sight:
            self.vel += Vector2((1 / (self.pos.x() + 0.01)) * avoid_walls, 0)
        if self.pos.x() >= self.f_max_width - self.sight:
            self.vel -= Vector2((1 / (self.f_max_width -
                                self.pos.x() - 0.01)) * avoid_walls, 0)
        if self.pos.y() <= self.sight:
            self.vel += Vector2(0, (1 / (self.pos.y() + 0.01)) * avoid_walls)
        if self.pos.y() >= self.f_max_height - self.sight:
            self.vel -= Vector2(0, (1 / (self.f_max_height -
                                self.pos.y() - 0.01)) * avoid_walls)

        # check if all players are inside of the field
        if self.pos.x() <= 0:
            self.pos.set_x(0.1)
        if self.pos.x() >= self.f_max_width:
            self.pos.set_x(self.f_max_width - 0.1)
        if self.pos.y() <= 0:
            self.pos.set_y(0.1)
        if self.pos.y() >= self.f_max_height:
            self.pos.set_y(self.f_max_height - 0.1)

        # amplify horizontal movement
        self.vel *= Vector2(1.001, 0.999)

        # cap speed to maximal velocity
        self.vel = self.vel.norm() * self.max_vel

        # add speed vector to position in dependence of time
        self.pos += (self.vel * time_delta * (random.randint(5,10)/10.0))


class Game():
    def __init__(self, player_count: int, field: Field):
        self.field = field
        # create player list
        self.players = []
        for i in range(player_count):
            p = PlayerBoid(id=i, field=self.field, max_vel=7., sight=3.0)
            self.players.append(p)

    def update(self):
        # update each player
        for p in self.players:
            p.update(self.players)

    def get_protobuf(self):
        # return data of players in profobuf format as a list
        positions = []
        for p in self.players:
            positions.append(p.get_protobuf())
        return positions
