from typing import Union

from peelml.llm.abs_llm import AbsLlm
from peelml.llm.openai import OpenAIModel
from peelml.llm.llama_cpp import LlamaCppModel
from peelml.llm.constants import LlmName
from peelml.llm.sagemaker import SageMaker
from peelml.vectordb.abs_vectordb import AbsVectorDb


class ModelFactory:
    @staticmethod
    def create_model(
        model_name: Union[str, LlmName],
        vector_db: AbsVectorDb
        ) -> AbsLlm:
        try: 
            model_name = LlmName(model_name)
            if model_name == LlmName.OPENAI:
                return OpenAIModel(vector_db)
            elif model_name == LlmName.LLAMA_CPP:
                return LlamaCppModel(vector_db)
            elif model_name == LlmName.SAGEMAKER:
                return SageMaker(vector_db)
        except Exception as ex:
            raise Exception("Unknown model: {}".format(model_name)) from ex
