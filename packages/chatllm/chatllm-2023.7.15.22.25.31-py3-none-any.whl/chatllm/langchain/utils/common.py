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
from langchain.document_loaders.base import Document

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains.base import Chain

# prompt_template = "Tell me a {adjective} joke"
# prompt = PromptTemplate(
#     input_variables=["adjective"], template=prompt_template
# )

template2prompt = PromptTemplate.from_template


def docs2dataframe(docs: List[Document]) -> pd.DataFrame:
    return pd.DataFrame(map(lambda doc: {**doc.metadata, **{'page_content': doc.page_content}}, docs))
