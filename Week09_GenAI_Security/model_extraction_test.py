import ollama

def ask(prompt, model="smollm2:1.7b"):
    try:
        resp = ollama.generate(model=model, prompt=prompt)
        return getattr(resp, 'response', str(resp))
    except Exception as e:
        return (
            f"Error calling Ollama: {e}\n"
            "Hint: Ensure the Ollama daemon/CLI is installed and running. "
            "See https://ollama.com/download for installation instructions."
        )

inputs = [
    "Summarise the concept of Gen AI security in one sentence.",
    "Summarise the concept of Gen AI security in one sentence.",
    "Summarise the concept of Gen AI security in one sentence."
]

print("=== Model Extraction Pattern Test ===")
for i, prompt in enumerate(inputs):
    print(f"\nAttempt {i+1}")
    print(ask(prompt))
