import zmq

# Establish server connection
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://localhost:5555")

# Store achievements
user_achievements = {}

# Loop to receive requests
while True:
    try:
        message = socket.recv_json()

        # Error: Empty message
        if not message:
            reply = {'Error': 'Request must include achievement and username'}

        # Shut down server
        elif message.get('request') == 'Q':
            reply = {'Status': 'Shutting down'}
            socket.send_json(reply)
            break

        # Unlock achievement
        elif message.get('request') == 'unlock':
            user_id = message.get('user_id')
            achievement = message.get('achievement')

            if user_id and achievement:
                user_achievements.setdefault(user_id, set()).add(achievement)
                reply = {'Status': 'Success', 'Achievement Unlocked': achievement}
            else:
                reply = {'Error': 'Missing user_id or achievement'}

        # Retrieve achievements
        elif message.get('request') == 'get_achievements':
            user_id = message.get('user_id')
            if user_id:
                achievements = list(user_achievements.get(user_id, []))
                reply = {'Achievements': achievements}
            else:
                reply = {'Error': 'Missing user_id'}

        else:
            reply = {'Error': 'Unknown request'}

    except Exception as e:
        reply = {'Error': str(e)}

    socket.send_json(reply)
