import { describe, it, expect, vi, beforeEach } from 'vitest';
import { realChat } from './api';

describe('API functions', () => {
    beforeEach(() => {
        global.fetch = vi.fn();
    });

    it('realChat should call /api/chat with correct payload', async () => {
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ answer: 'Test answer', session_id: '123', sources: [] })
        });

        const result = await realChat('Hello', '123', 5, true, false, 0.5, 'Hybrid');

        expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/chat', expect.objectContaining({
            method: 'POST',
            body: JSON.stringify({
                query: 'Hello',
                sessionId: '123',
                useHyDE: true,
                useReranking: false,
                topK: 5,
                threshold: 0.5,
                searchMode: 'Hybrid'
            })
        }));

        expect(result.answer).toBe('Test answer');
        expect(result.session_id).toBe('123');
    });
});
