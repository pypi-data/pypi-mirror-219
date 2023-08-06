import asyncio
from contextlib import asynccontextmanager
from typing import Any, Coroutine, Sequence

from tqdm import tqdm

from beni import block
from beni.btype import AnyType


@asynccontextmanager
async def show(total: int):
    '''```py
    # Example
    async with bprogress.show(100) as update:
        while True:
            await asyncio.sleep(1)
            update()
    ```'''
    print()
    with tqdm(total=total, ncols=70) as progress:
        yield progress.update
    print()


async def run(
    ary: Sequence[Coroutine[Any, Any, AnyType]],
    limit: int = 999999,
) -> Sequence[AnyType]:
    '''```py
    # Example
    await bprogress.run(
        [myfun() for _ in range(100)],
        10,
    )
    ```'''
    print()
    with tqdm(total=len(ary), ncols=70) as progress:
        @block.limit(limit)
        async def task(x: Coroutine[Any, Any, AnyType]):
            result = await x
            progress.update()
            return result
        result = await asyncio.gather(*[task(x) for x in ary])
    print()
    return result
