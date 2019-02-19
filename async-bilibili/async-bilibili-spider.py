import asyncio
import aiofiles
import os
import json
import time
from aiohttp import ClientSession

MAX_CONNECT_COUNT = 64
NUMBER = 10000
SLEEP = 23

async def fetch(sem, url, session):
    '''
    异步请求视频数据
    :param sem: Semaphore 实例
    :param url: 请求的链接
    :param session: ClientSession实例
    :return: 视频数据
    '''

    try:
        async with sem:
            async with session.get(url) as response:
                data = await response.json()
            if data and data.get("code", None) == 0:  # 只返回有效数据
                return data
    except Exception as e:
        print(e)

async def run(start, stop):
    start_url = "http://api.bilibili.com/archive_stat/stat?aid={}"
    sem = asyncio.Semaphore(MAX_CONNECT_COUNT)
    async with ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(sem, start_url.format(i), session)) for i in range(start, stop)]
        return await asyncio.gather(*tasks)

async def save_to_files(start, stop, path, label):
    """
    异步存储到文件
    :param start:
    :param stop:
    :param path: 存储路径
    :param label: 任务名称
    :return:
    """
    print(f"Running: job {label}")
    data = await asyncio.gather(asyncio.ensure_future(run(start, stop)))
    result = [d for d in data[0] if d]
    async with aiofiles.open(path, mode="w+") as f:
        await f.write(json.dumps(result))
        print(f"Fetch data: {len(result)}")

def get_files_tasks(index):
    """
    获取 `save_to_files()` 所需任务
    :param index: 任务索引
    :return: 任务列表
    """
    _tasks = [
        asyncio.ensure_future(
            save_to_files(
                start=NUMBER * i[0],
                stop=NUMBER * i[1],
                path=os.path.join("data", "{}.json".format(NUMBER * i[1])),
                label=i[1],
            )
        )
        for i in [(index, index + 1), (index + 1, index + 2)]
    ]
    return _tasks


if __name__ == "__main__":
    t1 = time.clock()
    loop = asyncio.get_event_loop()
    for index in range(0, 900, 2):
        tasks = get_files_tasks(index)
        loop.run_until_complete(asyncio.gather(*tasks))
        print("Sleep for a while: {}s".format(SLEEP))
        time.sleep(SLEEP)
    print(time.clock()-t1)

