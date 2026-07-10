import json
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from prompt.invoice_prompt import build_invoice_prompt


# -------------------------------------------------
# Model Configuration
# -------------------------------------------------

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading Qwen Model ({MODEL_NAME}) on {device}...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto"
).to(device)

model.eval()

print("Qwen Loaded Successfully!")


# -------------------------------------------------
# Invoice Extraction
# -------------------------------------------------

def extract_invoice_json(ocr_text: str):

    try:

        print("\n==============================")
        print("STEP 1 : Building Prompt")
        print("==============================")

        messages = build_invoice_prompt(ocr_text)

        print("Prompt Built Successfully")

        print("\n==============================")
        print("STEP 2 : Applying Chat Template")
        print("==============================")

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        print("Chat Template Applied")

        print("\n==============================")
        print("STEP 3 : Tokenizing")
        print("==============================")

        model_inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=4096
        ).to(device)

        print("Tokenization Complete")
        print("Input Tokens :", model_inputs.input_ids.shape[1])

        print("\n==============================")
        print("STEP 4 : Generating")
        print("==============================")

        with torch.inference_mode():

            outputs = model.generate(
                **model_inputs,
                max_new_tokens=1024,
                do_sample=False,
                temperature=0.1,
                repetition_penalty=1.05,
                eos_token_id=tokenizer.eos_token_id
            )

        print("Generation Complete")

        print("\n==============================")
        print("STEP 5 : Decoding")
        print("==============================")

        generated = outputs[0][model_inputs.input_ids.shape[1]:]

        response = tokenizer.decode(
            generated,
            skip_special_tokens=True
        ).strip()

        print("Decoded Successfully")

        print("\n==============================")
        print("MODEL OUTPUT")
        print("==============================")
        print(response)
        print("==============================")

        print("\n==============================")
        print("STEP 6 : Parsing JSON")
        print("==============================")

        start = response.find("{")
        end = response.rfind("}") + 1

        if start == -1 or end == 0:
            print("No JSON object found.")
            return {
                "raw_response": response
            }

        response = response[start:end]

        invoice = json.loads(response)

        print("JSON Parsed Successfully")

        return invoice

    except Exception as e:

        import traceback

        print("\n")
        print("=" * 80)
        print("LLM ERROR")
        print("=" * 80)

        traceback.print_exc()

        print("=" * 80)

        return {
            "error": str(e)
        }