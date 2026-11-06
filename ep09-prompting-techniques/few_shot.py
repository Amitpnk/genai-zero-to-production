"""Zero-shot vs one-shot vs few-shot: which examples actually help?

Episode 8 ended with a support bot that picked the same action for almost every message,
because its only example used that action. Here we classify 12 customer messages into one
of three actions, with four prompt versions, and measure accuracy over several runs.
"""

from collections import Counter

from shared.llm import chat, provider_from_args

provider = provider_from_args()
RUNS = 5
ACTIONS = ["offer_replacement_or_refund", "send_tracking", "escalate"]

INSTRUCTIONS = (
    "You are a support agent for Pageturn, an online bookshop. Choose the right action for the customer message.\n"
    "Policy: damaged or wrong items get a replacement or refund. Late or missing orders get the tracking link. "
    "Billing problems, threats, complaints about repeated failures, or demands for compensation go to a human (escalate).\n"
    "Reply with only one action name: offer_replacement_or_refund, send_tracking or escalate."
)

# Examples are never taken from the test set below.
ONE_EXAMPLE = [
    ("My mug arrived chipped.", "offer_replacement_or_refund"),
]
SAME_LABEL_EXAMPLES = [
    ("My mug arrived chipped.", "offer_replacement_or_refund"),
    ("The cover of my atlas is ripped.", "offer_replacement_or_refund"),
    ("You sent me the wrong edition of 'Emma'.", "offer_replacement_or_refund"),
]
ONE_PER_ACTION = [
    ("My mug arrived chipped.", "offer_replacement_or_refund"),
    ("I ordered a week ago. Where is my parcel?", "send_tracking"),
    ("You took the money from my card twice!", "escalate"),
]
VARIED_WITH_TRICKY = ONE_PER_ACTION + [
    ("The book arrived damaged and I want a free gift card for the trouble.", "escalate"),
]

TEST_SET = [  # (customer message, the action the policy says is right)
    ("My copy of 'Circe' has a big coffee stain on the first 20 pages.", "offer_replacement_or_refund"),
    ("You sent me 'The Hobbit' but I ordered 'The Silmarillion'.", "offer_replacement_or_refund"),
    ("The spine cracked the first time I opened the book.", "offer_replacement_or_refund"),
    ("Pages 40 to 80 are missing from my novel.", "offer_replacement_or_refund"),
    ("Where is my order? It was meant to arrive yesterday.", "send_tracking"),
    ("Has my parcel shipped yet? I ordered on Friday.", "send_tracking"),
    ("It's been 10 days and still nothing in my letterbox.", "send_tracking"),
    ("Can you tell me when my books will get here?", "send_tracking"),
    ("I've been charged twice for the same order.", "escalate"),
    ("This is the fourth time I've written. I want to speak to a manager.", "escalate"),
    ("Give me a 50% discount or I'm leaving a 1-star review.", "escalate"),
    ("My book arrived late AND damaged. I want compensation, not just a refund.", "escalate"),
]


def build_prompt(examples, message):
    parts = [INSTRUCTIONS]
    if examples:
        shots = "\n\n".join(f"<message>{text}</message>\nAction: {label}" for text, label in examples)
        parts.append("Examples:\n\n" + shots)
    parts.append(f"<message>{message}</message>\nAction:")
    return "\n\n".join(parts)


def parse_action(text):
    """Return the first allowed action the reply mentions, or None."""
    text = text.lower()
    found = [(text.find(action), action) for action in ACTIONS if action in text]
    return min(found)[1] if found else None


VERSIONS = {
    "zero-shot": [],
    "one-shot (Ep 8)": ONE_EXAMPLE,
    "few-shot, same label": SAME_LABEL_EXAMPLES,
    "few-shot, 1 per action": ONE_PER_ACTION,
    "few-shot, + tricky one": VARIED_WITH_TRICKY,
}

print(f"Provider: {provider} · {len(TEST_SET)} messages × {RUNS} runs per version\n")
results = {}
for name, examples in VERSIONS.items():
    correct, per_label, picked = 0, Counter(), Counter()
    for message, expected in TEST_SET:
        for _ in range(RUNS):
            reply = chat([{"role": "user", "content": build_prompt(examples, message)}],
                         provider=provider, temperature=0.7, max_tokens=20).text
            action = parse_action(reply)
            picked[action or "invalid"] += 1
            if action == expected:
                correct += 1
                per_label[expected] += 1
    results[name] = (correct, per_label, picked)
    print(f"{name:<24} accuracy {correct}/{len(TEST_SET) * RUNS}   picked: {dict(picked)}")

per_label_total = Counter(label for _, label in TEST_SET)
print(f"\n{'accuracy by right answer':<24}" + "".join(f"{a:>30}" for a in ACTIONS) + f"{'overall':>10}")
for name, (correct, per_label, _) in results.items():
    cells = "".join(f"{f'{per_label[a]}/{per_label_total[a] * RUNS}':>30}" for a in ACTIONS)
    print(f"{name:<24}{cells}{f'{correct}/{len(TEST_SET) * RUNS}':>10}")
