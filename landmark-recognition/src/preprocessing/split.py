import os
import shutil
import random

input_folder = "raw_dataset"
output_folder = "dataset"

train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

for split in ["train", "val", "test"]:
    for category in os.listdir(input_folder):
        os.makedirs(os.path.join(output_folder, split, category), exist_ok=True)

for category in os.listdir(input_folder):
    category_path = os.path.join(input_folder, category)
    images = os.listdir(category_path)
    random.shuffle(images)

    train_end = int(len(images) * train_ratio)
    val_end = train_end + int(len(images) * val_ratio)

    train_files = images[:train_end]
    val_files = images[train_end:val_end]
    test_files = images[val_end:]

    for file in train_files:
        shutil.copy(
            os.path.join(category_path, file),
            os.path.join(output_folder, "train", category, file),
        )

    for file in val_files:
        shutil.copy(
            os.path.join(category_path, file),
            os.path.join(output_folder, "val", category, file),
        )

    for file in test_files:
        shutil.copy(
            os.path.join(category_path, file),
            os.path.join(output_folder, "test", category, file),
        )

print("Dataset successfully split into Train, Val, and Test!")
