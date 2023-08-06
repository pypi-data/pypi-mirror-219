
# Introduction
## Install package
```shell
pip install request-url-2023
```
##  Example Usage:
```python
from request_url_2023 import send_requests

send_requests.run(url="https://www.hrtechchina.com/")
```

## Params

```python
from request_url_2023 import send_requests

# 总的请求数
# TOTAL_COUNT = 10000
# 线程池数目，
# THREAD_NUM = 20
# 每个协程同时发送多少个请求
# COROUTINE_REQUEST_COUNT = 50

send_requests.run(
    url="https://www.hrtechchina.com/",
    TOTAL_COUNT = 1000,
    THREAD_NUM = 20,
    COROUTINE_REQUEST_COUNT = 50)
```
```