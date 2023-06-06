from src.config_handler import ConfigHandler
import src.msg_pb2 as msg
import numpy as np
import cv2
import zmq

CONFIG_FILE = "./settings.json"

# load config
print(f"[INFO] Load settings from config file '{CONFIG_FILE}'")
config = ConfigHandler(CONFIG_FILE)
c_zmq_port = config.get("zmq", "port")
c_width = config.get("visualization", "width")
c_height = config.get("visualization", "height")
c_visual_point_size = config.get("visualization", "point_size")
c_visual_color = config.get("visualization", "color")
c_field_width = config.get("field", "width")
c_field_height = config.get("field", "height")

# create zmq server
print(f"[INFO] Start server on '*:{c_zmq_port}")
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind(f"tcp://*:{c_zmq_port}")

recv_pos = msg.Position()

# create opencv environment
img = np.zeros((c_height, c_width, 3), dtype = np.uint8)
scale_x = c_width / c_field_width
scale_y = c_height / c_field_height

# dict for storing the player positions
player_pos = {}

counter = 0
while True:
    counter += 1
    # get messages and store the player positions in the dict
    message = socket.recv()
    recv_pos.ParseFromString(message)
    player_pos[recv_pos.sensorId] = [recv_pos.position.x, recv_pos.position.y]
    
    # draw a dot for each player
    img = np.zeros((c_height, c_width, 3), dtype = np.uint8)
    for id in player_pos:
        x = player_pos[id][0] * scale_x
        y = player_pos[id][1] * scale_y
        img = cv2.circle(img, (int(x), int(y)), 1, c_visual_color, c_visual_point_size)
    # show the created image
    if counter%10 == 0:
        cv2.imshow('Game visualization', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # socket.send(b"stop")
        break
    # else:
        #  Send reply back to client
        # socket.send(b"success")