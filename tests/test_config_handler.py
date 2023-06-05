import unittest
import os
from src.config_handler import ConfigHandler

class TestConfigHandler(unittest.TestCase):
    
    def setUp(self):
        json_dump = {"category": {"value1": "string1", "value2": 3}, "single": "string2"}
        f = open("./tests/configtest.json", "w")
        f.write(str(json_dump).replace("'", '"'))
        f.close()
        self.config = ConfigHandler("./tests/configtest.json")
    
    def tearDown(self):
        del self.config
        os.remove("./tests/configtest.json")
    
    def test__init__(self):
        self.tearDown()
        with self.assertRaises(FileNotFoundError):
            self.config = ConfigHandler("./tests/configtest.json")
            
        f = open("./tests/configtest.json", "w")
        f.close()
        with self.assertRaises(SyntaxError):
            self.config = ConfigHandler("./tests/configtest.json")
        
        f = open("./tests/configtest.json", "w")
        f.write("{}")
        f.close()
        self.config = ConfigHandler("./tests/configtest.json")
        
    def test_get(self):
        self.assertEqual(self.config.get("single"), "string2")
        self.assertEqual(self.config.get("category", "value1"), "string1")
        self.assertEqual(self.config.get("category", "value2"), 3)
        with self.assertRaises(KeyError):
            self.config.get("category", "value3")
    
    def test_set(self):
        self.config.set("single2", "string3")
        self.assertEqual(self.config.get("single2"), "string3")
        
    def test_save(self):
        self.config.set("single2", "string3")
        del self.config
        self.config = ConfigHandler("./tests/configtest.json")
        self.assertEqual(self.config.get("single2"), "string3")
        