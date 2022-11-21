#异步执行使用：asyncio

import time
import asyncio

async def hello():
    await asyncio.sleep(1)
    print('hello world:%s'% time.time())

loop = asyncio.get_event_loop()
task=[hello() for i in range(5)]
loop.run_until_complete(asyncio.wait(task))

from aiohttp import ClientSession

tasks=[]
url="http://www.baidu.com/{}"
