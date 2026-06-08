import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """Answer the following question comprehensively.
For every statement of fact or claim, immediately insert a citation
in brackets linking to the specific source (e.g., [Author/Platform Name]).
IMPORTANT: Do NOT hallucinate or guess publication years. Only include the year if it is explicitly written in the provided context.
If the information is not explicitly stated in the provided context
or knowledge base, state 'I cannot verify this information'
rather than guessing."""

def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    chunks = sorted(chunks, key=lambda x: x.get("score", 0), reverse=True)
    if not chunks:
        return []
    result = [None] * len(chunks)
    left = 0
    right = len(chunks) - 1
    for i, chunk in enumerate(chunks):
        if i % 2 == 0:
            result[left] = chunk
            left += 1
        else:
            result[right] = chunk
            right -= 1
    return result

def format_context(chunks: list[dict]) -> str:
    ctx = []
    for c in chunks:
        source = c.get("metadata", {}).get("source", "unknown")
        ctx.append(f"Source: {source}\n{c.get('content', '')}")
    return "\n\n---\n\n".join(ctx)

def generate_hyde_document(query: str, history: list[dict] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "dummy"))
    
    messages = [
        {"role": "system", "content": "You are a legal and news expert. Write a detailed, hypothetical document that perfectly answers the user's question. Do not state that you are an AI. Just provide the text of the hypothetical document."}
    ]
    if history:
        messages.extend(history[-4:])
    messages.append({"role": "user", "content": query})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            top_p=0.9
        )
        return response.choices[0].message.content
    except Exception:
        return query

def generate_with_citation(query: str, context_chunks: list[dict] = None, history: list[dict] = None) -> dict:
    if context_chunks is None:
        context_chunks = []
        
    reordered = reorder_for_llm(context_chunks)
    context_str = format_context(reordered)
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "dummy"))
    
    prompt = f"Context:\n{context_str}\n\nQuestion: {query}"
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.0,
            top_p=0.1
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"I cannot verify this information. (API Error: {e})"
        
    return {"answer": answer}
