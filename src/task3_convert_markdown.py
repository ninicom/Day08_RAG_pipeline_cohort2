import os
import json
from pathlib import Path
from markitdown import MarkItDown
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

import tempfile
import pypdfium2 as pdfium

def convert_legal():
    try:
        md = MarkItDown(
            llm_client=OpenAI(), 
            llm_model="gpt-4o-mini",
            llm_prompt="You are an OCR system. Transcribe the exact Vietnamese text from this image. Do not describe the image, just output the raw text."
        )
        print("Initialized MarkItDown with GPT-4o Vision for Scanned PDF OCR.")
    except Exception as e:
        print("Cannot initialize OpenAI client for OCR, using standard MarkItDown.")
        md = MarkItDown()
        
    in_dir = Path("data/landing/legal")
    out_dir = Path("data/standardized/legal")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for file_path in in_dir.glob("*.pdf"):
        print(f"Bắt đầu OCR file scan: {file_path.name}")
        
        # Thử đọc trực tiếp trước
        result = md.convert(str(file_path))
        content = result.text_content.strip()
        
        # Nếu PDF là Scanned PDF (không có text), content sẽ trống. Lúc đó ta dùng pdfium để tách ảnh và gọi Vision OCR.
        if not content:
            print(f"[{file_path.name}] Phát hiện Scanned PDF. Tiến hành tách trang thành ảnh và chạy Vision OCR...")
            pdf = pdfium.PdfDocument(str(file_path))
            ocr_text = ""
            # Giới hạn OCR tối đa 3 trang đầu tiên để tiết kiệm thời gian và chi phí API cho các bộ luật khổng lồ
            num_pages = min(3, len(pdf))
            print(f"Sẽ OCR {num_pages} trang đầu tiên...")
            for i in range(num_pages):
                img = pdf[i].render(scale=2).to_pil()
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    img.save(tmp.name)
                    ocr_res = md.convert(tmp.name)
                    # markitdown sinh ra prefix '# Description:\n', ta có thể lấy phần sau đó
                    chunk = ocr_res.text_content.replace("# Description:\n", "").strip()
                    ocr_text += chunk + "\n\n"
                os.unlink(tmp.name)
            content = ocr_text
            
        out_path = out_dir / (file_path.stem + ".md")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Converted {file_path.name}")

def convert_news():
    in_dir = Path("data/landing/news")
    out_dir = Path("data/standardized/news")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for file_path in in_dir.glob("*.json"):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        content = f"# {data.get('title', 'News')}\n\nURL: {data.get('url')}\n\n{data.get('content')}"
            
        out_path = out_dir / (file_path.stem + ".md")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Converted {file_path.name}")

def main():
    convert_legal()
    convert_news()

if __name__ == "__main__":
    main()
