"""Why long chats get expensive: every turn resends the whole conversation. Runs locally."""

import tiktoken

enc = tiktoken.get_encoding("o200k_base")
count = lambda text: len(enc.encode(text))

# EXAMPLE price in US$ per 1 million input tokens, just to show the maths.
PRICE_IN = 0.50

system = "You are a helpful travel assistant. Answer clearly and briefly."
user_msg = "Can you suggest a few things to do in Lisbon this weekend, with rough costs?"
assistant_msg = (
    "Sure! Visit Belém Tower and Jerónimos Monastery (about 10-15 euros each), ride Tram 28 "
    "through Alfama (3 euros), watch sunset at Miradouro da Senhora do Monte (free), and try "
    "pastéis de nata at a local bakery (1-2 euros each). Want restaurant ideas too?"
)

history = count(system)
total_sent = 0
print(f"{'Turn':>4} {'input tokens sent':>18} {'running total':>14}")
for turn in range(1, 11):
    history += count(user_msg)          # the new question joins the history
    sent = history                      # the WHOLE history is sent as input
    total_sent += sent
    print(f"{turn:>4} {sent:>18,} {total_sent:>14,}  {'#' * (sent // 60)}")
    history += count(assistant_msg)     # the reply joins the history too

print(f"\n10 turns sent {total_sent:,} input tokens, though each new message is only ~{count(user_msg)}.")
print(f"Example input cost: ${total_sent * PRICE_IN / 1_000_000:.4f}  (x every user, every day)")
