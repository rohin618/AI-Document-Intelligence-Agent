import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

# -------------------------------------------------
# Load Environment
# -------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("Gemini API Key Loaded :", api_key is not None)

if api_key:
    print("Key Prefix :", api_key[:10] + "...")
else:
    print("ERROR : GEMINI_API_KEY not found!")

print("=" * 60)

# -------------------------------------------------
# Create Client
# -------------------------------------------------

client = genai.Client(api_key=api_key)

print("Gemini Client Created")
print("=" * 60)


# -------------------------------------------------
# Build Context
# -------------------------------------------------

def build_context(dashboard_data):

    print("Building Context...")

    context = {
        "summary": dashboard_data["summary"],
        "vendors": dashboard_data["vendors"][:5],
        "buyers": dashboard_data["buyers"][:5],
        "categories": dashboard_data["categories"][:5],
        "statistics": dashboard_data["statistics"],
        "prediction": dashboard_data["prediction"],
        "anomaly": dashboard_data["anomaly"],
    }

    print("Context Built")

    return context


# -------------------------------------------------
# Prompt
# -------------------------------------------------

def build_prompt(context, question):

    print("Building Prompt...")

    prompt = f"""
You are an Accounts Payable AI Copilot.

You answer questions ONLY using the dashboard data provided.

Rules

- Never invent values.
- Never assume missing information.
- If information is unavailable, clearly say so.
- Keep answers under 120 words.
- Give business-friendly answers.

Dashboard Data

{json.dumps(context, indent=2)}

User Question

{question}
"""

    print("Prompt Length :", len(prompt))

    return prompt


# -------------------------------------------------
# Ask AI
# -------------------------------------------------

def ask_dashboard_ai(dashboard_data, question):

    try:

        print("\nStep 1")
        context = build_context(dashboard_data)

        print("\nStep 2")
        prompt = build_prompt(context, question)

        print("\nStep 3")
        print("Sending request to Gemini...")

        start = time.time()

        response = client.interactions.create(
            model="gemini-3.1-flash-lite",
            input=prompt
        )

        end = time.time()

        print("Request Completed")
        print(f"Time Taken : {end-start:.2f} sec")

        print("\nStep 4")

        print("Response Object")
        print(response)

        print("\nStep 5")

        print(response.output_text)

        return response.output_text

    except ClientError as e:

        print("\nGemini Client Error")
        print(e)

        return str(e)
    
    

    except Exception as e:

        print("\nUnexpected Error")
        print(type(e))
        print(e)

        raise