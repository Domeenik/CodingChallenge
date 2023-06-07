from src.game import Field, Player, PlayerBoid, Game
from src.vectors import Vector2
import src.msg_pb2 as msg
import unittest


class TestField(unittest.TestCase):

    def test___init___(self):
        with self.assertRaises(ValueError):
            Field(0, 1)
        with self.assertRaises(ValueError):
            Field(1, -1)


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.field = Field(10, 10)

    def test___init__(self):
        # check input params
        with self.assertRaises(ValueError):
            player_a = Player(0, self.field, 0)
        with self.assertRaises(TypeError):
            player_a = Player(0, 0, 1)
        # because of random value assignment, the test has to be done multiple times
        for i in range(100):
            player_a = Player(0, self.field, 3)
            # check if speed is correct
            self.assertAlmostEqual(player_a.vel.length(), 3, places=4)
            # check if position is inside of the field
            self.assertTrue(0 <= player_a.pos.x() <= self.field.size_x)
            self.assertTrue(0 <= player_a.pos.y() <= self.field.size_y)

    def test_update(self):
        player_a = Player(0, self.field, 3)
        # check if position is inside of the field and the player is not too fast
        for i in range(100):
            player_a.update()
            self.assertLessEqual(player_a.vel.length(), 3)
            self.assertTrue(0 <= player_a.pos.x() <= self.field.size_x)
            self.assertTrue(0 <= player_a.pos.y() <= self.field.size_y)

    def test_get_protobuf(self):
        # check if the data output of the protobuf message matches the player data
        player_a = Player(0, self.field, 3)
        msg_pos = player_a.get_protobuf()
        self.assertEqual(player_a.id, msg_pos.sensorId)
        self.assertEqual(int(player_a.time_a*1000000.), msg_pos.timestamp_usec)
        self.assertAlmostEqual(player_a.pos.x(), msg_pos.position.x, places=4)
        self.assertAlmostEqual(player_a.pos.y(), msg_pos.position.y, places=4)
        self.assertAlmostEqual(player_a.z, msg_pos.position.z, places=4)


class TestPlayerBoid(unittest.TestCase):

    def setUp(self):
        self.field = Field(10, 10)

    def test___init__(self):
        # check input params
        with self.assertRaises(ValueError):
            player_a = PlayerBoid(0, self.field, 0)
        with self.assertRaises(ValueError):
            player_a = PlayerBoid(0, self.field, 1, sight=0)
        with self.assertRaises(ValueError):
            player_a = PlayerBoid(0, self.field, 1, alignment=0)
        with self.assertRaises(ValueError):
            player_a = PlayerBoid(0, self.field, 1, coherence=0)
        with self.assertRaises(ValueError):
            player_a = PlayerBoid(0, self.field, 1, separation=0)
        with self.assertRaises(TypeError):
            player_a = PlayerBoid(0, 0, 1)
        player_a = PlayerBoid(0, self.field, 3)
        # because of random value assignment, the test has to be done multiple times
        for i in range(100):
            # check if speed is correct
            self.assertAlmostEqual(player_a.vel.length(), 3)
            # check if position is inside of the field
            self.assertTrue(0 <= player_a.pos.x() <= self.field.size_x)
            self.assertTrue(0 <= player_a.pos.y() <= self.field.size_y)

    def test_update(self):
        players = []
        for i in range(10):
            players.append(PlayerBoid(i, self.field, 3))
        # check if position is inside of the field and the player is not too fast
        for i in range(100):
            for p in players:
                p.update(players)
                self.assertAlmostEqual(p.vel.length(), 3)
                self.assertTrue(0 <= p.pos.x() <= self.field.size_x)
                self.assertTrue(0 <= p.pos.y() <= self.field.size_y)

    def test_get_protobuf(self):
        # check if the data output of the protobuf message matches the player data
        player_a = PlayerBoid(0, self.field, 3)
        msg_pos = player_a.get_protobuf()
        self.assertEqual(player_a.id, msg_pos.sensorId)
        self.assertEqual(int(player_a.time_a*1000000.), msg_pos.timestamp_usec)
        self.assertAlmostEqual(player_a.pos.x(), msg_pos.position.x, places=4)
        self.assertAlmostEqual(player_a.pos.y(), msg_pos.position.y, places=4)
        self.assertAlmostEqual(player_a.z, msg_pos.position.z, places=4)

    def test_check_boundaries(self):
        # check if the check_boundaries positions the player inside of the field
        player_a = PlayerBoid(0, self.field, 3)
        player_a.pos = Vector2(-1, -1)
        self.assertFalse(0 <= player_a.pos.x() <= self.field.size_x)
        self.assertFalse(0 <= player_a.pos.y() <= self.field.size_y)
        player_a.check_boundaries()
        self.assertTrue(0 <= player_a.pos.x() <= self.field.size_x)
        self.assertTrue(0 <= player_a.pos.y() <= self.field.size_y)


class TestGame(unittest.TestCase):

    def setUp(self):
        self.field = Field(10, 10)

    def test___init__(self):
        # check if the correct instances are created
        game = Game(5, self.field, boid_behavior=False)
        for i in range(5):
            self.assertTrue(isinstance(game.players[i], Player))
        game = Game(5, self.field, boid_behavior=True)
        for i in range(5):
            self.assertTrue(isinstance(game.players[i], PlayerBoid))
        # check if the params are passed correctly
        max_vel = 5.0
        sight = 2.0
        alignment = 0.003
        coherence = 0.09
        separation = 0.09
        game = Game(5, self.field, boid_behavior=True, max_vel=max_vel, sight=sight,
                    alignment=alignment, coherence=coherence, separation=separation)
        for i in range(5):
            self.assertEqual(game.players[i].max_vel, max_vel)
            self.assertEqual(game.players[i].sight, sight)
            self.assertEqual(game.players[i].alignment, alignment)
            self.assertEqual(game.players[i].coherence, coherence)
            self.assertEqual(game.players[i].separation, separation)

    def test_update(self):
        game = Game(5, self.field, boid_behavior=True)
        # check if players are in the field and are not too fast
        for i in range(100):
            for p in game.players:
                p.update(game.players)
                self.assertAlmostEqual(p.vel.length(), 6, places=4)
                self.assertTrue(0 <= p.pos.x() <= self.field.size_x)
                self.assertTrue(0 <= p.pos.y() <= self.field.size_y)
                
    def test_get_protobuf(self):
        game = Game(5, self.field, boid_behavior=True)
        # check if the data output of the protobuf message matches the player data
        for i in range(100):
            for p in game.players:
                msg_pos = p.get_protobuf()
                self.assertEqual(p.id, msg_pos.sensorId)
                self.assertEqual(int(p.time_a*1000000.), msg_pos.timestamp_usec)
                self.assertAlmostEqual(p.pos.x(), msg_pos.position.x, places=4)
                self.assertAlmostEqual(p.pos.y(), msg_pos.position.y, places=4)
                self.assertAlmostEqual(p.z, msg_pos.position.z, places=4)