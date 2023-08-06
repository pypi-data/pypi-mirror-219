# openlimitHW

简单高效的 OpenAI API 速率限制器。它可以：

- 处理 _请求_ 和 _令牌_ 限制
- 协调多个 API KEY

## 安装

您可以使用 pip 安装 `openlimitHW`：

```bash
$ pip install openlimitHW
```

## 使用

### 定义速率限制

首先，为您使用的 OpenAI 模型定义速率限制。例如：

```python
from openlimit import ChatRateLimiter

rate_limiter = ChatRateLimiter(request_limit=3, token_limit=50000)
```
这为chat completion model（例如 gpt-4，gpt-3.5-turbo）设置了速率限制。`openlimit` 提供了不同的速率限制器对象，用于不同的 OpenAI 模型，所有对象都具有相同的参数：`request_limit` 和 `token_limit`。两种限制都是 每分钟 的量，可能因用户而异。

### 异步请求

速率限制也可以用于异步请求：

```python
async def call_openai():
    chat_params = { 
        "model": "gpt-4", 
        "messages": [{"role": "user", "content": "Hello!"}]
    }

    async with rate_limiter.limit(**chat_params):
        response = await openai.ChatCompletion.acreate(**chat_params)
        rate_limiter.update(response)
```