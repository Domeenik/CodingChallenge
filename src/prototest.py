import msg_pb2 as msg

my_pos = msg.Position()
my_pos.sensorId = 0
my_pos.timestamp_usec = 10000
my_pos.position.x = 10
my_pos.position.y = 10
my_pos.position.z = 10

print(my_pos)

serialized = my_pos.SerializeToString()

new_pos = msg.Position()
new_pos.ParseFromString(serialized)
print(new_pos)