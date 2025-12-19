#
# Simple Tick Data Server
#
import zmq
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://127.0.0.1:5555')

price = 1.15  # arbitrary starting value

while True:
    price += random.gauss(0, 0.01)  # random update of value
    message = {
            'SYMBOL': 'EURUSD',
            'PRICE': round(price, 5)
            }
    socket.send_pyobj(message)
    print(message)
    time.sleep(random.random() * 2)
