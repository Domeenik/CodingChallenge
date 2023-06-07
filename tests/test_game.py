import unittest
from src.game import Field, Player, PlayerBoid, Game

class TestPlayer(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test___init__(self):
        self.player_a = Player(0, 0, 5)