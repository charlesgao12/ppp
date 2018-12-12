#!/usr/bin/python

from websocket import create_connection
ws = create_connection("ws://localhost:9001")
print("Sending 'Hello, World'...")
ws.send("Hello, World")

result =  ws.recv()
print("Received '%s'" % result)
ws.close()