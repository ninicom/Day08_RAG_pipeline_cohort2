import os
import json
from pathlib import Path

def generate_mock_article(url: str, output_path: str, title: str):
    content = f"# {title}\n\n"
    content += "Đây là nội dung chi tiết bài báo viết về vấn đề nghệ sĩ liên quan đến ma túy. " * 30
    
    data = {
        "url": url,
        "title": title,
        "content": content
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    out_dir = Path("data/landing/news")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    articles = [
        ("https://vnexpress.net/ca-si-chi-dan-bi-dieu-tra-lien-quan-ma-tuy-4813959.html", "Ca sĩ Chi Dân bị điều tra liên quan ma túy"),
        ("https://dantri.com.vn/phap-luat/nhieu-nghe-si-vuong-lao-ly-vi-ma-tuy-bai-hoc-dat-gia-cho-su-sa-nga-20241110.htm", "Nhiều nghệ sĩ vướng lao lý vì ma túy"),
        ("https://thanhnien.vn/nhung-nghe-si-viet-tieu-tan-su-nghiep-vi-ma-tuy-185240608.htm", "Những nghệ sĩ Việt tiêu tan sự nghiệp vì ma túy"),
        ("https://tuoitre.vn/ca-si-chi-dan-an-tay-ngoc-thanh-bi-bat-giam-vi-ma-tuy-20241114.htm", "Ca sĩ Chi Dân, An Tây bị bắt vì ma túy"),
        ("https://vietnamnet.vn/nhung-nghe-si-viet-danh-mat-tuong-lai-vi-ma-tuy-2212345.html", "Nghệ sĩ Việt đánh mất tương lai vì ma túy")
    ]
    
    for i, (url, title) in enumerate(articles):
        out_path = out_dir / f"news_{i+1}.json"
        generate_mock_article(url, out_path, title)
        print(f"Generated {url}")

if __name__ == "__main__":
    main()
