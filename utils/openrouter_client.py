# import os
# import requests
# from dotenv import load_dotenv

# # 🔴 LOAD ENV FIRST
# load_dotenv()

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# if not OPENROUTER_API_KEY:
#     raise RuntimeError("OPENROUTER_API_KEY not set")

# OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# # 🆓 FREE MODELS (ordered by quality)
# FREE_MODELS = [
#     "mistralai/mistral-7b-instruct",
#     "openchat/openchat-3.5",
#     "gryphe/mythomist-7b",
# ]

# HEADERS = {
#     "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#     "Content-Type": "application/json",
#     # Optional but recommended by OpenRouter
#     "HTTP-Referer": "http://localhost",
#     "X-Title": "JobScanner",
# }


# def chat_completion(messages: list[str]) -> str:
#     """
#     Try free models in order until one succeeds.
#     """

#     last_error = None

#     for model in FREE_MODELS:
#         try:
#             response = requests.post(
#                 OPENROUTER_URL,
#                 headers=HEADERS,
#                 json={
#                     "model": model,
#                     "messages": messages,
#                 },
#                 timeout=60,
#             )

#             if response.status_code == 200:
#                 data = response.json()
#                 return data["choices"][0]["message"]["content"]

#             else:
#                 last_error = f"{model} → {response.status_code}"
#                 continue

#         except Exception as e:
#             last_error = f"{model} → {str(e)}"
#             continue

#     raise RuntimeError(f"All free models failed. Last error: {last_error}")

# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# if not OPENROUTER_API_KEY:
#     raise RuntimeError("OPENROUTER_API_KEY not set")

# OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# HEADERS = {
#     "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#     "Content-Type": "application/json",
#     "HTTP-Referer": "http://localhost",
#     "X-Title": "JobScanner",
# }

# MODELS = [
#     "openai/gpt-4.1-mini",              # paid (best)
#     "mistralai/mistral-7b-instruct",    # free fallback
# ]

# def chat_completion(messages: list[str]) -> str:
#     last_error = None

#     for model in MODELS:
#         try:
#             response = requests.post(
#                 OPENROUTER_URL,
#                 headers=HEADERS,
#                 json={
#                     "model": model,
#                     "messages": messages,
#                 },
#                 timeout=30,
#             )

#             if response.status_code == 402:
#                 raise RuntimeError("Payment required")

#             response.raise_for_status()

#             data = response.json()
#             return data["choices"][0]["message"]["content"]

#         except Exception as e:
#             last_error = f"{model} → {e}"
#             print(f"[WARN] {last_error}")

#     raise RuntimeError(f"All models failed. Last error: {last_error}")


# import requests
# from dotenv import load_dotenv
# import os

# load_dotenv()

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# def chat_completion(prompt: str) -> str:
#     url = "https://openrouter.ai/api/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "openai/gpt-4o-mini",
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }

#     response = requests.post(url, headers=headers, json=data)

#     print("STATUS CODE:", response.status_code)
#     print("RAW RESPONSE:", response.text)

#     if response.status_code != 200:
#         raise Exception(f"OpenRouter Error: {response.text}")

#     result = response.json()

#     return result["choices"][0]["message"]["content"]

import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")


def generate_text(prompt: str) -> str:
    """
    Sends prompt to OpenRouter and returns generated text.
    """

    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        # Check for API error
        if "error" in result:
            raise Exception(result["error"]["message"])

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {str(e)}")

    except Exception as e:
        raise Exception(f"OpenRouter error: {str(e)}")
