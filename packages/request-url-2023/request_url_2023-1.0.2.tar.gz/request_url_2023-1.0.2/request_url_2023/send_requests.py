import random
import sys

import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from fake_headers import Headers

# pip install fake-headers
# pip install aiohttp


def generate_header_list():
    header_list_len = 100
    header = Headers(
        # generate any browser & os headeers
        headers=False  # don`t generate misc headers
    )
    header_list = []
    for i in range(header_list_len):
        header_list.append(header.generate())
    return header_list

header_list = generate_header_list()

async def get_url(session, url):
    # print(url)
    header = random.choice(header_list)
    async with session.get(url, headers=header) as response:
        text = await response.text()
        return text

async def handler(url):
    try:
        async with aiohttp.ClientSession() as session:
            text = await get_url(session, url)
    except Exception as e:
        print("Error Url:", url)
        print(e)

async def engine(url,request_count):
    tasks = [
        asyncio.create_task(handler(url)) for _ in range(request_count)
    ]

    await asyncio.wait(tasks)

def task(url,request_count):
    asyncio.run(engine(url,request_count))

def run(url, TOTAL_COUNT = 1000,THREAD_NUM = 20,COROUTINE_REQUEST_COUNT = 50):
    # 总的请求数
    # TOTAL_COUNT = 10000
    # url
    # url = "https://www.baidu.com"
    # 线程池数目，
    # THREAD_NUM = 20
    # 每个协程同时发送多少个请求
    # COROUTINE_REQUEST_COUNT = 50
    # 初始化线程池
    pool = ThreadPoolExecutor(THREAD_NUM)
    #  1000/20=50，5
    loop_count, div = divmod(TOTAL_COUNT, COROUTINE_REQUEST_COUNT)
    # 循环50次 * 20 = 1000个请求
    for i in range(loop_count):
        # print(COROUTINE_REQUEST_COUNT)
        pool.submit(task, url, COROUTINE_REQUEST_COUNT)

    pool.submit(task, url, div)
    # 等待所有任务执行完毕
    pool.shutdown()





