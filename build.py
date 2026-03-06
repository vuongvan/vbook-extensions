import os
import json
import zipfile

def build_extensions():
    extensions_dir = "." # Thư mục gốc chứa các folder extension
    output_dir = "dist"  # Thư mục chứa kết quả sau khi đóng gói
    index_data = []

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Duyệt qua các thư mục con
    for entry in os.scandir(extensions_dir):
        if entry.is_dir() and not entry.name.startswith('.') and entry.name != output_dir:
            plugin_file = os.path.join(entry.path, 'plugin.json')
            
            if os.path.exists(plugin_file):
                # 1. Đọc thông tin plugin
                with open(plugin_file, 'r', encoding='utf-8') as f:
                    try:
                        config = json.load(f)
                    except:
                        print(f"Lỗi đọc file: {plugin_file}")
                        continue

                # 2. Tạo file ZIP cho extension này
                zip_name = f"{entry.name}.zip"
                zip_path = os.path.join(output_dir, zip_name)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(entry.path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, entry.path)
                            zipf.write(file_path, arcname)

                # 3. Cập nhật metadata cho file tổng (dùng URL trỏ đến nhánh builds)
                ext_info = {
                    "name": config.get("metadata", {}).get("name", entry.name),
                    "author": config.get("metadata", {}).get("author", "Unknown"),
                    "version": config.get("metadata", {}).get("version", "1.0.0"),
                    "url": zip_name, # Tên file zip trong cùng thư mục dist
                    "path": entry.name
                }
                index_data.append(ext_info)
                print(f"Đã đóng gói: {entry.name}")

    # 4. Ghi file plugin.json tổng hợp (giống định dạng Darkrai9x)
    with open(os.path.join(output_dir, 'plugin.json'), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    build_extensions()
