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
c_zmq_epoc_time = config.get("zmq", "epoch_time")
c_freq = config.get("game", "updates_per_second")
c_player_count = config.get("game", "player_count")
c_field_width = config.get("field", "width")
c_field_height = config.get("field", "height")

# some info about the config
print(f"[CONF] Sending frequency is {(1./c_freq)} Hz")
print(f"[CONF] There are {c_player_count} players")
print(f"[CONF] Field dimensions are {c_field_width} m x {c_field_height} m")

# setup ZeroMQ-connection
print(f"[INFO] Connect to server 'tcp://{c_zmq_addr}:{c_zmq_port}'")
context = zmq.Context()
socket = context.socket(zmq.REQ)
#ToDo: add timeout
socket.connect(f"tcp://{c_zmq_addr}:{c_zmq_port}")

# setup game
print("[INFO] Create game instance")
field = Field(size_x=c_field_width, size_y=c_field_height)
game = Game(player_count=c_player_count, field=field)


# main
print("[INFO] Start with the main loop")
time_a = time.time()
while True:
    game.update()
    print("update")
    
    time_b = time.time()
    if time_b >= time_a + (1./c_freq):
        time_a = time_b
        msg_list = game.get_protobuf()
        print("send")

        for msg in msg_list:
            socket.send(msg.SerializeToString())
            
            # wait for answer and check if data was successfully received
            message = socket.recv()
            message = message.decode('utf-8')
            if not message == "success":
                if message == "stop":
                    print("[INFO] The server send the command to stop sending")
                    quit()
                else:
                    print(f"[WARN] Unexpected answer: '{message}'")