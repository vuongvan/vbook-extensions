import os
import json
import zipfile
import shutil

def build_extensions():
    # Cấu hình Repo và thông tin của bạn
    USER_REPO = "vuongvan/vbook-extensions"
    BRANCH = "builds"
    BASE_RAW_URL = f"https://raw.githubusercontent.com/{USER_REPO}/{BRANCH}"
    
    extensions_dir = "." 
    output_dir = "dist"
    
    # Khởi tạo cấu trúc file plugin.json theo mẫu yêu cầu
    final_output = {
        "metadata": {
            "author": "vuongvan",
            "description": "Thích là nhích ^^!"
        },
        "data": []
    }

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for entry in os.scandir(extensions_dir):
        # Bỏ qua các file và thư mục hệ thống
        if entry.is_dir() and not entry.name.startswith('.') and entry.name not in [output_dir, '.github', '__pycache__']:
            plugin_config_path = os.path.join(entry.path, 'plugin.json')
            
            if os.path.exists(plugin_config_path):
                # 1. Đọc nội dung plugin.json của từng extension
                with open(plugin_config_path, 'r', encoding='utf-8') as f:
                    try:
                        config = json.load(f)
                    except Exception as e:
                        print(f"Lỗi đọc file {plugin_config_path}: {e}")
                        continue

                # 2. Tạo thư mục và nén plugin.zip
                ext_output_dir = os.path.join(output_dir, entry.name)
                os.makedirs(ext_output_dir)
                zip_name = "plugin.zip"
                zip_path = os.path.join(ext_output_dir, zip_name)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(entry.path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, entry.path)
                            zipf.write(file_path, arcname)

                # 3. Trích xuất metadata từ plugin.json gốc để đưa vào danh sách data
                # Ưu tiên lấy từ config['metadata'], nếu không có thì lấy mặc định
                meta = config.get("metadata", {})
                
                ext_entry = {
                    "name": meta.get("name", entry.name),
                    "author": meta.get("author", final_output["metadata"]["author"]),
                    "path": f"{BASE_RAW_URL}/{entry.name}/{zip_name}",
                    "version": meta.get("version", 1),
                    "source": meta.get("source", ""),
                    "icon": f"{BASE_RAW_URL}/{entry.name}/icon.png", # Mặc định lấy icon.png trong mỗi folder
                    "description": meta.get("description", "Đọc truyện trên " + entry.name),
                    "type": meta.get("type", "comic"),
                    "locale": meta.get("locale", "vi_VN")
                }

                final_output["data"].append(ext_entry)
                print(f"Đã đóng gói: {entry.name}")

    # 4. Ghi file plugin.json tổng hợp vào thư mục dist
    if final_output["data"]:
        with open(os.path.join(output_dir, 'plugin.json'), 'w', encoding='utf-8') as f:
            json.dump(final_output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    build_extensions()
                
