from src.config_handler import ConfigHandler
import zmq

# load config
config = ConfigHandler("./settings.json")
c_zmq_addr = config.get("zmq", "address")
c_zmq_port = config.get("zmq", "port")

context = zmq.Context()

print(f"[INFO] connect to server 'tcp://{c_zmq_addr}:{c_zmq_port}'")
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://{c_zmq_addr}:{c_zmq_port}")

print("[INFO] send simple message")
socket.send(b"Hello")