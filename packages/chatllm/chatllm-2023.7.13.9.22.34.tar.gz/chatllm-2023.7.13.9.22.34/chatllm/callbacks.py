#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : callbacks
# @Time         : 2023/7/12 17:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from threading import Thread

from langchain.chat_models import ChatOpenAI as _ChatOpenAI

from chatllm.langchain.callbacks.streaming import StreamingGeneratorCallbackHandler
from meutils.pipe import *




class ChatOpenAI(_ChatOpenAI):




    def stream(self, text: str) -> Generator:
        """Stream the answer to a query.

        NOTE: this is a beta feature. Will try to build or use
        better abstractions about response handling.

        Args:
            prompt (Prompt): Prompt to use for prediction.

        Returns:
            str: The predicted answer.

        """

        handler = StreamingGeneratorCallbackHandler()

        self.callbacks = [handler]

        if not getattr(self, "streaming", False):
            raise ValueError("LLM must support streaming and set streaming=True.")

        thread = Thread(target=self.predict, args=[text])
        thread.start()

        response_gen = handler.get_response_gen()

        # NOTE/TODO: token counting doesn't work with streaming
        return response_gen


if __name__ == '__main__':
    llm = ChatOpenAI(streaming=True, temperature=0)
    for i in llm.stream('你好'):
        print(i, end='')
