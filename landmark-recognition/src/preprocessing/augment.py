import os
import cv2
import numpy as np
import random
from tqdm import tqdm

SRC_FOLDER = "dataset/train"
DEST_FOLDER = "train_augmented"

os.makedirs(DEST_FOLDER, exist_ok=True)


def random_crop(image, crop_size_range=(0.5, 0.8)):
    h, w, _ = image.shape
    crop_factor = random.uniform(*crop_size_range)
    crop_h, crop_w = int(h * crop_factor), int(w * crop_factor)
    x_start = random.randint(0, w - crop_w) if w > crop_w else 0
    y_start = random.randint(0, h - crop_h) if h > crop_h else 0
    cropped_img = image[y_start : y_start + crop_h, x_start : x_start + crop_w]
    return cropped_img


def random_rotate(image, max_angle=30):
    angle = random.uniform(-max_angle, max_angle)
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img = cv2.warpAffine(
        image, rotation_matrix, (w, h), borderMode=cv2.BORDER_REFLECT
    )
    return rotated_img


def random_lighting(image, brightness_range=(-50, 50), contrast_range=(0.8, 1.5)):
    brightness = random.randint(*brightness_range)
    contrast = random.uniform(*contrast_range)
    adjusted_img = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return adjusted_img


for class_folder in tqdm(os.listdir(SRC_FOLDER)):
    class_path = os.path.join(SRC_FOLDER, class_folder)
    save_path = os.path.join(DEST_FOLDER, class_folder)

    if not os.path.isdir(class_path):
        continue

    os.makedirs(save_path, exist_ok=True)

    for img_index, img_name in enumerate(os.listdir(class_path), start=1):
        img_path = os.path.join(class_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        class_prefix = class_folder.lower().replace(" ", "_")
        original_name = f"{class_prefix}_{img_index:03d}.jpg"
        cv2.imwrite(
            os.path.join(save_path, original_name), cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        )

        for i in range(4):
            cropped_img = random_crop(img)
            rotated_img = random_rotate(cropped_img)
            adjusted_img = random_lighting(rotated_img)
            aug_name = f"{class_prefix}_{img_index:03d}_aug{i+1}.jpg"
            cv2.imwrite(
                os.path.join(save_path, aug_name),
                cv2.cvtColor(adjusted_img, cv2.COLOR_RGB2BGR),
            )

print("✅ Data Augmentation Completed! Augmented images saved in:", DEST_FOLDER)
