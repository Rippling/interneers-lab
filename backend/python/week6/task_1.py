import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# official gemini 2.5 flash prices
INPUT_PRICE_PER_1M = 0.30
OUTPUT_PRICE_PER_1M = 2.50


def calculate_cost(prompt_tokens, total_tokens):
    output_tokens = total_tokens - prompt_tokens
    inp_cost = (prompt_tokens/1000000)*INPUT_PRICE_PER_1M
    out_cost = (output_tokens/1000000)*OUTPUT_PRICE_PER_1M
    tot_cost = inp_cost + out_cost
    return inp_cost, out_cost, tot_cost, output_tokens


def run_prompt(temperature):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Generate 5 product names for a toy store. Return only a numbered list.",
        # extra settings for temperature
        config={
            "temperature": temperature
        }
    )
    print(f"\n===TEMPERATURE: {temperature}===")
    print("\nTEXT RESPONSE:")
    print(response.text)
    print("\nFULL RESPONSE:")
    print(response)
    # metadata : data about data
    usage = response.usage_metadata
    # number of tokens in input prompt
    prompt_tokens = getattr(usage, "prompt_token_count", 0)
    # total tokens used in whole request
    total_tokens = getattr(usage, "total_token_count", 0)
    # number of tokens in visible response text
    candidate_tokens = getattr(usage, "candidates_token_count", 0)
    # number of tokens used in thinking and internal reasoning
    thoughts_tokens = getattr(usage, "thoughts_token_count", 0)
    print("\nTOKEN USAGE:")
    print("Prompt tokens:", prompt_tokens)
    print("Candidate tokens:", candidate_tokens)
    print("Thoughts tokens:", thoughts_tokens)
    print("Total tokens:", total_tokens)
    inp_cost, out_cost, tot_cost, output_tokens = calculate_cost(
        prompt_tokens, total_tokens)
    print("\nCOST BREAKDOWN:")
    print("Output tokens:", output_tokens)
    print(f"Input cost: ${inp_cost:.8f}")
    print(f"Output cost: ${out_cost:.8f}")
    print(f"Total cost: ${tot_cost:.8f}")


# temperature controls randomness in token selection
# low temperature => less randomness => more stable outcomes
run_prompt(0.0)
run_prompt(0.5)
run_prompt(1)
run_prompt(1.5)
