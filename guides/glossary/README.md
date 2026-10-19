# GenAI glossary

Plain-English definitions of the terms used in this series, with links to where each one is explained properly.

> **Draft** · Grows with every episode · Terms are grouped by topic, alphabetical within each group.

## Models

| Term | Meaning |
| --- | --- |
| **Base model** | A model trained only to continue text; not yet tuned to follow instructions. ([Ep 3](../../ep03-how-llms-work/)) |
| **Closed model** | Used only through the provider's API; you never get the weights. ([Ep 6](../../ep06-model-landscape/)) |
| **Fine-tuning** | Further training a model on your own examples to change its behaviour. (Module 5) |
| **Foundation model** | A large, general model trained on broad data that you build on top of. ([Ep 1](../../ep01-what-is-genai-engineering/)) |
| **Hallucination** | A confident answer that's wrong or made up, because the model produces plausible text, not looked-up facts. ([Ep 3](../../ep03-how-llms-work/)) |
| **Inference** | Running a trained model to get an output (as opposed to training it). |
| **LLM** | Large language model: a model that predicts the next token, trained on huge amounts of text. |
| **Multimodal** | Handles more than text: images, audio or video, as input or output. (Module 6) |
| **Open-weight model** | You can download the trained weights and run it yourself. Not always fully "open source". ([Ep 6](../../ep06-model-landscape/)) |
| **Parameters / weights** | The billions of numbers learned in training. "7B" = about 7 billion parameters. |
| **Quantization** | Storing weights with fewer bits (e.g. 4-bit) so a model uses less memory, with a small quality cost. ([Ollama guide](../ollama/)) |
| **Reasoning / thinking model** | A model that spends extra (often hidden) tokens thinking before it answers. ([Ep 4](../../ep04-tokens-and-context-windows/)) |
| **Tier** | The size level within a model family: largest, balanced, smallest. ([Ep 6](../../ep06-model-landscape/)) |
| **Transformer** | The neural-network design behind LLMs: layers of attention and feed-forward blocks. ([Ep 3](../../ep03-how-llms-work/)) |

## How LLMs work

| Term | Meaning |
| --- | --- |
| **Attention** | Lets each token look back at earlier tokens and update its meaning from context. ([Ep 3](../../ep03-how-llms-work/)) |
| **Autoregressive generation** | Producing output one token at a time, each added to the input for the next. ([Ep 3](../../ep03-how-llms-work/)) |
| **Context window** | The maximum tokens a model handles in one request, input and output together. ([Ep 4](../../ep04-tokens-and-context-windows/)) |
| **Embedding** | A list of numbers representing meaning; similar meanings get similar numbers. ([Ep 3](../../ep03-how-llms-work/)) |
| **Logprobs** | The model's log-probabilities for candidate next tokens. ([Ep 3](../../ep03-how-llms-work/)) |
| **Token** | A chunk of text (often part of a word) that models read and write; the unit of cost. ([Ep 4](../../ep04-tokens-and-context-windows/)) |
| **Tokenizer** | Splits text into tokens; each model family has its own. ([Ep 4](../../ep04-tokens-and-context-windows/)) |
| **Vocabulary** | All the tokens a model knows, usually 100k–250k. |

## Controlling output

| Term | Meaning |
| --- | --- |
| **Finish / stop reason** | Why generation ended: natural end, max tokens or a stop sequence. ([Ep 5](../../ep05-sampling-parameters/)) |
| **Greedy decoding** | Always picking the most likely token (temperature 0). ([Ep 5](../../ep05-sampling-parameters/)) |
| **Max tokens** | A hard cap on output length. ([Ep 5](../../ep05-sampling-parameters/)) |
| **Seed** | Makes the random choices repeatable, where supported. ([Ep 5](../../ep05-sampling-parameters/)) |
| **Stop sequence** | Text that ends generation as soon as it appears. ([Ep 5](../../ep05-sampling-parameters/)) |
| **Structured output** | Making the model return data in a fixed format, like JSON matching a schema. (Module 2) |
| **System prompt** | Instructions that set the model's role and rules for a conversation. (Ep 7) |
| **Temperature** | How sharp or flat the next-token odds are: low = focused, high = varied. ([Ep 5](../../ep05-sampling-parameters/)) |
| **Top-p / top-k** | Limit sampling to the most likely tokens. ([Ep 5](../../ep05-sampling-parameters/)) |

## Prompting

| Term | Meaning |
| --- | --- |
| **Chain-of-thought** | Asking the model to reason step by step before answering. (Module 2) |
| **Few-shot** | Including a few worked examples in the prompt. (Module 2) |
| **Prompt injection** | Untrusted text tricking a model into ignoring its instructions. (Module 2) |
| **Zero-shot** | Asking without any examples. (Module 2) |

## Retrieval and data

| Term | Meaning |
| --- | --- |
| **Chunking** | Splitting documents into pieces small enough to embed and retrieve. (Module 3) |
| **Cosine similarity** | A score for how closely two embeddings point the same way. ([Ep 3](../../ep03-how-llms-work/)) |
| **Grounding** | Making answers rely on provided sources instead of the model's memory. (Module 4) |
| **Hybrid search** | Combining keyword search (like BM25) with vector search. (Module 4) |
| **RAG** | Retrieval-augmented generation: fetch relevant data, put it in the prompt, then answer. (Module 4) |
| **Re-ranking** | Re-ordering retrieved results with a stronger model before using them. (Module 4) |
| **Vector database** | Stores embeddings and finds the nearest ones fast. ([guide](../vector-databases/), Module 3) |

## Agents and tools

| Term | Meaning |
| --- | --- |
| **Agent** | An LLM in a loop that decides which tools to call to reach a goal. (Module 7) |
| **Guardrails** | Checks around a model to block unsafe inputs, outputs or actions. (Modules 8, 10) |
| **MCP** | Model Context Protocol: a standard way to connect models to tools and data. ([guide](../mcp/), Module 8) |
| **Tool / function calling** | The model asks your code to run a function and uses the result. (Module 7) |

## Evaluation and production

| Term | Meaning |
| --- | --- |
| **Eval** | A repeatable test of model quality on a set of examples. (Module 9) |
| **LLM-as-judge** | Using a model to grade another model's outputs. (Module 9) |
| **Latency / TTFT** | Total response time / time to first token. ([Ep 4](../../ep04-tokens-and-context-windows/)) |
| **Prompt caching** | Reusing processed input across requests to cut cost and latency. (Module 10) |
| **Rate limit** | A cap on requests or tokens per minute or day. ([guide](../api-errors/)) |
| **Tracing** | Recording every step of an LLM app (prompts, tool calls, tokens, time). ([guide](../tracing/), Module 9) |
