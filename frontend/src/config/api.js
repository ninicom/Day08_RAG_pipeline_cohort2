export const API_BASE = "http://localhost:8000";

// Normalize SourceChunk từ backend → format frontend dùng
const normalizeSource = (chunk, idx) => ({
    id: idx + 1,
    content: chunk.content,
    score: chunk.score,
    metadata: {
        source: chunk.metadata?.source || chunk.source || "unknown",
        type: chunk.metadata?.type || chunk.source || "hybrid",
        ...chunk.metadata,
    },
});

export const realChat = async (query, sessionId = null, topK = 5, useHyDE = false, useRerank = true, threshold = 0.5, searchMode = "Hybrid kết hợp") => {
    const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            query: query,
            sessionId: sessionId,
            useHyDE: useHyDE,
            useReranking: useRerank,
            topK: Number(topK),
            threshold: Number(threshold),
            searchMode: searchMode
        }),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
    }
    const data = await res.json();
    return {
        answer: data.answer,
        session_id: data.session_id,
        sources: data.sources.map(normalizeSource),
    };
};

export const realRetrieval = async (query, method = "Hybrid", topK = 5, threshold = 0.3) => {
    const res = await fetch(`${API_BASE}/api/retrieval`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, method, topK: Number(topK), threshold: Number(threshold) }),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
    }
    const data = await res.json();
    return { results: data.results.map(normalizeSource) };
};

export const checkHealth = async () => {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
};

export const realEvaluation = async (deepevalKey, openaiKey) => {
    const headers = { "Accept": "application/json" };
    if (deepevalKey) headers["X-DeepEval-Key"] = deepevalKey;
    if (openaiKey) headers["X-OpenAI-Key"] = openaiKey;
    
    const res = await fetch(`${API_BASE}/api/evaluation`, {
        method: "GET",
        headers: headers
    });
    
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return res.json();
};

export const realUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    
    const res = await fetch(`${API_BASE}/api/upload`, {
        method: "POST",
        body: formData
    });
    
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return res.json();
};

export const getSystemStats = async () => {
    const res = await fetch(`${API_BASE}/api/stats`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
};
