import os
import cv2

input_folder = "dataset"
image_size = (224, 224)

for split in os.listdir(input_folder):
    split_path = os.path.join(input_folder, split)

    if not os.path.isdir(split_path):
        continue

    for category in os.listdir(split_path):
        category_path = os.path.join(split_path, category)

        if not os.path.isdir(category_path):
            continue

        for img_name in os.listdir(category_path):
            img_path = os.path.join(category_path, img_name)

            if not img_name.lower().endswith(
                (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")
            ):
                print(f"Skipping non-image file: {img_path}")
                continue

            img = cv2.imread(img_path)

            if img is None:
                print(f"Warning: Could not read {img_path}. Check the file integrity.")
                continue

            img_resized = cv2.resize(img, image_size)
            cv2.imwrite(img_path, img_resized)

print("✅ All images resized and replaced successfully!")
