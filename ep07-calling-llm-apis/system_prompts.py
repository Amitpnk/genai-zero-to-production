"""Same question, three system prompts: the system prompt sets the role and the rules."""

from shared.llm import chat, provider_from_args

provider = provider_from_args()
question = [{"role": "user", "content": "My order arrived damaged. What should I do?"}]

systems = {
    "none": None,
    "support agent": (
        "You are a support agent for an online bookshop. Be warm and brief (max 2 sentences). "
        "Always ask for the order number."
    ),
    "strict JSON": (
        'Classify the customer message. Reply with only JSON: {"intent": string, "urgency": "low"|"medium"|"high"}'
    ),
}

print(f"Provider: {provider}\nQuestion: {question[0]['content']}\n")
for name, system in systems.items():
    reply = chat(question, system=system, provider=provider, max_tokens=150)
    print(f"--- system prompt: {name}")
    print(reply.text.strip(), "\n")
