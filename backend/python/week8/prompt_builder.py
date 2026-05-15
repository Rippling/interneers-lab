# bridge between retieval and LLM answer generation

# this file takes user question and retrievd chunks and combines them into one final prompt string that will be sent to gemini


def build_context_blocks(retrieved_chunks):
    context_parts = []
    for index, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"""Source #{index}
Title: {chunk.get("title", "Unknown")}
Source File: {chunk.get("source", "unknown")}
Document Type: {chunk.get("doc_type", "unknown")}
Chunk Index: {chunk.get("chunk_index", -1)}
Content:
{chunk.get("text", "")}
"""
        )

    return "\n" + ("\n" + "-" * 80 + "\n").join(context_parts)


def build_rag_prompt(user_query, retrieved_chunks):
    context_block = build_context_blocks(retrieved_chunks)
    prompt = f"""
You are an inventory support assistant for a toy store.

Answer the user's question only from the provided context.
Do not make up facts.
Do not use outside knowledge.
If the answer is not clearly present in the context, say:
"I could not find that information in the provided documents."

Be clear, concise, and helpful.
If multiple sources support the answer, combine them carefully.
If relevant, mention the source title in your answer.

User Question:
{user_query}

Retrieved Context:
{context_block}

Final Answer:
"""
    return prompt.strip()
