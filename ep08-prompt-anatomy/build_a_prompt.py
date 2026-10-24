"""Build a prompt one part at a time and measure what each part fixes.

Same customer message, six prompt versions. Each version runs RUNS times (sampling on),
and every reply is checked automatically, so we compare pass rates, not one lucky answer.
"""

import json
import re

from shared.llm import chat, provider_from_args

provider = provider_from_args()
RUNS = 10

CUSTOMER = "Hi, I ordered 'Dune' last week and it arrived with the cover torn. Can I get a new copy?"
POLICY = (
    "Returns policy: damaged items get a free replacement or a full refund within 30 days of delivery. "
    "We need the order number. Replacements ship in 2-3 working days. No other compensation is offered."
)

ROLE = "You are a customer support agent for Pageturn, an online bookshop."
CONTEXT = f"{POLICY}\n\nCustomer message:\n<message>\n{CUSTOMER}\n</message>"
TASK = "Write a reply to the customer."
CONSTRAINTS = (
    "Rules: under 60 words; warm but professional; offer a replacement or refund; "
    "always ask for the order number; never offer discounts, vouchers or anything not in the policy."
)
EXAMPLE = (
    "Example of a good reply to a different message:\n"
    '{"reply": "I\'m sorry your mug arrived chipped! We can send a free replacement or refund you in full. '
    'Could you share your order number so I can arrange it?", "action": "offer_replacement_or_refund", '
    '"needs_order_number": true}'
)
FORMAT = (
    "Return only JSON, no other text: "
    '{"reply": string, "action": "offer_replacement_or_refund" | "escalate", "needs_order_number": boolean}'
)

FORMAT_CLEAR = (
    "Return only JSON, no other text, with exactly these three keys:\n"
    '- "reply": your reply to the customer (string)\n'
    '- "action": must be exactly "offer_replacement_or_refund" or "escalate"; no other values\n'
    '- "needs_order_number": true or false'
)

VERSIONS = {
    "1 · vague": "Reply to this: " + CUSTOMER,
    "2 · + role + context": f"{ROLE}\n\n{CONTEXT}\n\n{TASK}",
    "3 · + constraints": f"{ROLE}\n\n{CONTEXT}\n\n{TASK}\n{CONSTRAINTS}",
    "4 · + example": f"{ROLE}\n\n{CONTEXT}\n\n{TASK}\n{CONSTRAINTS}\n\n{EXAMPLE}",
    "5 · + output format": f"{ROLE}\n\n{CONTEXT}\n\n{TASK}\n{CONSTRAINTS}\n\n{EXAMPLE}\n\n{FORMAT}",
    "6 · format, rewritten": f"{ROLE}\n\n{CONTEXT}\n\n{TASK}\n{CONSTRAINTS}\n\n{EXAMPLE}\n\n{FORMAT_CLEAR}",
}


def parse_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    try:
        return json.loads(match.group(0)) if match else None
    except json.JSONDecodeError:
        return None


def check(output):
    """Four automatic checks. 'valid JSON' also requires the allowed action values."""
    data = parse_json(output)
    reply = data["reply"] if isinstance(data, dict) and "reply" in data else output
    return {
        "≤60 words": len(reply.split()) <= 60,
        "asks order no.": "order number" in reply.lower() or "order #" in reply.lower(),
        "follows policy": not re.search(r"discount|voucher|coupon|% off|gift card|credit", reply, re.I),
        "valid JSON": isinstance(data, dict)
        and {"reply", "action", "needs_order_number"} <= data.keys()
        and data["action"] in ("offer_replacement_or_refund", "escalate"),
    }


print(f"Provider: {provider} · {RUNS} runs per version\nCustomer: {CUSTOMER}\n")
summary = {}
for name, prompt in VERSIONS.items():
    totals, sample = {}, None
    for _ in range(RUNS):
        output = chat([{"role": "user", "content": prompt}], provider=provider, temperature=0.7, max_tokens=400).text.strip()
        sample = sample or output
        for label, ok in check(output).items():
            totals[label] = totals.get(label, 0) + ok
    summary[name] = totals
    print(f"===== Prompt {name}   ({len(prompt.split())} words) · one sample reply:")
    print(sample[:300] + ("…" if len(sample) > 300 else ""), "\n")

labels = list(next(iter(summary.values())))
print(f"{'pass rate':<24}" + "".join(f"{label:>16}" for label in labels))
for name, totals in summary.items():
    print(f"{name:<24}" + "".join(f"{f'{totals[label]}/{RUNS}':>16}" for label in labels))
