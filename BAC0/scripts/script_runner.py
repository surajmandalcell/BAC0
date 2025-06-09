import asyncio
import typing as t
from signal import SIGINT, SIGTERM, signal
from typing import Callable, Optional, Coroutine, Any


def run(main_task: Callable[[], Coroutine[Any, Any, None]], bacnet: Optional[Any]) -> None:
    global loop

    def handler(sig: int, sig2: Any) -> None:
        if bacnet is not None:
            bacnet._log.info(f"Got signal: {sig!s}, shutting down.")
            bacnet.disconnect()
        loop.stop()

    try:
        loop = (
            asyncio.get_running_loop()
        )  # we also could have chosen get_event_loop(), and if we did we would not have needed to set_event_loop() and create a new event loop
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # for sig in (SIGINT, SIGTERM):
    #    loop.add_signal_handler(sig, handler)
    signal(SIGINT, handler)
    signal(SIGTERM, handler)

    loop.create_task(main_task())
    loop.run_forever()
    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
