from utils.llm.llmFactory.llm_factory import LLMFactory

# Create the selected LLM instance only once
llm = LLMFactory.get_llm()


def extract_invoice_json(ocr_text: str):
    """
    Extract invoice JSON using the configured LLM.
    The actual implementation (Local or Hugging Face)
    is selected by the LLM Factory.
    """
    return llm.extract_invoice_json(ocr_text)