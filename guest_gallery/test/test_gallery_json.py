import os
import json

# đi lên root project
project_root = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

gallery_folder = os.path.join(
    project_root,
    "guest_ui",
    "guest_gallery",
    "images"
)

gallery_data = {"albums": []}

for album in os.listdir(gallery_folder):

    album_path = os.path.join(gallery_folder, album)

    if not os.path.isdir(album_path):
        continue

    images = []

    for file in os.listdir(album_path):

        if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):

            images.append(os.path.join(album, file))

    gallery_data["albums"].append({
        "name": album.capitalize(),
        "images": images
    })

json_path = os.path.join(project_root, "datasets", "gallery.json")

with open(json_path, "w", encoding="utf8") as f:
    json.dump(gallery_data, f, indent=4)

print("Gallery JSON created successfully!")