import websockets
import asyncio
import time

def get_from_file():
    with open("/worker-app/.indexer_progress_bar", "r") as f:
        return str(f.read())


async def send_progress_info(websocket, path):
    while True:
        data = get_from_file()
        print(f"data: {data}%")
        await websocket.send(str(data))
        time.sleep(1)


if __name__ == "__main__":
    server = websockets.serve(send_progress_info, "0.0.0.0", 7070)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
