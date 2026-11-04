"""
augment_dataset.py - Augment existing seed images using PIL to create a viable dataset
"""
import os
import sys
import random
from PIL import Image, ImageEnhance, ImageOps

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
TARGET_COUNT_PER_CLASS = 30

def augment_class(cat_dir):
    files = [
        f for f in os.listdir(cat_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) and not f.startswith("aug_")
    ]
    if not files:
        print(f"No seed images found in {cat_dir}")
        return

    current_files = [
        f for f in os.listdir(cat_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]
    needed = TARGET_COUNT_PER_CLASS - len(current_files)
    if needed <= 0:
        return

    print(f"Generating {needed} augmented images for {os.path.basename(cat_dir)}...")
    idx = 1
    while needed > 0:
        seed_name = random.choice(files)
        seed_path = os.path.join(cat_dir, seed_name)
        try:
            with Image.open(seed_path) as img:
                img = img.convert("RGB")
                
                # Apply random augmentations
                # 1. Flip
                if random.random() > 0.5:
                    img = ImageOps.mirror(img)
                
                # 2. Rotation
                angle = random.choice([-25, -15, -10, 10, 15, 25])
                img = img.rotate(angle, resample=Image.BICUBIC, expand=False)
                
                # 3. Brightness
                factor = random.uniform(0.75, 1.25)
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(factor)
                
                # 4. Contrast
                factor = random.uniform(0.8, 1.2)
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(factor)
                
                # 5. Color jitter
                factor = random.uniform(0.8, 1.2)
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(factor)
                
                save_path = os.path.join(cat_dir, f"aug_{idx:03d}.jpg")
                img.save(save_path, "JPEG", quality=90)
                needed -= 1
                idx += 1
        except Exception as e:
            print(f"Error augmenting {seed_path}: {e}")
            break

def main():
    print("=" * 55)
    print("  Dataset Augmentation (Generating 30 images/class)")
    print("=" * 55)
    for cat in os.listdir(DATASET_DIR):
        cat_path = os.path.join(DATASET_DIR, cat)
        if os.path.isdir(cat_path):
            augment_class(cat_path)
    
    print("\nUpdated Dataset Summary:")
    print("-" * 40)
    total = 0
    for cat in sorted(os.listdir(DATASET_DIR)):
        cat_path = os.path.join(DATASET_DIR, cat)
        if os.path.isdir(cat_path):
            count = len([
                f for f in os.listdir(cat_path)
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            ])
            total += count
            print(f"   {cat:20s}  ->  {count:4d} images")
    print("-" * 40)
    print(f"   {'TOTAL':20s}  ->  {total:4d} images")

if __name__ == "__main__":
    main()
