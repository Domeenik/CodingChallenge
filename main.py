from src.config_handler import ConfigHandler
import src.msg_pb2 as msg
import zmq
import time

my_pos = msg.Position()

my_pos.sensorId = 0
my_pos.timestamp_usec = 10000
my_pos.position.x = 10
my_pos.position.y = 12
my_pos.position.z = 13

# load config
config = ConfigHandler("./settings.json")
c_zmq_addr = config.get("zmq", "address")
c_zmq_port = config.get("zmq", "port")
c_zmq_epoc_time = config.get("zmq", "epoch_time")

# setup ZeroMQ-connection
context = zmq.Context()
print(f"[INFO] connect to server 'tcp://{c_zmq_addr}:{c_zmq_port}'")
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://{c_zmq_addr}:{c_zmq_port}")


# main
time_start = time.time()
time_a = time_start
while True:
    time_b = time.time()
    if (time_b >= time_a + 1):
        time_a = time_b
        
        # get timestamp
        if c_zmq_epoc_time:
            my_pos.timestamp_usec = int(time_a*1000000.)
        else:
            my_pos.timestamp_usec = int((time_a-time_start)*1000000.)

        socket.send(my_pos.SerializeToString())
        message = socket.recv()