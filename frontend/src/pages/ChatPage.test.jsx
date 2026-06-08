import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ChatPage from './ChatPage';

describe('ChatPage component', () => {
    it('renders the title and input box', () => {
        render(<ChatPage />);
        expect(screen.getByText('RAG Chatbot')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Nhập câu hỏi về luật hoặc tin tức phòng, chống ma túy…')).toBeInTheDocument();
    });

    it('can type in the input box', () => {
        render(<ChatPage />);
        const input = screen.getByPlaceholderText('Nhập câu hỏi về luật hoặc tin tức phòng, chống ma túy…');
        fireEvent.change(input, { target: { value: 'Hello World' } });
        expect(input.value).toBe('Hello World');
    });
});
