from __future__ import annotations

import json
import time
from datetime import datetime, timezone

import numpy as np
import zmq

"""
Simple ZeroMQ PUB server streaming synthetic EURUSD ticks.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""


def run_tick_server(bind_addr: str="tcp://127.0.0.1:5555",
                    symbol: str="EURUSD",
                    start_price: float=1.10,
                    dt: float=0.1,
                    sigma: float=0.0005) -> None:
    """Publish synthetic EURUSD ticks as JSON messages on a PUB socket."""
    ctx = zmq.Context.instance()
    socket = ctx.socket(zmq.PUB)
    socket.bind(bind_addr)

    price = start_price  #  initial level of the random walk
    rng = np.random.default_rng(seed=42)

    try:
        while True:
            shock = rng.normal(0.0, sigma)  #  small random move
            price = max(0.1, price + shock)  #  keep price positive
            payload = {
                "time": datetime.now(timezone.utc).isoformat(),
                "symbol": symbol,
                "price": float(price),
            }
            socket.send_json(payload)
            time.sleep(dt)
    except KeyboardInterrupt:
        pass
    finally:
        socket.close(0)
        ctx.term()


if __name__ == "__main__":
    run_tick_server()
