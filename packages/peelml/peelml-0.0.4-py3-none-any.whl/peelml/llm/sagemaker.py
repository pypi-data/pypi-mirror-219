import os
import json

from typing import Dict
from langchain import SagemakerEndpoint
from langchain.chains import RetrievalQA
from langchain.llms.sagemaker_endpoint import LLMContentHandler

from peelml.llm.abs_llm import AbsLlm
from peelml.vectordb.abs_vectordb import AbsVectorDb

MIN_DOCS = 2

class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        input_str = json.dumps({"inputs": prompt, **model_kwargs})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generated_text"]


class SageMaker(AbsLlm):
    """
    A class representing a language model that uses OpenAI's GPT-3 to generate text.
    """
    def __init__(self, vector_db: AbsVectorDb):
        """
        Initializes the OpenAIModel class.
        """
        try:
            parameters = {
                "do_sample": True,
                "top_p": 0.7,
                "temperature": 0.1,
                "top_k": 5,
                "max_new_tokens": 500,
                "repetition_penalty": 1.03,
                "stop": ["<|endoftext|>"]
            }

            llm=SagemakerEndpoint(
                    endpoint_name=os.environ["SAGEMAKER_ENDPOINT_NAME"],
                    region_name="us-west-2",
                    model_kwargs={"parameters": parameters},
                    content_handler=ContentHandler(),
                )


            vector_db = vector_db.vector_db

            retrieve_qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vector_db.as_retriever(search_kwargs={"k": MIN_DOCS}))

            super().__init__(retrieve_qa)
        except Exception as ex:
            print("Inference initialization failed: {}".format(ex))
