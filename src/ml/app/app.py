from settings import RABBIT_URL, RABBIT_PORT
from process_audio import process
import asyncio

from aio_pika import connect_robust
from aio_pika.patterns import RPC


async def main() -> None:
    connection = await connect_robust(port=RABBIT_PORT, host=RABBIT_URL,
        client_properties={"connection_name": "callee"},
    )

    # Creating channel
    channel = await connection.channel()

    rpc = await RPC.create(channel)
    await rpc.register("v", process, auto_delete=True)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())