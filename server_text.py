import src.msg_pb2 as msg
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

recv_pos = msg.Position()

while True:
    message = socket.recv()
    recv_pos.ParseFromString(message)
    print("[INFO] received: {}".format(recv_pos))
    
    #  Send reply back to client
    socket.send(b"World")