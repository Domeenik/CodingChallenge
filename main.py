from src.config_handler import ConfigHandler
from src.game import Field, Game
import src.msg_pb2 as msg
import zmq
import time

CONFIG_FILE = "./settings.json"

# load config
print(f"[INFO] Load settings from config file '{CONFIG_FILE}'")
config = ConfigHandler(CONFIG_FILE)
c_zmq_addr = config.get("zmq", "address")
c_zmq_port = config.get("zmq", "port")
c_freq = config.get("game", "updates_per_second")
c_player_count = config.get("game", "player_count")
c_field_width = config.get("field", "width")
c_field_height = config.get("field", "height")
c_max_exc_time = config.get("quality_control", "max_excessive_time_percent")

# some info about the config
print(f"[CONF] Sending frequency is {(1./c_freq)} Hz")
print(f"[CONF] There are {c_player_count} players")
print(f"[CONF] Field dimensions are {c_field_width} m x {c_field_height} m")

# setup ZeroMQ-connection
print(f"[INFO] Connect to server 'tcp://{c_zmq_addr}:{c_zmq_port}'")
context = zmq.Context()
socket = context.socket(zmq.PAIR)
# ToDo: add timeout
socket.connect(f"tcp://{c_zmq_addr}:{c_zmq_port}")

# ToDo: add handshake

# setup game
print("[INFO] Create game instance")
field = Field(size_x=c_field_width, size_y=c_field_height)
game = Game(player_count=c_player_count, field=field)

# main
print("[INFO] Start with the main loop")
time_a = time.time()
while True:
    # update the players
    game.update()

    # check if it is time for sending the data to the server
    time_b = time.time()
    if time_b >= time_a + (1./c_freq):
        # get excessive time after intervall for quality control
        excessive_time = ((time_b - time_a) - (1./c_freq))
        if (excessive_time / (1./c_freq)) > c_max_exc_time:
            print(f"[WARN] The overrun time above the set point is too long by {round((excessive_time / (1./c_freq)), 5)}%")
            print("[WARN] The simulation will NOT run in real time")
        time_a = time_b
            
        # send player data to the server
        msg_list = game.get_protobuf()
        for msg in msg_list:
            socket.send(msg.SerializeToString())
