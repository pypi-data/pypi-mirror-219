#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatdoc
# @Time         : 2023/7/15 20:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *

from chatllm.langchain.utils import docs2dataframe
from chatllm.langchain.decorators import llm_stream
from chatllm.langchain.vectorstores import Milvus
from chatllm.langchain.embeddings import OpenAIEmbeddings
from chatllm.langchain.document_loaders import FilesLoader

from langchain.text_splitter import *
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.base import Embeddings


class ChatBase(object):

    def __init__(self, model: str = "gpt-3.5-turbo-16k-0613",
                 collection_name: str = 'TEST',
                 embeddings: Embeddings = OpenAIEmbeddings(chunk_size=5),
                 temperature=0
                 ):
        self.embeddings = embeddings
        self.collection_name = collection_name
        self.llm = ChatOpenAI(model=model, temperature=temperature, streaming=True)
        self.chain = load_qa_chain(self.llm, chain_type="stuff")

        # self.chain.llm_chain.prompt.messages[0].prompt.template = \
        #     f'System time: {datetime.datetime.now()};' \
        #     + self.chain.llm_chain.prompt.messages[0].prompt.template

        _vdb_kwargs = self.vdb_kwargs.copy()
        _vdb_kwargs['embedding_function'] = _vdb_kwargs.pop('embedding')
        self.vdb: Optional[Milvus] = Milvus(**_vdb_kwargs)

    @staticmethod
    def load_file(file_paths):
        loader = FilesLoader(file_paths)
        docs = loader.load_and_split(
            RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200, add_start_index=True)
        )
        return docs

    @diskcache(location=os.getenv('INSERT_VECTOR_CACHE', '~/.cache/insert_vector_cache'), ignore=['self'])
    def create_index(self, docs: List[Document], **kwargs):
        """初始化 drop_old=True"""
        self.vdb = Milvus.from_documents(docs, **{**self.vdb_kwargs, **kwargs})

    def llm_qa(self, query: str, k: int = 5, threshold: float = 0.5, **kwargs: Any):
        docs = self.vdb.similarity_search(query, k=max(k, 10), threshold=threshold, **kwargs)
        docs = docs | xUnique_plus(lambda doc: doc.page_content.strip())  # 按内容去重
        docs = docs[:k]
        # todo: 上下文信息
        docs = [Document(page_content=f"system time: {datetime.datetime.now()}")] + docs
        if docs:
            return llm_stream(self.chain.run)({"input_documents": docs, "question": query})

    @cached_property
    def vdb_kwargs(self):
        connection_args = {
            'uri': os.getenv('ZILLIZ_ENDPOINT'),
            'token': os.getenv('ZILLIZ_TOKEN')
        }
        address = os.getenv('MILVUS_ADDRESS')
        if address:
            connection_args.pop('uri')
            connection_args['address'] = address

        index_params = {
            "metric_type": "IP",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }

        embedding_function = self.embeddings

        vdb_kwargs = dict(
            embedding=embedding_function,
            connection_args=connection_args,
            index_params=index_params,
            search_params=None,
            collection_name=self.collection_name,
            drop_old=False,
        )

        return vdb_kwargs
