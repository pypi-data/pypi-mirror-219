from enum import Enum


class LlmName(Enum):
    LLAMA_CPP = "llama_cpp"
    OPENAI = "openai"
    SAGEMAKER = "sagemaker"
