"""Turn the winning prompt into a reusable template, then test it on messages it has never seen."""

import json
import re
from dataclasses import dataclass

from shared.llm import chat, provider_from_args


@dataclass
class Prompt:
    """The six parts of a prompt, kept separate so each one can be changed and tested on its own."""

    role: str
    context: str
    task: str
    constraints: str
    examples: str
    output_format: str

    def render(self, **values):
        parts = [self.role, self.context, self.task, self.constraints, self.examples, self.output_format]
        return "\n\n".join(part.format(**values) for part in parts if part)


SUPPORT_REPLY = Prompt(
    role="You are a customer support agent for Pageturn, an online bookshop.",
    context=(
        "Returns policy: damaged or wrong items get a free replacement or a full refund within 30 days of delivery. "
        "Late orders: apologise and give the tracking link; no compensation. We need the order number for any action.\n\n"
        "Customer message:\n<message>\n{message}\n</message>"
    ),
    task="Write a reply to the customer.",
    constraints=(
        "Rules: under 60 words; warm but professional; always ask for the order number; "
        "never offer discounts, vouchers or anything not in the policy."
    ),
    examples=(
        "Example of a good reply to a different message:\n"
        '{{"reply": "I\'m sorry your mug arrived chipped! We can send a free replacement or refund you in full. '
        'Could you share your order number so I can arrange it?", "action": "offer_replacement_or_refund", '
        '"needs_order_number": true}}'
    ),
    output_format=(
        "Return only JSON, no other text, with exactly these three keys:\n"
        '- "reply": your reply to the customer (string)\n'
        '- "action": must be exactly "offer_replacement_or_refund", "send_tracking" or "escalate"; no other values\n'
        '- "needs_order_number": true or false'
    ),
)

MESSAGES = [  # (customer message, the action the policy says is right)
    ("The book I received is 'Emma', but I ordered 'Dune'.", "offer_replacement_or_refund"),
    ("My order was due on Monday and it still hasn't arrived.", "send_tracking"),
    ("Two pages in my cookbook are stuck together and torn.", "offer_replacement_or_refund"),
    ("This is the third time you've messed up. I want a 50% discount NOW.", "escalate"),
]


def parse(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    try:
        return json.loads(match.group(0)) if match else None
    except json.JSONDecodeError:
        return None


provider = provider_from_args()
print(f"Provider: {provider}\n")
print("The rendered prompt for the first message:\n" + "-" * 60)
print(SUPPORT_REPLY.render(message=MESSAGES[0][0]))
print("-" * 60 + "\n")

format_ok = action_ok = 0
for message, expected in MESSAGES:
    raw = chat([{"role": "user", "content": SUPPORT_REPLY.render(message=message)}],
               provider=provider, temperature=0.7, max_tokens=300).text
    data = parse(raw)
    valid = (isinstance(data, dict) and {"reply", "action", "needs_order_number"} <= data.keys()
             and data["action"] in ("offer_replacement_or_refund", "send_tracking", "escalate"))
    right_action = valid and data["action"] == expected
    format_ok += valid
    action_ok += right_action
    print(f"Customer: {message}")
    if valid:
        print(f"  action: {data['action']}   reply: {data['reply']}")
    else:
        print(f"  raw output: {raw.strip()[:160]}")
    print(f"  {'✓' if valid else '✗'} valid JSON   {'✓' if right_action else '✗'} right action (expected {expected})\n")

print(f"Valid format: {format_ok}/{len(MESSAGES)}   Right decision: {action_ok}/{len(MESSAGES)}")
print("A perfect format can still hide a wrong decision: check what actually matters.")
