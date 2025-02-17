import cv2
import os
import numpy as np

dataset_path = "dataset"

for category in ["train", "val", "test"]:
    category_path = os.path.join(dataset_path, category)

    for class_folder in os.listdir(category_path):
        class_path = os.path.join(category_path, class_folder)

        if not os.path.isdir(class_path):
            continue

        for file in os.listdir(class_path):
            file_path = os.path.join(class_path, file)

            img = cv2.imread(file_path)

            if img is None:
                print(f"Skipping (not a valid image): {file}")
                continue

            img_normalized = img.astype(np.float32) / 255.0
            img_final = (img_normalized * 255).astype(np.uint8)
            cv2.imwrite(file_path, img_final)


print("Normalization complete!")
