import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Unlock achievement
socket.send_json({'request': 'unlock', 'user_id': 'user1', 'achievement': 'Find the treasure'})
message = socket.recv_json()
print(f'Achievement Unlocked: {message}')

# Get achievements
socket.send_json({'request': 'get_achievements', 'user_id': 'user1'})
message = socket.recv_json()
print(f'Received reply: {message}')

# Shut down server
socket.send_json({'request': 'Q'})
message = socket.recv_json()
print(f'Received reply: {message}')
