import os
from dotenv import load_dotenv

from utils.llm.llmList.local_qwen import LocalQwenLLM
from utils.llm.llmList.hf_qwen import HFQwen

load_dotenv()

LLM_ENGINE = os.getenv("LLM_ENGINE", "local").lower()


class LLMFactory:

    @staticmethod
    def get_llm():

        if LLM_ENGINE == "local":
            print("\nUsing Local Qwen Model\n")
            return LocalQwenLLM()

        elif LLM_ENGINE == "hf":
            print("\nUsing Hugging Face Qwen API\n")
            return HFQwen()

        else:
            raise ValueError(
                f"Unsupported LLM Engine: {LLM_ENGINE}. "
                "Supported engines: local, hf"
            )