# Devotional Landmark Recognition

## Project Overview

This project aims to develop a deep learning model for Devotional landmark recognition. It involves preprocessing a dataset, performing data augmentation and normalization, and training a model for classification.

## Folder Structure

```
landmark-recognition/
├── assets/               # Stores images, icons, or other resources
├── data/                 # Contains the dataset
├── models/               # Trained models and checkpoints
└── src/
    ├── preprocessing/    # Data preprocessing scripts
    │   ├── augment.py    # Performs data augmentation
    │   ├── normalize.py  # Normalizes dataset images
    │   ├── rename.py     # Renames dataset images
    │   ├── resize.py     # Resizes dataset images
    │   └── split.py      # Splits dataset into train, test, and validation sets
    └── training/
        └── main.py       # Model training script
├── .gitignore            # Git ignored files and folders
└── requirements.txt      # Required dependencies
```

## Installation & Setup

### 1️. Clone the Repository

```bash
git clone https://github.com/thisissudeep/landmark-recognition.git
cd landmark-recognition
```

### 2️. Install Dependencies

Ensure you have Python installed (preferably 3.8+), then install dependencies:

```bash
pip install -r requirements.txt
```

### 3️. Dataset Preparation

1. **Rename the images:**
   ```bash
   python src/preprocessing/rename.py
   ```
2. **Split dataset into train, test, and validation sets:**
   ```bash
   python src/preprocessing/split.py
   ```
3. **Resize the images:**
   ```bash
   python src/preprocessing/resize.py
   ```
4. **Apply data augmentation:**
   ```bash
   python src/preprocessing/augment.py
   ```
5. **Normalize dataset images:**
   ```bash
   python src/preprocessing/normalize.py
   ```

### 4️. Model Training

After preprocessing the dataset, start training the model:

```
Execute the Notebook src/training/train.py
```

### 5️. Run Model

Once training is complete, the trained model will be saved in the `models/` folder. You can execute it using:

```bash
python src/main.py
```

**Happy Coding :)**
