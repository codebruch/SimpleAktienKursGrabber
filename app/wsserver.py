import asyncio
from websockets import broadcast
from websockets.server import serve
import logging
import time

async def echo(websocket):
    async for message in websocket:
        #logging.debug('echo message ' + str(message))
        #await broadcast(message)
        await websocket.send(message)
        #await broadcast(message)


async def broadcast_messages():
    while True:
        await asyncio.sleep(1)
        
        

async def handler(websocket):
     async for message in websocket:
        logging.debug('echo message ' + str(message))

# async def main():
#     async with serve(handler, "0.0.0.0", 8765):
#         await broadcast_messages()  # runs forever

async def main():
    async with serve(echo, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename='wsserver.log',format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)
    asyncio.run(main())