#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/7/4 08:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains.base import Chain

# prompt_template = "Tell me a {adjective} joke"
# prompt = PromptTemplate(
#     input_variables=["adjective"], template=prompt_template
# )

template2prompt = PromptTemplate.from_template


async def stream_chat(chain: Chain, query):

    handler = AsyncIteratorCallbackHandler()
    coroutine = chain.arun({"question": "什么叫做职教高考", "chat_history": []}, callbacks=[handler])
    task = asyncio.create_task(coroutine)

    async for token in handler.aiter():
        yield token
        # print(f"{token}", end='')
