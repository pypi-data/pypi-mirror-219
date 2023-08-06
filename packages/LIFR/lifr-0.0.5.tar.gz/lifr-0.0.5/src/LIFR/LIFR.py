import asyncio
import websockets
print("hello")
async def send():
    async with websockets.connect('ws://localhost:8765') as websocket:
        # Send a message to the server
        await websocket.send('{"ask":"la valeur","data":["la valeur [x1] est-elle plus grande que 6 vu que [x1]>6 alors oui [break] plus grande que 6 vu que [x1]<6 alors non [break]"]}')

        # Receive and print the server's response
        response = await websocket.recv()
        print(f'Received: {response}')

def generate(content):
	asyncio.get_event_loop().run_until_complete(send(content))
