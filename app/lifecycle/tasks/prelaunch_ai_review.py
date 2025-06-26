import os
import subprocess


def review_with_ollama(prompt, model="llama3"):
    """Send prompt to local Ollama model."""
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(result.stdout.decode())


def review_with_lmstudio(
        prompt,
        api_url="http://localhost:1234/v1/chat/completions"):
    """Send prompt to LM Studio local API (OpenAI compatible)."""
    import requests

    response = requests.post(
        api_url,
        json={
            "model": "local-model",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
        },
        timeout=60,
    )
    print(response.json()["choices"][0]["message"]["content"])


if __name__ == "__main__":
    # Example: Review backend main API file
    with open("../../backend/main.py") as f:
        code = f.read()
    prompt = (
        "Review code for best practices, security, and missing tests. "
        "Suggest improvements and highlight any issues:\n\n" + code)

    # Choose your local AI model provider:
    if os.environ.get("USE_LMSTUDIO"):
        review_with_lmstudio(prompt)
    else:
        review_with_ollama(prompt)
