import zmq

context = zmq.Context()

print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for request in range(10):
    print("Sending request {}".format(request))
    socket.send(b"Hello")
    
    message = socket.recv()
    print("Received reply {} [ {} ]".format(request, message))