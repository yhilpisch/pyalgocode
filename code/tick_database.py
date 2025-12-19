from __future__ import annotations

import sqlite3

import zmq

"""
ZeroMQ SUB client persisting EURUSD ticks into a SQLite database.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""


def init_db(path: str="ticks.db") -> sqlite3.Connection:
    """Create (or open) a SQLite database for storing ticks."""
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ticks (
            time TEXT NOT NULL,
            symbol TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def run_tick_database(connect_addr: str="tcp://127.0.0.1:5555",
                      db_path: str="ticks.db") -> None:
    """Subscribe to ticks and write them to SQLite."""
    conn = init_db(db_path)
    cur = conn.cursor()

    ctx = zmq.Context.instance()
    socket = ctx.socket(zmq.SUB)
    socket.connect(connect_addr)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  #  receive all symbols

    try:
        while True:
            tick = socket.recv_json()
            cur.execute(
                "INSERT INTO ticks (time, symbol, price) VALUES (?, ?, ?)",
                (tick["time"], tick["symbol"], float(tick["price"])),
            )
            conn.commit()
    except KeyboardInterrupt:
        pass
    finally:
        socket.close(0)
        conn.close()
        ctx.term()


if __name__ == "__main__":
    run_tick_database()
