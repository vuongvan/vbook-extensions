import os
import json
import zipfile
import shutil

def build_extensions():
    # Cấu hình Repo của bạn
    USER_REPO = "vuongvan/vbook-extensions"
    BRANCH = "builds"
    BASE_RAW_URL = f"https://raw.githubusercontent.com/{USER_REPO}/{BRANCH}"
    
    extensions_dir = "." 
    output_dir = "dist"
    
    # Khởi tạo Object chứa toàn bộ plugin (giống Darkrai9x)
    all_plugins_data = {}

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for entry in os.scandir(extensions_dir):
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
                zip_path = os.path.join(ext_output_dir, 'plugin.zip')
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(entry.path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, entry.path)
                            zipf.write(file_path, arcname)

                # 3. Cập nhật link tải vào nội dung config
                # Cấu trúc: https://raw.githubusercontent.com/vuongvan/vbook-extensions/builds/tranh18/plugin.zip
                config['path'] = f"{BASE_RAW_URL}/{entry.name}/plugin.zip"

                # 4. Thêm vào object tổng với Key là tên thư mục
                all_plugins_data[entry.name] = config
                print(f"Đã xử lý: {entry.name}")

    # 5. Ghi file plugin.json tổng hợp theo định dạng Object
    if all_plugins_data:
        with open(os.path.join(output_dir, 'plugin.json'), 'w', encoding='utf-8') as f:
            json.dump(all_plugins_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    build_extensions()
            
