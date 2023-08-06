#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2023/6/30 16:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.cache_utils import diskcache


def init(verbose=-1):
    import openai

    OPENAI_CACHE = os.getenv("OPENAI_CACHE", "~/.cache/openai_cache")

    openai.Embedding.create = diskcache(
        openai.Embedding.create,
        location=f"{OPENAI_CACHE}_EMBEDDINGS",
        verbose=verbose
    )

    openai.Completion.create = diskcache(
        openai.Completion.create,
        location=f"{OPENAI_CACHE}_Completion",
        verbose=verbose
    )

    openai.ChatCompletion.create = diskcache(
        openai.ChatCompletion.create,
        location=f"{OPENAI_CACHE}_ChatCompletion",
        verbose=verbose
    )
    #
    # from chatllm.langchain.vectorstores.base import VectorStoreRetriever as _VectorStoreRetriever
    # from langchain.vectorstores.base import VectorStoreRetriever
    #
    # VectorStoreRetriever._get_relevant_documents = _VectorStoreRetriever._get_relevant_documents

# openai.Completion.acreate
