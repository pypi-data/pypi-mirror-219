import os

from typing import Union

from langchain.embeddings.base import Embeddings
from langchain.embeddings import LlamaCppEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

from peelml.llm.constants import LlmName  

HUGGINGFACEEMBEDDING_MODEL_NAME = "hkunlp/instructor-large"


class EmbeddingFactory:
    @staticmethod
    def create_embedding(
        model_name: Union[str, LlmName],
        ) -> Embeddings:
        try: 
            model_name = LlmName(model_name)
            if model_name == LlmName.OPENAI:
                return OpenAIEmbeddings()
            elif model_name == LlmName.LLAMA_CPP:
                return LlamaCppEmbeddings(
                    model_path=os.getenv("LLAMA_CPP_PATH"))
            elif model_name == LlmName.SAGEMAKER:
                return HuggingFaceEmbeddings(
                    model_name=HUGGINGFACEEMBEDDING_MODEL_NAME,
                    cache_folder='./')
        except Exception as ex:
            raise Exception("Unknown embedding: {}".format(model_name)) from ex
