#
# Tick Data Collector
#
import zmq
import pandas as pd
import datetime

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://127.0.0.1:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, '')

ticks = pd.DataFrame()
i = 0
while True:
    i += 1
    msg = socket.recv_pyobj()
    t = datetime.datetime.now()
    ticks = pd.concat((ticks,
            pd.DataFrame(msg, index=[t])),
            )
    bars = ticks.resample(
            '5s', label='right'
            ).last()
    print(msg)
    if i % 10 == 0:
        ticks.to_csv('ticks.csv')
