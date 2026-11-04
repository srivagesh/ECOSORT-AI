# ─────────────────────────────────────────────────────────
#  train_model.py  –  Train MobileNetV2 for E-Waste Classification
# ─────────────────────────────────────────────────────────
"""
Usage:
    python train_model.py

Expects a dataset folder at  ../dataset/  with sub-folders:
    battery/  charger_cable/  circuit_board/  laptop/  mobile_phone/  monitor_tv/

Each sub-folder should contain images (JPG/PNG/WEBP) of that category.
"""

import json
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import matplotlib
matplotlib.use("Agg")  # non-interactive backend (no GUI needed)
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # suppress TF info logs

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# ── Paths ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "dataset"))
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "ewaste_model.keras")
MODEL_SAVE_H5_PATH = os.path.join(BASE_DIR, "ewaste_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "class_labels.json")
EVAL_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "evaluation"))

os.makedirs(EVAL_DIR, exist_ok=True)

# ── Hyperparameters ──────────────────────────────────────
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 12
LEARNING_RATE = 0.0001
VALIDATION_SPLIT = 0.2


def build_datasets():
    """Load training and validation datasets from the dataset directory."""
    print(f"\n📂 Loading dataset from: {DATASET_DIR}")

    if not os.path.isdir(DATASET_DIR):
        print(f"❌ Dataset directory not found: {DATASET_DIR}")
        print("   Please create sub-folders (battery, charger_cable, etc.) with images.")
        sys.exit(1)

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
    print(f"✅ Found {len(class_names)} classes: {class_names}")

    # Save class labels
    with open(LABELS_PATH, "w") as f:
        json.dump(class_names, f, indent=2)
    print(f"💾 Class labels saved to: {LABELS_PATH}")

    # Prefetch for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds, class_names


def build_model(num_classes: int):
    """Build MobileNetV2 transfer-learning model."""
    print("\n🧠 Building MobileNetV2 model...")

    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(*IMG_SIZE, 3),
    )
    base_model.trainable = False  # freeze base layers

    model = models.Sequential([
        layers.Input(shape=(*IMG_SIZE, 3)),
        # Preprocessing: scale pixel values to [-1, 1] as MobileNetV2 expects
        layers.Rescaling(1.0 / 127.5, offset=-1),

        # Data augmentation
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.1),

        # Base model
        base_model,

        # Classification head
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(128, activation="relu"),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax"),
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()
    return model, base_model


def fine_tune(model, base_model, train_ds, val_ds):
    """Unfreeze top layers of base model and fine-tune."""
    print("\n🔧 Fine-tuning top layers...")

    # Unfreeze the last 30 layers of MobileNetV2
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True, verbose=1),
        ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True, verbose=1),
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=10,
        callbacks=callbacks,
    )
    return history


def evaluate(model, val_ds, class_names):
    """Generate evaluation metrics and plots."""
    print("\n📊 Evaluating model...")

    # Get predictions
    y_true = []
    y_pred = []

    for images, labels in val_ds:
        predictions = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(predictions, axis=1))

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # Classification report
    report = classification_report(
        y_true, y_pred, target_names=class_names, digits=4
    )
    print("\n" + report)

    report_path = os.path.join(EVAL_DIR, "metrics_report.txt")
    with open(report_path, "w") as f:
        f.write("E-Waste Classification — Evaluation Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(report)
    print(f"💾 Metrics report saved to: {report_path}")

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Greens",
        xticklabels=class_names,
        yticklabels=class_names,
    )
    plt.title("E-Waste Classification — Confusion Matrix", fontsize=14)
    plt.xlabel("Predicted", fontsize=12)
    plt.ylabel("Actual", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    cm_path = os.path.join(EVAL_DIR, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=150)
    print(f"💾 Confusion matrix saved to: {cm_path}")
    plt.close()


def plot_history(history, label=""):
    """Save accuracy and loss plots."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Accuracy
    ax1.plot(history.history["accuracy"], label="Train")
    ax1.plot(history.history["val_accuracy"], label="Validation")
    ax1.set_title(f"Accuracy {label}")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Loss
    ax2.plot(history.history["loss"], label="Train")
    ax2.plot(history.history["val_loss"], label="Validation")
    ax2.set_title(f"Loss {label}")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(EVAL_DIR, f"training_curves{label.replace(' ', '_')}.png")
    plt.savefig(path, dpi=150)
    print(f"💾 Training curves saved to: {path}")
    plt.close()


def main():
    print("=" * 55)
    print("  E-Waste Classification — MobileNetV2 Training")
    print("=" * 55)

    # 1) Load data
    train_ds, val_ds, class_names = build_datasets()
    num_classes = len(class_names)

    # 2) Build model
    model, base_model = build_model(num_classes)

    # 3) Initial training (frozen base)
    print("\n🚀 Phase 1: Training classification head...")
    callbacks = [
        EarlyStopping(patience=4, restore_best_weights=True, verbose=1),
        ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True, verbose=1),
    ]

    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks,
    )
    plot_history(history1, label=" (Phase 1 — Frozen Base)")

    # 4) Fine-tune top layers
    history2 = fine_tune(model, base_model, train_ds, val_ds)
    plot_history(history2, label=" (Phase 2 — Fine-Tuning)")

    # 5) Evaluate
    evaluate(model, val_ds, class_names)

    # Save final model in both formats for maximum compatibility
    model.save(MODEL_SAVE_PATH)
    try:
        model.save(MODEL_SAVE_H5_PATH)
    except Exception as e:
        print(f"Note: .h5 export: {e}")

    print(f"\n✅ Model saved to: {MODEL_SAVE_PATH}")
    print("🎉 Training complete!")


if __name__ == "__main__":
    main()
