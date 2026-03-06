import os
import json
import zipfile
import shutil

def build_extensions():
    extensions_dir = "." # Thư mục gốc chứa code (master)
    output_dir = "dist"  # Thư mục sẽ đẩy lên nhánh builds
    index_data = []

    # Xóa thư mục dist cũ nếu có để build mới hoàn toàn
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Duyệt qua các thư mục extension (ví dụ: tranh18, vbook-extension, ...)
    for entry in os.scandir(extensions_dir):
        # Chỉ xử lý thư mục, bỏ qua thư mục ẩn, thư mục dist và thư mục .github
        if entry.is_dir() and not entry.name.startswith('.') and entry.name not in [output_dir, '.github', '__pycache__']:
            plugin_config_file = os.path.join(entry.path, 'plugin.json')
            
            if os.path.exists(plugin_config_file):
                # 1. Đọc metadata từ plugin.json của extension
                with open(plugin_config_file, 'r', encoding='utf-8') as f:
                    try:
                        config = json.load(f)
                    except Exception as e:
                        print(f"Lỗi đọc file {plugin_config_file}: {e}")
                        continue

                # 2. Tạo thư mục tương ứng trong dist (ví dụ: dist/tranh18/)
                extension_output_path = os.path.join(output_dir, entry.name)
                os.makedirs(extension_output_path)

                # 3. Nén toàn bộ nội dung thư mục đó thành plugin.zip
                zip_path = os.path.join(extension_output_path, 'plugin.zip')
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(entry.path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Tạo đường dẫn tương đối trong file zip
                            arcname = os.path.relpath(file_path, entry.path)
                            zipf.write(file_path, arcname)

                # 4. Tạo metadata cho file plugin.json tổng hợp (ở gốc nhánh builds)
                # Link URL lúc này sẽ trỏ vào thư mục/plugin.zip
                ext_info = {
                    "name": config.get("metadata", {}).get("name", entry.name),
                    "author": config.get("metadata", {}).get("author", "Unknown"),
                    "version": config.get("metadata", {}).get("version", "1.0.0"),
                    "url": f"{entry.name}/plugin.zip", 
                    "path": entry.name
                }
                index_data.append(ext_info)
                print(f"Đã đóng gói: {entry.name} -> {entry.name}/plugin.zip")

    # 5. Ghi file plugin.json tổng hợp vào thư mục gốc của dist
    if index_data:
        with open(os.path.join(output_dir, 'plugin.json'), 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    build_extensions()
    
