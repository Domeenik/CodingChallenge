from src.config_handler import ConfigHandler
import src.msg_pb2 as msg
import zmq

CONFIG_FILE = "./settings.json"

# load config
print(f"[INFO] Load settings from config file '{CONFIG_FILE}'")
config = ConfigHandler(CONFIG_FILE)
c_zmq_port = config.get("zmq", "port")

# create zmq server
print(f"[INFO] Start server on '*:{c_zmq_port}")
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind(f"tcp://*:{c_zmq_port}")

# main loop
recv_pos = msg.Position()
while True:
    message = socket.recv()
    recv_pos.ParseFromString(message)
    print("[INFO] received: {}".format(recv_pos))