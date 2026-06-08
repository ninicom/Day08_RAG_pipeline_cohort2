import os
from pathlib import Path

def main():
    out_dir = Path("data/landing/legal")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    LEGAL_DOCS = {
        "Luat_Phong_chong_ma_tuy_2021.pdf": "https://datafiles.chinhphu.vn/cpp/files/vbpq/2022/01/73luat.pdf",
        "Bo_luat_Hinh_su_2015_sua_doi_2017.pdf": 'https://eu-central.storage.cloudconvert.com/tasks/851c3efc-4121-4d29-be50-d84816a942e3/Luật-12-2017-QH14.docx?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20260608%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20260608T045737Z&X-Amz-Expires=86400&X-Amz-Signature=42cfe106c8536a4422292130c9e93a5749ce57613990b30ed3013b7bd0db3111&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3D"Lu%3Ft-12-2017-QH14.docx"%3B%20filename*%3DUTF-8\'\'Lu%E1%BA%ADt-12-2017-QH14.docx&response-content-type=application%2Fvnd.openxmlformats-officedocument.wordprocessingml.document&x-id=GetObject',
        "Nghi_dinh_105_2021_ND_CP.pdf": "https://luatvietnam.vn/van-ban/tai-file-092805ad-0e3a-8e00-0668-b8b269fa9daf" 
    }
    
    print("=== TASK 1: TẢI DỮ LIỆU TỪ DIRECT LINKS ===")
    
    import requests
    for name, url in LEGAL_DOCS.items():
        out_path = out_dir / name
        print(f"Downloading {name}...")
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            if res.status_code == 200:
                with open(out_path, 'wb') as f:
                    f.write(res.content)
                print(f" -> Thành công: {name}")
            else:
                print(f" -> LỖI: {res.status_code}. Server từ chối truy cập (403 Forbidden).")
        except Exception as e:
            print(f" -> LỖI: {e}")
            
    # Kiểm tra lại
    existing_pdfs = list(out_dir.glob("*.pdf"))
    print(f"\nHiện có {len(existing_pdfs)} file PDF trong {out_dir}.")
    if len(existing_pdfs) < 3:
        print("\nLưu ý: Một số link tải trực tiếp bị lỗi 403 (do Cloudflare chặn hoặc link CloudConvert hết hạn).")
        print("Vui lòng tải các file bị lỗi bằng trình duyệt và chép tay vào thư mục `data/landing/legal/` nhé.")

if __name__ == "__main__":
    main()
