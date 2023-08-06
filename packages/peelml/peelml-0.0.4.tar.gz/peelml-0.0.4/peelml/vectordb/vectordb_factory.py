from typing import Union

from peelml.llm.constants import LlmName
from peelml.llm.embedding_factory import EmbeddingFactory
from peelml.vectordb.abs_vectordb import AbsVectorDb
from peelml.vectordb.chroma import ChromaDb
from peelml.vectordb.constants import VectorDbName


class VectorDbFactory:
    @staticmethod
    def create_vector_db(
        model_name: Union[str, LlmName],
        vector_db_name: Union[str, VectorDbName]) -> AbsVectorDb:
        try: 
            vector_db_name = VectorDbName(vector_db_name)
            model_name = LlmName(model_name)
            model_embedding = EmbeddingFactory.create_embedding(
                model_name.value)
            if vector_db_name == VectorDbName.CHROMA:
                return ChromaDb(model_embedding)

        except Exception as ex:
            raise Exception("Unknown db: {}".format(vector_db_name)) from ex
