# this file communicates with gemini
import os
from dotenv import load_dotenv
from google import genai
from week8.config import GEMINI_MODEL_NAME, GEMINI_TEMPERATURE
from langsmith import traceable


load_dotenv()

# retriever => retrieval onlu
# prompt_builder => prompt only
# llm_client => gemini call only

# 1. load gemini api key
# 2. create gemini client
# 3. send prompt to gemini
# 4. get back final ans text


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing in the environment.")
    return genai.Client(api_key=api_key)


@traceable(
    run_type="llm",
    name="gemini_generate_answer",
    metadata={
        "ls_provider": "google_genai",
        "ls_model_name": GEMINI_MODEL_NAME,
    },
)
def generate_answer(prompt: str) -> str:
    client = get_gemini_client()

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt,
        config={
            "temperature": GEMINI_TEMPERATURE,
        },
    )

    if not response.text:
        return "I could not generate a response."

    return response.text.strip()
