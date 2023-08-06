#!/usr/bin/env python3
import logging

import serial
import socketio
import uvicorn
from hardware.robot_brain import augment, check

sio = socketio.AsyncServer(async_mode='asgi')


@sio.event
def write(sid, line) -> None:
    serial.write(f'{augment(line)}\n'.encode())


async def receive() -> None:
    global buffer
    try:
        while not stop_requested:
            try:
                buffer += serial.read_all().decode()
                await sio.sleep(0)
            except UnicodeDecodeError as e:
                logging.exception('could not decode', exc_info=e)
            if '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                await sio.emit('read', check(line.rstrip('\r')))
    except Exception:
        logging.exception('could not read')


if __name__ == '__main__':
    serial = serial.Serial('/dev/ttyTHS1', 115200)
    buffer = ''
    app = socketio.ASGIApp(sio, on_startup=lambda: sio.start_background_task(receive))
    stop_requested = False
    try:
        uvicorn.run(app, host='0.0.0.0', port=8081)
    except KeyboardInterrupt:
        stop_requested = True
