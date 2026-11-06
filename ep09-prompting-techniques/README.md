# Episode 09: Zero-shot, Few-shot and Chain-of-Thought

When examples help, how to choose them, and when to ask the model to think step by step — all measured, not guessed.

> **Module 2: Prompt Engineering** · Episode 9 of 42 · [Slides](https://amitpnk.github.io/genai-zero-to-production/ep09-prompting-techniques/)

## What you'll learn

- What **zero-shot**, **few-shot** and **chain-of-thought** prompting mean
- Why **any examples** can help a lot, and why **which examples** you pick is something to test, not guess
- How to spot a biased prompt with **accuracy per label**, not just overall accuracy
- When **"think step by step"** helps, and what it **costs** in tokens and time
- How **reasoning ("thinking") models** change the picture

---

## 1. The big idea

> **Examples and step-by-step thinking are tools, not magic.** Each one can help a lot, do nothing, or make things worse. The only way to know is to measure it on your model and your data.

[Episode 8](../ep08-prompt-anatomy/) ended with a support bot that chose the same action for almost every message, because its one example used that action. This episode tests the fix.

## 2. Three techniques

| Technique | What you give the model | Good for |
| --- | --- | --- |
| **Zero-shot** | Instructions only, no examples | Simple tasks; strong models; quick first try |
| **Few-shot** | Instructions + a few worked examples (input → right output) | Teaching a format, a style, or labels the model can't guess |
| **Chain-of-thought (CoT)** | Ask the model to reason step by step before answering | Maths, logic, multi-step rules |

"Shot" just means "example". One-shot is one example; few-shot is usually 2–8.

## 3. Few-shot: which examples help?

The demo: the same bookshop from Episode 8. [`few_shot.py`](few_shot.py) sorts **12 customer messages** into one of three actions: `offer_replacement_or_refund`, `send_tracking` or `escalate`. Every prompt version has the same instructions and policy; only the examples change. Each version runs **5 times per message** (60 answers), and the examples are never taken from the test messages.

| Version | Examples |
| --- | --- |
| Zero-shot | none |
| One-shot (Ep 8) | 1 × replacement |
| Few-shot, same label | 3 × replacement |
| Few-shot, 1 per action | 1 replacement, 1 tracking, 1 escalate |
| Few-shot, + tricky one | the 3 above + "damaged **and** wants a gift card → escalate" |

Real results (`gemma3:1b`, local, 5 runs per message):

| Version | Replacement (20) | Tracking (20) | Escalate (20) | **Overall (60)** |
| --- | ---: | ---: | ---: | ---: |
| Zero-shot | 20/20 | 0/20 | 5/20 | **25/60** |
| One-shot (Ep 8) | 20/20 | 10/20 | 10/20 | **40/60** |
| Few-shot, same label | 20/20 | 19/20 | 13/20 | **52/60** |
| Few-shot, 1 per action | 20/20 | 4/20 | 5/20 | **29/60** |
| Few-shot, + tricky one | 20/20 | 12/20 | 5/20 | **37/60** |

**What we learned:**

1. **Zero-shot** picked "replacement" 55 times out of 60, and never chose tracking. A small model falls back to the most obvious label.
2. **Examples help**: even Episode 8's single example took it from 25/60 to 40/60 — but not in the way the usual tip says.
3. The usual advice is *"show one example of each label"*. On this model, that was the **worst** few-shot version (29/60) — worse than one single example (40/60). It still picked "replacement" 51 times out of 60.
4. **Three examples of the same label scored best.** We don't fully know why. Small models react to examples in ways that are hard to predict.
5. Adding one **tricky example** (a case on the line between two labels) helped compared to one-per-action.

> **Which examples you choose is a setting you tune and test, like temperature.** Don't trust a tip — including this one — until you've measured it on your model.

### Look at accuracy per label

The overall score hides *where* it fails. Every version gets "replacement" right 20/20, so a test set full of damaged-book messages would make every prompt look perfect. **Split accuracy by the right answer** and the bias is obvious.

### Why we re-ran it

The first 3-run test showed the same surprise. Before believing it, we ran it again with 5 runs, and added the "1 per action" version to check whether the tricky example was the cause. It wasn't. **When a result surprises you, re-run it before you build a story on it.**

## 4. How to choose few-shot examples

- **Use real inputs**, like the messages you'll actually get — not made-up perfect ones.
- **Keep examples out of your test set**, or your score is fake.
- **Cover the hard cases**: messages on the line between two labels teach more than easy ones.
- **Watch for copying**: if most answers match your examples' labels, the model is copying, not deciding.
- **Order can matter**: the last example often has the biggest pull. Try shuffling.
- **Test several sets** and keep the one with the best per-label scores.

## 5. Chain-of-thought: does "think step by step" help?

[`chain_of_thought.py`](chain_of_thought.py) asks **8 small bookshop maths problems** (discounts, free shipping over £40, refunds, "every 4th notebook free"). Each has one right number. Two styles:

- **Direct:** "Answer with only the final number."
- **Step by step:** "Think step by step and show your working. Then write the final answer on the last line as: Answer: &lt;number&gt;"

Real results (`gemma3:1b`, local, 3 runs per problem):

| Style | Accuracy | Avg output tokens | Avg time per answer |
| --- | ---: | ---: | ---: |
| Direct | **0/24** | 3 | 2.7 s |
| Step by step | **16/24** | 128 | 9.8 s |

From **0/24 to 16/24** — just by letting the model write its working first. Remember [Episode 3](../ep03-how-llms-work/): the model writes one token at a time. Asked for only a number, it must guess the answer in one token. Given room to write steps, each step becomes context for the next.

But look at the cost: **about 40× more output tokens** and **3–4× slower**. Output tokens are the expensive ones ([Episode 4](../ep04-tokens-and-context-windows/)).

> **Use chain-of-thought when the task has steps.** For a simple label, like the few-shot task above, it just adds cost and delay.

### Tips for chain-of-thought

- Ask for the **final answer in a fixed place** ("Answer: …" on the last line) so your code can find it.
- **Don't show the working to end users** unless it helps them. Store it for debugging.
- **Check the answer, not the working.** Good-looking steps can still end in a wrong number.

## 6. Reasoning ("thinking") models

Many newer models, including recent Gemini, Claude and OpenAI models, can **think before they answer** on their own. They do a hidden chain-of-thought and you're billed for those thinking tokens (`shared/llm.py` adds them to `output_tokens`).

- With these models, "think step by step" in the prompt usually adds **less**: they already do it.
- You often control thinking with a **setting** (a thinking budget or effort level) instead of prompt words.
- The trade-off is the same: **more thinking = better on hard tasks, but more tokens and slower.**

## 7. Which technique when?

| Situation | Start with |
| --- | --- |
| Simple, clear task; strong model | Zero-shot |
| Need a specific format, style or label set | Few-shot (and test which examples) |
| Maths, logic, multi-step rules | Chain-of-thought, or a reasoning model |
| Simple label at high volume, cost matters | Zero- or few-shot, no CoT |
| Still failing after all of this | Better context (RAG, Module 4) or fine-tuning (Module 5) |

---

## Run the demos

From the repo root (`--provider ollama` is the default, or `--provider gemini`):

```bash
uv run python ep09-prompting-techniques/few_shot.py           # 5 versions × 12 messages × 5 runs; ~25 min locally
uv run python ep09-prompting-techniques/chain_of_thought.py   # 2 styles × 8 problems × 3 runs; ~6 min locally
```

> These use [`shared/llm.py`](../shared/llm.py) from Episode 7. Your numbers will be different: that's sampling. A bigger model (Gemini) will usually score higher, and **the best examples for it may be different** — which is the whole point. Run it and compare.

---

## Interview question (FDE)

> **"When would you use few-shot prompting, chain-of-thought, or fine-tuning?"**

**A strong answer:**

> "I'd start zero-shot with clear instructions, and build a test set with automatic checks so I can measure. If the model gets the format or labels wrong, I'd add few-shot examples taken from real data — and test a few different sets, checking accuracy per label so I can see if it's just copying the examples. If the task has steps, like calculations or applying several rules, I'd add chain-of-thought or use a reasoning model, but only where it pays off, because it costs many more output tokens and adds delay. Fine-tuning comes last: when prompting has hit its limit, the task is high-volume and narrow, and I have hundreds of good labelled examples. And if the problem is missing knowledge, not behaviour, the answer is retrieval, not fine-tuning."

Practise it: say it out loud in your own words before moving on.

## Recap

- **Zero-shot** = instructions only. **Few-shot** = add examples. **Chain-of-thought** = reason before answering.
- **Examples help**, but which ones is something to **test**. On our model, the textbook "one per label" lost.
- **Check accuracy per label** to catch a biased prompt.
- **Chain-of-thought** took maths from **0/24 to 16/24**, at **~40× the output tokens**.
- **Reasoning models** think on their own; you tune a setting, and still pay for the tokens.

## Next up

**Episode 10: Structured outputs.** JSON mode, schemas with Pydantic, and validation with retries — so your code can trust the shape of every answer.
