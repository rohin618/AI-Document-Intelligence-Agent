import os
import json
import traceback
import requests

from dotenv import load_dotenv

from prompt.invoice_prompt import build_invoice_prompt
from utils.llm.base_llm import BaseLLM


# Load .env variables
load_dotenv()


class HFQwen(BaseLLM):

    MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct:featherless-ai"

    def __init__(self):

        self.api_url = "https://router.huggingface.co/v1/chat/completions"

        self.token = os.getenv("HF_TOKEN")

        if not self.token:
            raise Exception("HF_TOKEN not found in .env file")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        print("Connected to HuggingFace API")

    def extract_invoice_json(self, ocr_text: str):

        try:

            print("\n==============================")
            print("STEP 1 : Building Prompt")
            print("==============================")

            messages = build_invoice_prompt(ocr_text)

            print("Prompt Built Successfully")

            print("\n==============================")
            print("STEP 2 : Sending Request")
            print("==============================")

            payload = {
                "model": self.MODEL_NAME,
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": 1024
            }

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )

            if response.status_code != 200:
                print("Status Code:", response.status_code)
                print("Response:")
                print(response.text)
                return {
                    "error": response.text
                }

            result = response.json()

            print("Response Received")

            print("\n==============================")
            print("STEP 3 : Reading Response")
            print("==============================")

            output = result["choices"][0]["message"]["content"]

            print(output)

            print("\n==============================")
            print("STEP 4 : Parsing JSON")
            print("==============================")

            start = output.find("{")
            end = output.rfind("}") + 1

            if start == -1 or end == 0:

                print("No JSON Found")

                return {
                    "raw_response": output
                }

            output = output[start:end]

            invoice = json.loads(output)

            print("JSON Parsed Successfully")

            return invoice

        except Exception as e:

            print("\n")
            print("=" * 80)
            print("HUGGINGFACE ERROR")
            print("=" * 80)

            traceback.print_exc()

            print("=" * 80)

            return {
                "error": str(e)
            }