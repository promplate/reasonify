from asyncio import Queue

END = object()


class QueueWrapper[T]:
    def __init__(self):
        self.queue = Queue[T]()

    def __aiter__(self):
        return self

    async def __anext__(self) -> T:
        data = await self.queue.get()
        if data is END:
            raise StopAsyncIteration
        return data

    def put(self, data: T):
        self.queue.put_nowait(data)

    def end(self):
        self.queue.put_nowait(END)  # type: ignore
