import os

SRC_FOLDER = "raw_dataset"

class_folders = sorted(os.listdir(SRC_FOLDER))
class_mapping = {folder: f"class{idx+1}" for idx, folder in enumerate(class_folders)}

for class_folder in class_folders:
    class_path = os.path.join(SRC_FOLDER, class_folder)

    if not os.path.isdir(class_path):
        continue

    class_label = class_mapping[class_folder]
    print(f"Renaming images in: {class_folder} → {class_label}")

    for idx, img_name in enumerate(sorted(os.listdir(class_path)), start=1):
        img_path = os.path.join(class_path, img_name)

        if not img_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue

        new_name = f"{class_label}_{idx:03d}{os.path.splitext(img_name)[1]}"
        new_path = os.path.join(class_path, new_name)

        os.rename(img_path, new_path)

print("✅ Image renaming completed successfully!")
