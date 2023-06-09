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
c_visual_player_color = config.get("visualization", "player_color")
c_visual_background_color = config.get("visualization", "background_color")
c_field_width = config.get("field", "width")
c_field_height = config.get("field", "height")

# create zmq server
print(f"[INFO] Start server on '*:{c_zmq_port}")
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind(f"tcp://*:{c_zmq_port}")

# create opencv image and get scale factors
img = np.zeros((c_height, c_width, 3), dtype = np.uint8)
img[:] = tuple(c_visual_background_color)
scale_x = c_width / c_field_width
scale_y = c_height / c_field_height

# dict for storing the player positions
player_pos = {}

# main loop
recv_pos = msg.Position()
while True:
    # get messages and store the player positions in the dict
    message = socket.recv()
    recv_pos.ParseFromString(message)
    player_pos[recv_pos.sensorId] = [recv_pos.position.x, recv_pos.position.y]
    
    # reset image
    img = np.zeros((c_height, c_width, 3), dtype = np.uint8)
    img[:] = tuple(c_visual_background_color)
    
    # draw a dot for each player
    for id in player_pos:
        x = player_pos[id][0] * scale_x
        y = player_pos[id][1] * scale_y
        img = cv2.circle(img, (int(x), int(y)), 1, c_visual_player_color, c_visual_point_size)
        
    # show image and check for exit via the key 'q'
    cv2.imshow('Game visualization', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break