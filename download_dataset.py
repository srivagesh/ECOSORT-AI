# ─────────────────────────────────────────────────────────
#  download_dataset.py  –  Download e-waste dataset
# ─────────────────────────────────────────────────────────
"""
Downloads an e-waste image dataset for training.

Option 1 (Recommended): Use images from the web
Option 2: Create placeholder folder structure for manual population

Usage:
    python download_dataset.py
"""

import os
import sys
import urllib.request
import zipfile
import shutil

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

CATEGORIES = [
    "battery",
    "charger_cable",
    "circuit_board",
    "laptop",
    "mobile_phone",
    "monitor_tv",
]


def create_folder_structure():
    """Create the expected folder structure for the dataset."""
    print("📁 Creating dataset folder structure...")
    for cat in CATEGORIES:
        path = os.path.join(DATASET_DIR, cat)
        os.makedirs(path, exist_ok=True)
        print(f"   ✅ {path}")
    print()


def download_sample_images():
    """
    Download a small set of sample images from Unsplash/Pexels for each category.
    These are royalty-free images for educational use.
    """
    # Sample image URLs (royalty-free / educational use)
    # In a real project, you'd use a proper dataset from Kaggle
    sample_urls = {
        "mobile_phone": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
            "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400",
            "https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=400",
            "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=400",
            "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=400",
        ],
        "laptop": [
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400",
            "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400",
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400",
            "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400",
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400",
        ],
        "battery": [
            "https://images.unsplash.com/photo-1619641805634-98e04336af99?w=400",
            "https://images.unsplash.com/photo-1609692814857-28e0a2de7844?w=400",
            "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400",
            "https://images.unsplash.com/photo-1620714223084-8fcacc6dfd8d?w=400",
        ],
        "charger_cable": [
            "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400",
            "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400",
            "https://images.unsplash.com/photo-1601999109332-542b18dbef7e?w=400",
        ],
        "circuit_board": [
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400",
            "https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=400",
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400",
            "https://images.unsplash.com/photo-1562976540-1502c2145186?w=400",
        ],
        "monitor_tv": [
            "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=400",
            "https://images.unsplash.com/photo-1561883088-039e53143d73?w=400",
            "https://images.unsplash.com/photo-1585792180666-f7347c490ee2?w=400",
        ],
    }

    print("⬇️  Downloading sample images...")
    total = 0

    for category, urls in sample_urls.items():
        cat_dir = os.path.join(DATASET_DIR, category)
        os.makedirs(cat_dir, exist_ok=True)

        for i, url in enumerate(urls):
            filename = f"{category}_{i+1:03d}.jpg"
            filepath = os.path.join(cat_dir, filename)

            if os.path.exists(filepath):
                print(f"   ⏭️  {filename} already exists, skipping")
                continue

            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=15) as response:
                    with open(filepath, "wb") as f:
                        f.write(response.read())
                print(f"   ✅ {category}/{filename}")
                total += 1
            except Exception as e:
                print(f"   ❌ {category}/{filename} — {e}")

    print(f"\n📦 Downloaded {total} images total.\n")


def print_dataset_stats():
    """Print a summary of the dataset."""
    print("📊 Dataset Summary:")
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
            print(f"   {cat:20s}  →  {count:4d} images")
    print("-" * 40)
    print(f"   {'TOTAL':20s}  →  {total:4d} images")
    print()

    if total < 50:
        print("⚠️  Very few images! For decent training, aim for at least")
        print("   50-100 images per category. Options:")
        print()
        print("   1. Download from Kaggle:")
        print("      https://www.kaggle.com/datasets")
        print("      Search: 'e-waste classification' or 'electronic waste'")
        print()
        print("   2. Use Google Images to collect ~50+ per category")
        print()
        print("   3. Use data augmentation (already built into train_model.py)")
        print()


def main():
    print("=" * 55)
    print("  E-Waste Dataset Setup")
    print("=" * 55)
    print()

    create_folder_structure()
    download_sample_images()
    print_dataset_stats()

    print("✅ Dataset setup complete!")
    print(f"   Location: {DATASET_DIR}")
    print()
    print("Next step:")
    print("   cd backend")
    print("   python model/train_model.py")


if __name__ == "__main__":
    main()
