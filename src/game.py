from src.vectors import Vector2
import src.msg_pb2 as msg
import time
import random


class Field():
    def __init__(self, size_x: float, size_y: float):
        if size_x > 0 and size_y > 0:
            self.size_x = size_x
            self.size_y = size_y
        else:
            raise ValueError(
                "dimensions in each direction must be higher than zero")


class Player():
    def __init__(self, id: int, field: Field, max_vel: float = 6.0):
        self.id = id
        self.time_a = time.time()

        # check input parameters
        if isinstance(field, Field):
            self.f_max_width = field.size_x
            self.f_max_height = field.size_y
        else:
            raise TypeError("arg 'field' must be of type 'Field'")
        if max_vel > 0:
            self.max_vel = max_vel
        else:
            raise ValueError("maximum velocity must be higher than 0")

        # assign random values for speed and position for the players
        self.pos = Vector2(random.randint(0, self.f_max_width)
                           * 1.0, random.randint(0, self.f_max_height)*1.0)
        self.z = random.randint(15, 17) / 10.0
        self.vel = Vector2((random.random()-0.5)*max_vel,
                           (random.random()-0.5)*max_vel)

        # cap speed to maximal velocity
        self.vel = self.vel.norm() * self.max_vel * 0.99

    def update(self, *args):
        time_b = time.time()
        time_delta = time_b - self.time_a
        self.time_a = time_b

        # add velocity vetor time dependend to position
        self.pos += (self.vel * time_delta)

        # check boundaries
        if self.pos.x() <= 0:
            self.vel = Vector2(-self.vel.x(), self.vel.y())
            self.pos.set_x(0.1)
        if self.pos.y() <= 0:
            self.vel = Vector2(self.vel.x(), -self.vel.y())
            self.pos.set_y(0.1)
        if self.pos.x() >= self.f_max_width:
            self.vel = Vector2(-self.vel.x(), self.vel.y())
            self.pos.set_x(self.f_max_width - 0.1)
        if self.pos.y() >= self.f_max_height:
            self.vel = Vector2(self.vel.x(), -self.vel.y())
            self.pos.set_y(self.f_max_height - 0.1)

        # cap speed to little less than maximal velocity
        self.vel = self.vel.norm() * self.max_vel * 0.9999

        # set height of sensor at around 1.5-1.8m in case of jumps and movement
        self.z = random.randint(15, 18) / 10.0

    def get_protobuf(self):
        # transfer all the information into the protobuf format
        self.msg_pos = msg.Position()
        self.msg_pos.sensorId = self.id
        self.msg_pos.timestamp_usec = int(self.time_a*1000000.)
        self.msg_pos.position.x = round(self.pos.x(), 4)
        self.msg_pos.position.y = round(self.pos.y(), 4)
        self.msg_pos.position.z = round(self.z, 4)
        return self.msg_pos


class PlayerBoid(Player):
    # A derivation of the standard player class with boid behavior according to the paper:
    # http://www.cs.toronto.edu/~dt/siggraph97-course/cwr87/

    def __init__(self, id: int, field: Field, max_vel: float = 6.0, sight: float = 3.0, alignment: float = 0.002, coherence: float = 0.1, separation: float = 0.1):
        Player.__init__(self, id, field, max_vel)
        if sight > 0 and alignment > 0 and coherence > 0 and separation > 0:
            self.sight = sight
            self.alignment = alignment
            self.coherence = coherence
            self.separation = separation
        else:
            raise ValueError("the values for 'sight', 'alignment', 'coherence' and 'separation' must be greater than zero")
        self.check_boundaries()

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

    def check_boundaries(self):
        # check if the player is inside of the field
        if self.pos.x() <= 0:
            self.pos.set_x(0.1)
        if self.pos.x() >= self.f_max_width:
            self.pos.set_x(self.f_max_width - 0.1)
        if self.pos.y() <= 0:
            self.pos.set_y(0.1)
        if self.pos.y() >= self.f_max_height:
            self.pos.set_y(self.f_max_height - 0.1)

    def update(self, players: list):
        # get current position for speed check at the end of the update
        pos_old = Vector2(self.pos.x(), self.pos.y())

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
        self.vel += self.find_move_direction(relevant_players) * self.alignment
        # coherence
        self.vel += (self.find_center(relevant_players) -
                     self.pos) * self.coherence
        # seperation
        for p in relevant_players:
            distance = self.pos.distance_to(p.pos)
            if distance > 0:
                self.vel -= (p.pos - self.pos) * \
                    (1 / distance) * self.separation

        # avoid the outer walls
        avoid_walls = 0.09
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

        # amplify horizontal movement
        self.vel *= Vector2(1.001, 0.999)

        # cap speed to maximal velocity
        self.vel = self.vel.norm() * self.max_vel

        # add speed vector to position in dependence of time
        self.pos += (self.vel * time_delta * (random.randint(5, 10)/10.0))

        # set height of sensor at around 1.5-1.8m in case of jumps and movement
        self.z = random.randint(15, 18) / 10.0

        # check if the player is inside of the field
        self.check_boundaries()

        # print warning if player is outside of boundaries
        if not 0 < self.pos.x() < self.f_max_width or not 0 < self.pos.y() < self.f_max_height:
            print(
                f"[WARN] Player {self.id} out of field with coordinates: {self.pos}")

        # check for speed cap after correction with a 1 percent tolerance
        if self.pos.distance_to(pos_old) > time_delta * self.max_vel * 1.01:
            # print(self.pos.distance_to(pos_old), time_delta * self.max_vel)
            print(
                f"[WARN] Player {self.id} moved {round((time_delta * self.max_vel)/(self.pos.distance_to(pos_old)), 2)*100}% faster than the maximum speed set in the config")


class Game():
    def __init__(self, player_count: int, field: Field, boid_behavior: bool = True, max_vel: float = 6.0, sight: float = 3.0, alignment: float = 0.002, coherence: float = 0.1, separation: float = 0.1):
        self.field = field
        # create player list
        self.players = []
        for i in range(player_count):
            # use plain player or boid player instance dependend on boid_behavior flag
            if boid_behavior:
                p = PlayerBoid(id=i, field=self.field, max_vel=max_vel, sight=sight,
                               alignment=alignment, coherence=coherence, separation=separation)
            else:
                p = Player(id=i, field=field, max_vel=max_vel)
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
