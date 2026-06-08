# PLVN — Trợ lý Pháp luật & Tin tức (RAG Pipeline v2)

Một hệ thống Hỏi - Đáp (Question Answering) dựa trên kiến trúc RAG (Retrieval-Augmented Generation) chuyên sâu về lĩnh vực **Pháp luật và Tin tức phòng, chống ma tuý**. Hệ thống tập trung vào tính minh bạch, mỗi câu trả lời đều được trích dẫn nguồn rõ ràng và kiểm chứng được.

## 🌟 Tính Năng Nổi Bật

- **Hybrid Search + Reranking:** Kết hợp tìm kiếm ngữ nghĩa (Semantic) và từ khóa (Lexical - BM25), sau đó đánh giá lại độ ưu tiên (Rerank) bằng mô hình Cross-Encoder để có kết quả chính xác nhất.
- **Vectorless Fallback (PageIndex):** Tự động chuyển đổi sang phương thức tìm kiếm không cần vector khi kết quả hybrid search không đạt ngưỡng tin cậy.
- **Trích dẫn minh bạch (Detailed Citations):** LLM sinh câu trả lời kèm trích dẫn gốc. Giao diện frontend hỗ trợ hiển thị đoạn text gốc, điểm số relevance và tự động tô sáng (highlight) từ khóa của người dùng.
- **Giao diện hiện đại (React/Vite):** Frontend thân thiện, hỗ trợ thao tác tinh chỉnh thông số truy xuất (Top-K, Threshold, Search Mode, HyDE) theo thời gian thực.
- **Conversation Memory:** Duy trì ngữ cảnh hội thoại đa lượt.

## 📁 Cấu Trúc Dự Án

```text
day_08_rag_pipeline_v2/
├── frontend/             ← Giao diện người dùng (React, Vite)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/        ← Chứa ChatPage.jsx (Giao diện chính)
│   │   └── config/
│   └── package.json
├── data/
│   ├── landing/          ← Dữ liệu thô (PDF, DOCX, HTML, JSON)
│   └── standardized/     ← Dữ liệu đã được chuyển đổi sang Markdown
├── src/                  ← Backend & Data Pipeline
│   ├── task1_collect_legal_docs.py
│   ├── task2_crawl_news.py
│   ├── task3_convert_markdown.py
│   ├── task4_chunking_indexing.py
│   ├── task5_semantic_search.py
│   ├── task6_lexical_search.py
│   ├── task7_reranking.py
│   ├── task8_pageindex_vectorless.py
│   ├── task9_retrieval_pipeline.py
│   └── task10_generation.py
├── chroma_db/            ← Cơ sở dữ liệu Vector cục bộ
├── notebooks/            ← Notebook demo 
└── requirements.txt
```

## 🚀 Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Cài đặt Backend (Data Pipeline)
Yêu cầu: Python 3.10+

```bash
# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Copy file môi trường và điền API keys của bạn (nếu có dùng API ngoài như OpenAI, Jina)
cp .env.example .env
```

Để chạy pipeline xử lý dữ liệu từ đầu (Thu thập -> Markdown -> Chunking -> Indexing):
```bash
python src/task1_collect_legal_docs.py
python src/task2_crawl_news.py
python src/task3_convert_markdown.py
python src/task4_chunking_indexing.py
```

### 2. Khởi chạy Frontend
Yêu cầu: Node.js 18+

```bash
cd frontend
npm install

# Khởi chạy server phát triển
npm run dev
```
Trình duyệt sẽ tự động mở giao diện tại `http://localhost:5173`.

## 🛠 Công Nghệ Sử Dụng

- **Backend & Pipeline:** Python, LangChain, Weaviate / ChromaDB, BM25 (rank_bm25), MarkItDown, Crawl4AI.
- **AI Models:** 
  - Embedding: `sentence-transformers/all-MiniLM-L6-v2` hoặc BAAI/bge-m3.
  - Reranker: `jina-reranker-v2-base-multilingual` / Qwen Reranker.
- **Frontend:** React.js, Vite, Lucide React, Vanilla CSS.

## 📝 Đánh Giá (Evaluation)
Dự án có hỗ trợ framework đánh giá RAG (RAGAS / DeepEval / TruLens) nằm trong bài tập nhóm `group_project/README.md`. Nhóm tiến hành tạo Golden Dataset và chạy benchmark các trục: *Faithfulness, Answer Relevance, Context Recall, Context Precision*.

---
*Dự án nằm trong khuôn khổ chương trình RAG Pipeline Cohort 2.*
