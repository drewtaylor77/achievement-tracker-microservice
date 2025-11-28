# Achievement Tracker

A Python-based microservice capable of receiving requests to unlock and retrieve achievements through TCP connections set up via ZeroMQ after a user completes a request action.

### How It Works

The microservice runs as a server using ZeroMQ REP socket.

   * It listens for incoming value requests via a TCP server connection.
   * It stores unlocked achievements for each user.
   * It can return all achievements completed by a user.

### Request formats
All requests must be in valid JSON format.

| Request  | Return/Action                      |
|----------|------------------------------------|
| `{'request': 'Q'}` | Break communication and shut down the server |
| `{'request': 'unlock', 'user_id': 'user1', 'achievement': 'Find the treasure'}` | Unlocks and stores achievement for user. Returns confirmation JSON message. |
| `{'request': 'get_achievements', 'user_id': 'user1'}` | Returns all achievements for user in JSON message |

### Making a Request

1. Establish a ZeroMQ context object
2. Create a socket w/ the context & establish connection on the host and port with 'socket = context.socket(zmq.REQ)'
   * connection is currently set to target "tcp://localhost:5555"
3. Create a valid JSON object in a format listed in the table above.
4. Send the string quote via 'socket.send_json()'

#### Example Request
```python
import zmq

context = zmq.Context()

print("Connecting to server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:55555")

# Unlock achievement
socket.send_json({'request': 'unlock', 'user_id': 'user1', 'achievement': 'Find the treasure'})

# Get achievements
socket.send_json({'request': 'get_achievements', 'user_id': 'user1'})
```

### Receiving a Response

After having received the request, assign a variable equal to 'socket.recv()'; it will generate a quote and send it back to the client.

#### Example of Receiving
```python
# Unlock achievement
message = socket.recv_json()
print(f'Achievement Unlocked: {message}')

# Get achievements
message = socket.recv_json()
print(f'Completed achievements: {message}')
```

The response is formatted as follows:

```python
# Unlock achievement
{'Status': 'Success', 'Achievement Unlocked': achievement}

# Get achievements
{'Achievements': achievements}

# Errors
{'Error': 'Missing user_id or achievement'}
```

## Tech Stack

Python 3.13

ZeroMQ (pyzmq) — Microservice communication

### Author

Andrew Taylor
