from src.config_handler import ConfigHandler
from src.game import Field, Game
from src.vectors import Vector2
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
c_player_boid_behavior = config.get("player", "boid_behavior")
c_player_max_speed = config.get("player", "max_speed")
c_player_sight = config.get("player", "sight")
c_player_alignment = config.get("player", "alignment")
c_player_coherence = config.get("player", "coherence")
c_player_separation = config.get("player", "separation")
c_runtime_testing = config.get("quality_control", "enable_runtime_testing")
c_max_exc_time = config.get("quality_control", "max_excessive_time_percent")

# some info about the config
print(f"[CONF] Sending frequency is {(1./c_freq)} Hz")
print(f"[CONF] There are {c_player_count} players")
print(f"[CONF] Field dimensions are {c_field_width} m x {c_field_height} m")
print(f"[CONF] Runtime testing is {'enabled' if c_runtime_testing else 'disabled'}")

# setup ZeroMQ-connection
print(f"[INFO] Connect to server 'tcp://{c_zmq_addr}:{c_zmq_port}'")
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect(f"tcp://{c_zmq_addr}:{c_zmq_port}")

# setup game instance
print("[INFO] Create game instance")
field = Field(size_x=c_field_width, size_y=c_field_height)
game = Game(player_count=c_player_count, field=field, boid_behavior=c_player_boid_behavior, max_vel=c_player_max_speed,
            sight=c_player_sight, alignment=c_player_alignment, coherence=c_player_coherence, separation=c_player_separation)

# runtime testing
players = {}
def runtime_testing(last_message: msg.Position, current_message: msg.Position):
    # check if the required frequency is matched
    time_deviation = abs(current_message.timestamp_usec - last_message.timestamp_usec - 1000000)
    if time_deviation > 1000000 * c_max_exc_time:
        print(f"[WARN] Time deviation is with {time_deviation} microseconds larger than the required {c_max_exc_time*100.0}%")
    
    # check if player is inside the boundaries
    if not 0 <= current_message.position.x <= c_field_width or not 0 <= current_message.position.y <= c_field_height:
        print(f"[WARN] Player {current_message.sensorId} is not inside of the field")
    
    # check if the players velocity is below the set maximum
    pos_last = Vector2(last_message.position.x, last_message.position.y)
    pos_current = Vector2(current_message.position.x, current_message.position.y)
    player_speed = pos_last.distance_to(pos_current) / ((current_message.timestamp_usec - last_message.timestamp_usec)/ 1000000.0)
    if player_speed > c_player_max_speed:
        print(f"[WARN] Player {current_message.sensorId} is too fast with a speed of {round(player_speed, 4)} m/s")
    
# fill runtime test dict
if c_runtime_testing:
    game.update()
    msg_list = game.get_protobuf()
    for msg in msg_list:
        players[msg.sensorId] = msg

# main loop
time_a = time.time()
print("[INFO] Start with the main loop")
while True:
    # update the players
    game.update()

    # check if it is time for sending the data to the server
    time_b = time.time()
    if time_b >= time_a + (1./c_freq):
        time_a = time_b

        # send player data to the server
        msg_list = game.get_protobuf()
        for msg in msg_list:
            if c_runtime_testing:
                runtime_testing(players[msg.sensorId], msg)
            socket.send(msg.SerializeToString())
            players[msg.sensorId] = msg
