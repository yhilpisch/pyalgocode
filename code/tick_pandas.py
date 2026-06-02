from __future__ import annotations

import zmq
import pandas as pd

"""
ZeroMQ SUB client receiving and storing EURUSD ticks.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""


def run_tick_client(connect_addr: str="tcp://127.0.0.1:5555") -> None:
    """Subscribe to all tick messages and print them."""
    ctx = zmq.Context.instance()
    socket = ctx.socket(zmq.SUB)
    socket.connect(connect_addr)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # receive all symbols
    ticks = pd.DataFrame()

    try:
        while True:
            tick = socket.recv_json()
            time_str = tick["time"]
            symbol = tick["symbol"]
            price = tick["price"]
            df = pd.DataFrame({'symbol': symbol, 'price': float(price)},
                              index=[pd.Timestamp(time_str)])
            ticks = pd.concat((ticks, df))
            print("COLLECTED:", tick)
    except KeyboardInterrupt:
        ticks.to_csv('ticks.csv')
    finally:
        socket.close(0)
        ctx.term()


if __name__ == "__main__":
    run_tick_client()
