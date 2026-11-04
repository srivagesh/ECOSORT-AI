# ─────────────────────────────────────────────────────────
#  download_and_train.py  –  Download real images & retrain
# ─────────────────────────────────────────────────────────
"""
Step 1: Downloads real e-waste images from DuckDuckGo Images (no API key needed)
Step 2: Retrains EfficientNetB0 on the downloaded dataset
Step 3: Saves the new model as ewaste_model.keras

Usage:
    python download_and_train.py

Requirements (all already installed in venv313):
    pip install requests pillow tensorflow scikit-learn seaborn matplotlib
    pip install duckduckgo_search   # <-- needs this!
"""

import json
import os
import sys
import time
import io
import hashlib
import urllib.request

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ── Paths ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "dataset"))
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "ewaste_model.keras")
LABELS_PATH = os.path.join(BASE_DIR, "class_labels.json")
EVAL_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "evaluation"))

os.makedirs(EVAL_DIR, exist_ok=True)

# ── Download Config ──────────────────────────────────────
IMAGES_PER_CLASS = 80   # target per class (will deduplicate)

# Search queries that should return clean, recognizable images
SEARCH_QUERIES = {
    "battery": [
        "AA battery white background",
        "lithium ion battery pack electronics",
        "9V battery electronics",
        "rechargeable battery cells",
        "power bank battery",
        "button cell battery",
        "battery pack laptop",
    ],
    "charger_cable": [
        "USB charger cable white background",
        "phone charger adapter plug",
        "USB-C charging cable electronics",
        "laptop power adapter charger",
        "charging brick adapter white",
        "micro USB cable",
        "lightning cable iPhone charger",
    ],
    "circuit_board": [
        "green circuit board PCB electronics",
        "motherboard computer hardware",
        "printed circuit board components",
        "electronic circuit board chips",
        "Arduino circuit board",
        "GPU graphics card circuit board",
        "RAM memory stick circuit board",
    ],
    "laptop": [
        "old laptop computer open lid",
        "broken laptop recycling",
        "used laptop computer side view",
        "laptop computer keyboard open",
        "damaged laptop electronics",
        "MacBook laptop white background",
        "laptop screen keyboard",
    ],
    "mobile_phone": [
        "old smartphone white background",
        "broken cracked smartphone screen",
        "used mobile phone electronics",
        "old iPhone discard recycle",
        "Samsung Galaxy smartphone",
        "damaged phone screen cracked",
        "mobile phone ewaste recycle",
    ],
    "monitor_tv": [
        "old computer monitor CRT",
        "flat screen monitor electronics",
        "old television recycling",
        "LCD monitor desktop",
        "broken TV screen ewaste",
        "old CRT television tube",
        "computer display monitor ewaste",
    ],
}

# ── Hyperparameters ──────────────────────────────────────
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS_PHASE1 = 15
EPOCHS_PHASE2 = 10
LEARNING_RATE = 1e-4
VALIDATION_SPLIT = 0.2


def install_duckduckgo_search():
    """Install duckduckgo_search if not present."""
    try:
        from duckduckgo_search import DDGS
        return True
    except ImportError:
        print("📦 Installing duckduckgo_search...")
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "duckduckgo_search"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ duckduckgo_search installed!")
            return True
        else:
            print(f"❌ Failed to install: {result.stderr}")
            return False


def download_images_for_class(class_name, queries, target_dir, target_count):
    """Download images for a class using DuckDuckGo Images search."""
    from duckduckgo_search import DDGS

    os.makedirs(target_dir, exist_ok=True)
    existing = [f for f in os.listdir(target_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    if len(existing) >= target_count:
        print(f"   ✅ {class_name}: {len(existing)} images already present, skipping download")
        return len(existing)

    downloaded = len(existing)
    seen_hashes = set()

    # Hash existing files to avoid duplicates
    for f in existing:
        try:
            with open(os.path.join(target_dir, f), 'rb') as fp:
                seen_hashes.add(hashlib.md5(fp.read(1024)).hexdigest())
        except Exception:
            pass

    print(f"\n   📥 Downloading images for: {class_name} (need {target_count - downloaded} more)")

    for query in queries:
        if downloaded >= target_count:
            break

        try:
            with DDGS() as ddgs:
                results = list(ddgs.images(
                    query,
                    max_results=20,
                    safesearch="on",
                    type_image="photo",
                ))
        except Exception as e:
            print(f"      ⚠️  Search failed for '{query}': {e}")
            time.sleep(2)
            continue

        for result in results:
            if downloaded >= target_count:
                break

            url = result.get("image", "")
            if not url:
                continue

            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    method="GET"
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    img_bytes = resp.read()

                # Deduplicate
                img_hash = hashlib.md5(img_bytes[:1024]).hexdigest()
                if img_hash in seen_hashes:
                    continue
                seen_hashes.add(img_hash)

                # Validate image
                from PIL import Image
                img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                w, h = img.size
                if w < 100 or h < 100:
                    continue

                # Save
                fname = f"{class_name}_{downloaded+1:04d}.jpg"
                save_path = os.path.join(target_dir, fname)
                img.save(save_path, "JPEG", quality=90)
                downloaded += 1
                print(f"      ✅ [{downloaded}/{target_count}] {fname}")

            except Exception:
                continue

        time.sleep(1.5)  # Be polite between queries

    print(f"   📊 {class_name}: {downloaded} images total")
    return downloaded


def download_all_classes():
    """Download images for all 6 e-waste categories."""
    print("\n" + "="*55)
    print("  PHASE 0: Downloading Real E-Waste Images")
    print("="*55)

    if not install_duckduckgo_search():
        print("❌ Cannot download images. Using existing dataset.")
        return

    for class_name, queries in SEARCH_QUERIES.items():
        class_dir = os.path.join(DATASET_DIR, class_name)
        downloaded = download_images_for_class(
            class_name, queries, class_dir, IMAGES_PER_CLASS
        )


def build_datasets():
    """Load training and validation datasets."""
    import tensorflow as tf

    print(f"\n📂 Loading dataset from: {DATASET_DIR}")

    # Count images per class
    for cls in os.listdir(DATASET_DIR):
        cls_dir = os.path.join(DATASET_DIR, cls)
        if os.path.isdir(cls_dir):
            count = len([f for f in os.listdir(cls_dir)
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
            print(f"   {cls}: {count} images")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )

    class_names = train_ds.class_names
    print(f"\n✅ Found {len(class_names)} classes: {class_names}")

    with open(LABELS_PATH, "w") as f:
        json.dump(class_names, f, indent=2)
    print(f"💾 Class labels saved to: {LABELS_PATH}")

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds, class_names


def build_model(num_classes):
    """Build EfficientNetB0 transfer-learning model (better than MobileNetV2)."""
    import tensorflow as tf
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import EfficientNetB0

    print("\n🧠 Building EfficientNetB0 model (stronger than MobileNetV2)...")

    base_model = EfficientNetB0(
        weights="imagenet",
        include_top=False,
        input_shape=(*IMG_SIZE, 3),
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(*IMG_SIZE, 3))

    # Data augmentation (only active during training)
    x = layers.RandomFlip("horizontal")(inputs)
    x = layers.RandomRotation(0.15)(x)
    x = layers.RandomZoom(0.15)(x)
    x = layers.RandomContrast(0.15)(x)
    x = layers.RandomBrightness(0.1)(x)

    # EfficientNet expects [0, 255] range (no rescaling needed)
    x = base_model(x, training=False)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model, base_model


def train_model(model, base_model, train_ds, val_ds):
    """Two-phase training: head-only then fine-tune."""
    import tensorflow as tf
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

    # Phase 1: Train head only
    print("\n🚀 Phase 1: Training classification head (frozen base)...")
    callbacks_p1 = [
        EarlyStopping(patience=5, restore_best_weights=True, verbose=1),
        ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True, verbose=1),
        ReduceLROnPlateau(patience=3, factor=0.5, verbose=1),
    ]
    h1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_PHASE1,
        callbacks=callbacks_p1,
    )

    # Phase 2: Fine-tune top 50 layers
    print("\n🔧 Phase 2: Fine-tuning top 50 EfficientNet layers...")
    base_model.trainable = True
    for layer in base_model.layers[:-50]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks_p2 = [
        EarlyStopping(patience=6, restore_best_weights=True, verbose=1),
        ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True, verbose=1),
        ReduceLROnPlateau(patience=3, factor=0.5, verbose=1),
    ]
    h2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_PHASE2,
        callbacks=callbacks_p2,
    )

    return h1, h2


def evaluate_model(model, val_ds, class_names):
    """Generate metrics and confusion matrix."""
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.metrics import classification_report, confusion_matrix

    print("\n📊 Evaluating model...")
    y_true, y_pred = [], []
    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
    print("\n" + report)

    report_path = os.path.join(EVAL_DIR, "metrics_report.txt")
    with open(report_path, "w") as f:
        f.write("E-Waste Classification — Evaluation Report (EfficientNetB0)\n")
        f.write("=" * 60 + "\n\n")
        f.write(report)
    print(f"💾 Metrics saved: {report_path}")

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
                xticklabels=class_names, yticklabels=class_names)
    plt.title("E-Waste Classification — Confusion Matrix (EfficientNetB0)", fontsize=13)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    cm_path = os.path.join(EVAL_DIR, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=150)
    print(f"💾 Confusion matrix: {cm_path}")
    plt.close()


def main():
    print("=" * 55)
    print("  E-Waste — Download + EfficientNetB0 Training")
    print("=" * 55)

    # Step 1: Download real images
    download_all_classes()

    # Step 2: Import TF (after download to avoid slow startup)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

    # Step 3: Build datasets
    train_ds, val_ds, class_names = build_datasets()
    num_classes = len(class_names)

    # Step 4: Build model
    model, base_model = build_model(num_classes)
    model.summary()

    # Step 5: Train
    train_model(model, base_model, train_ds, val_ds)

    # Step 6: Evaluate
    evaluate_model(model, val_ds, class_names)

    # Step 7: Save
    model.save(MODEL_SAVE_PATH)
    print(f"\n✅ Model saved to: {MODEL_SAVE_PATH}")
    print("🎉 Done! Restart the Flask backend to use the new model.")


if __name__ == "__main__":
    main()
