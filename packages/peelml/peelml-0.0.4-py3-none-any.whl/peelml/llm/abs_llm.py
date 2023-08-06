from abc import ABC

from langchain.chains import RetrievalQA


class AbsLlm(ABC):
    def __init__(self, retrieve_qa: RetrievalQA):
        self._retrieve_qa = retrieve_qa

    def run(self, message: str):
        return self._retrieve_qa.run(message)
