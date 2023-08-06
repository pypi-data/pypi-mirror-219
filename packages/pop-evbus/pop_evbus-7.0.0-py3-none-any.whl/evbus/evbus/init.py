import asyncio
from typing import Any
from typing import Dict
from typing import List

STOP_ITERATION = object()


def __init__(hub):
    hub.evbus.STARTED = False
    for dyne in ("acct", "ingress", "output", "serial", "match"):
        hub.pop.sub.add(dyne_name=dyne)


async def start(hub, contexts: Dict[str, List[Dict[str, Any]]]):
    hub.log.debug("Starting event bus")
    hub.evbus.STARTED = True

    # Initialize the queue in the current loop
    bus: asyncio.Queue = await hub.evbus.broker.init()

    while True:
        event = await bus.get()
        if event is STOP_ITERATION:
            # Check if there are more events after terminal (STOP_ITERATION) events
            if bus.qsize() > 0:
                # It should push the terminal (STOP_ITERATION) event in the back of the queue
                # This is to make sure all events are processed before stopping
                await hub.evbus.BUS.put(STOP_ITERATION)
                continue
            else:
                hub.log.info("Event bus was forced to stop")
                return
        await hub.evbus.broker.propagate(contexts=contexts, event=event)


async def stop(hub):
    """
    Stop the event bus
    """
    hub.log.debug("Stopping the event bus")
    hub.evbus.BUS.put_nowait(STOP_ITERATION)


async def join(hub):
    while not hub.evbus.STARTED:
        await hub.pop.loop.sleep(0)
