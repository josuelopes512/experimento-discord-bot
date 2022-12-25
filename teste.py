import websockets
import threading
import asyncio


def websocket_thread():
    # código do websocket
    async def hello(websocket, path):
        name = await websocket.recv()
        print(f"< {name}")

        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f"> {greeting}")

    start_server = websockets.serve(hello, "localhost", 8765)

    asyncio.get_event_loop().call_soon_threadsafe(asyncio.ensure_future, start_server())
    # asyncio.get_event_loop().run_forever()


thread = threading.Thread(target=websocket_thread)
thread.start()


# import asyncio

# async def my_task():
#     # Async code goes here

# def start_task():
#     loop = asyncio.get_event_loop()
#     loop.call_soon_threadsafe(asyncio.ensure_future, my_task())

# thread = threading.Thread(target=start_task)
# thread.start()

