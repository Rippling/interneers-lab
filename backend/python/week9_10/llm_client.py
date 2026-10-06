# adapter bw code and gemini (langchain cover)
# produces langchain compatible chat model backed by gemini
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from week9_10.config import GEMINI_MODEL_NAME, GEMINI_TEMPERATURE

load_dotenv()


# we are using langchain wrapper not direct gemini to directly trace langchain whenever needed
def get_chat_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing in the environment.")
    else:
        return ChatGoogleGenerativeAI(
            model=GEMINI_MODEL_NAME,
            temperature=GEMINI_TEMPERATURE,
            google_api_key=api_key,
        )


# just to test whether this file is working or not i.e calls are made or not and responses are received or not
if __name__ == "__main__":
    llm = get_chat_model()
    response = llm.invoke("Say hello in 5 words.")
    print(response.content)
