"""Chain-of-thought: does "think step by step" help, and what does it cost?

Eight small bookshop maths problems, each with one right number. We ask for the answer
directly, then ask the model to reason first, and compare accuracy, output tokens and time.
"""

import re
import time

from shared.llm import chat, provider_from_args

provider = provider_from_args()
RUNS = 3

PROBLEMS = [  # (question, right answer)
    (
        (
            "A customer buys 3 books at £8 each and 2 books at £12 each. Shipping is £4, but free for orders over £40. "
            "One £12 book arrives damaged and is refunded. How much has the customer paid in total after the refund?"
        ),
        36,
    ),
    (
        (
            "A box set costs £45. Members get 20% off. Shipping is £5, but free if the price after discount is £40 or more. "
            "A member buys one box set. How much do they pay in total?"
        ),
        41,
    ),
    (
        (
            "A customer orders 4 paperbacks at £7 each, uses a £5 voucher, and pays £3 shipping. How much do they pay?"
        ),
        26,
    ),
    (
        (
            "A shop has 120 copies of a book. It sells 45 on Monday, receives a delivery of 35 on Tuesday, "
            "and sells half of its stock on Wednesday. How many copies are left?"
        ),
        55,
    ),
    (
        (
            "A reader reads 25 pages a day on weekdays and 40 pages a day at weekends. "
            "Starting on a Monday, how many pages do they read in one full week?"
        ),
        205,
    ),
    (
        (
            "Three friends buy 5 books at £9 each and pay £6 shipping. They split the total equally. "
            "How much does each friend pay?"
        ),
        17,
    ),
    (
        (
            "A customer returns 2 of the 6 books they bought. Every book cost £10. "
            "The shop refunds the returned books but keeps a £2 fee for each returned book. How much is the refund?"
        ),
        16,
    ),
    (
        (
            "Notebooks cost £3 each, and every 4th notebook is free. A customer takes 10 notebooks. "
            "How much do they pay?"
        ),
        24,
    ),
]

STYLES = {
    "direct": "Answer with only the final number, no words, no working.",
    "step by step": "Think step by step and show your working. "
                    "Then write the final answer on the last line as: Answer: <number>",
}


def parse_number(text, style):
    text = text.replace(",", "")
    if style == "step by step":
        match = re.search(r"answer\W*£?\s*(-?\d+(?:\.\d+)?)", text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)
    if not numbers:
        return None
    return float(numbers[0] if style == "direct" else numbers[-1])


print(f"Provider: {provider} · {len(PROBLEMS)} problems × {RUNS} runs per style\n")
summary = {}
for style, instruction in STYLES.items():
    correct, tokens, seconds, sample = 0, 0, 0.0, None
    for question, answer in PROBLEMS:
        for _ in range(RUNS):
            start = time.perf_counter()
            reply = chat([{"role": "user", "content": f"{question}\n\n{instruction}"}],
                         provider=provider, temperature=0.7, max_tokens=800)
            seconds += time.perf_counter() - start
            tokens += reply.output_tokens
            correct += parse_number(reply.text, style) == answer
            sample = sample or reply.text.strip()
    calls = len(PROBLEMS) * RUNS
    summary[style] = (correct, calls, tokens / calls, seconds / calls)
    print(f"===== {style} · one sample reply (problem 1, right answer {PROBLEMS[0][1]}):")
    print(sample[:500] + ("…" if len(sample) > 500 else ""), "\n")

print(f"{'style':<16}{'accuracy':>12}{'avg output tokens':>20}{'avg seconds':>14}")
for style, (correct, calls, avg_tokens, avg_seconds) in summary.items():
    print(f"{style:<16}{f'{correct}/{calls}':>12}{avg_tokens:>20.0f}{avg_seconds:>14.1f}")
