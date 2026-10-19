# Vector databases quickstart

Store embeddings and find the most similar ones: the core of semantic search and RAG. Quick starts for Chroma (local, zero setup) and pgvector (PostgreSQL).

> **Draft** · Preview of Module 3 (Embeddings & Vector Databases) · Code follows the libraries' documented APIs; it will be run and finalised in Module 3.

## What a vector database does

```text
documents ──embed──▶ vectors ──store──▶ vector DB
question  ──embed──▶ vector  ──search─▶ "the 5 nearest vectors" ──▶ their documents
```

It's a database whose main query is **"find the stored items closest in meaning to this one"**, using similarity measures like cosine similarity ([Episode 3](../../ep03-how-llms-work/)).

## Which one?

| Option | Best for | Setup |
| --- | --- | --- |
| **Chroma** | Learning, prototypes, small apps | `uv add chromadb`, no server needed |
| **pgvector** | You already use PostgreSQL; production with SQL | A Postgres extension (Docker or managed) |
| **FAISS** | Fast in-memory search inside one Python process | A library, not a database |
| **Pinecone** | Fully managed, scale without running servers | Cloud account |
| **OpenSearch** | Search + vectors together; AWS-friendly | Managed service or cluster |

## Chroma in 10 lines

```python
import chromadb

client = chromadb.PersistentClient(path="chroma_data")      # saved to disk
docs = client.get_or_create_collection("course_notes")

docs.add(
    ids=["ep3", "ep4", "ep5"],
    documents=[
        "Embeddings turn tokens into vectors of meaning.",
        "The context window holds input and output tokens.",
        "Temperature reshapes the next-token odds.",
    ],
)

results = docs.query(query_texts=["How much text can a model see at once?"], n_results=1)
print(results["documents"][0])     # ['The context window holds input and output tokens.']
```

Chroma embeds the text for you with a small default model. To use your own embeddings (e.g. Gemini's), pass `embeddings=[...]` to `add` and `query_embeddings=[...]` to `query`.

## pgvector quick start

Run PostgreSQL with pgvector in Docker:

```bash
docker run -d --name pgvector -e POSTGRES_PASSWORD=dev -p 5432:5432 pgvector/pgvector:pg17
```

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE notes (
  id        serial PRIMARY KEY,
  content   text,
  embedding vector(768)          -- must match your embedding size
);

-- nearest 5 by cosine distance (<=> operator)
SELECT content FROM notes ORDER BY embedding <=> '[0.01, -0.02, ...]' LIMIT 5;

-- an index for speed once you have lots of rows
CREATE INDEX ON notes USING hnsw (embedding vector_cosine_ops);
```

> **Dimension gotcha:** `gemini-embedding-001` returns **3,072** numbers by default ([Episode 3](../../ep03-how-llms-work/)), but pgvector's HNSW index on the standard `vector` type supports up to **2,000** dimensions. Ask the embedding API for fewer dimensions (e.g. 768), or use pgvector's `halfvec` type.

## Things that matter more than the database

- **Chunking:** how you split documents decides what can be found (Module 3).
- **The same embedding model** must be used for documents and questions.
- **Metadata filters** (source, date, user) narrow results before similarity search.
- **Evaluate retrieval:** does the right chunk come back for real questions? (Module 4)
