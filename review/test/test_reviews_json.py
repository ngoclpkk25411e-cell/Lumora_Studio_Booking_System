import json
import os

# đường dẫn datasets ở root project
folder = "../../../datasets"
file_path = os.path.join(folder, "reviews.json")

# nếu thư mục datasets chưa tồn tại → tạo
os.makedirs(folder, exist_ok=True)

# tạo file json
with open(file_path, "w", encoding="utf-8") as f:
    json.dump([], f, indent=4)

print("reviews.json created successfully")