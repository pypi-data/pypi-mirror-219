import os

from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp

from peelml.llm.abs_llm import AbsLlm
from peelml.vectordb.abs_vectordb import AbsVectorDb

MIN_DOCS = 2


class LlamaCppModel(AbsLlm):
    """
    A class representing a LlamaCpp model for language modeling.
    """
    def __init__(self, vector_db: AbsVectorDb):
        """
        Initializes the LlamaCppModel class.
        """
        try:
            # without 1024 context length, the model will not work
            # with below error, ValueError: Requested tokens (...)
            # exceed context window of 512
            llm = LlamaCpp(model_path=os.getenv("LLAMA_CPP_PATH"),
                           n_ctx=1024)

            vector_db = vector_db.vector_db

            retrieve_qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vector_db.as_retriever(search_kwargs={"k": MIN_DOCS}))

            super().__init__(retrieve_qa)
        except Exception as ex:
            print("Inference initialization failed: {}".format(ex))
