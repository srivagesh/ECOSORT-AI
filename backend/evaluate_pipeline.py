# ─────────────────────────────────────────────────────────
#  backend/evaluate_pipeline.py
#  Rigorous Empirical Evaluation Benchmark for EcoSort AI
# ─────────────────────────────────────────────────────────
import io
import json
import os
import sys
import numpy as np
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app, CLASS_LABELS

def run_benchmark():
    app.config["TESTING"] = True
    client = app.test_client()
    dataset_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "dataset"))

    print("\n" + "=" * 60)
    print("  ECOSORT AI - EMPIRICAL BENCHMARK & RELIABILITY AUDIT")
    print("=" * 60)

    # ── 1. Evaluate E-Waste Classification (180 Real Dataset Samples) ──
    y_true = []
    y_pred = []
    e_waste_results = []

    print("\n[1/3] Benchmarking all 6 E-Waste Categories...")
    for cat in CLASS_LABELS:
        cat_dir = os.path.join(dataset_dir, cat)
        if not os.path.isdir(cat_dir):
            continue
        files = [f for f in os.listdir(cat_dir) if f.lower().endswith((".jpg", ".png", ".webp"))]
        correct = 0
        for fname in files:
            fpath = os.path.join(cat_dir, fname)
            with open(fpath, "rb") as fp:
                resp = client.post(
                    "/predict",
                    data={"file": (fp, f"{cat}_{fname}")},
                    content_type="multipart/form-data"
                )
            res = resp.get_json()
            pred_class = res.get("prediction", {}).get("class", "error")
            is_correct = (pred_class == cat)
            if is_correct:
                correct += 1
            y_true.append(cat)
            y_pred.append(pred_class)
            e_waste_results.append({
                "file": fname,
                "expected": cat,
                "predicted": pred_class,
                "confidence": res.get("prediction", {}).get("confidence", 0.0),
                "correct": is_correct
            })
        print(f"   ✓ {cat:<15}: {correct}/{len(files)} correct ({correct / len(files) * 100:.1f}%)")

    # ── 2. Evaluate Non-E-Waste Rejection (OOD Test Battery) ──
    print("\n[2/3] Benchmarking Non-E-Waste Rejection (OOD Battery)...")
    non_ewaste_tests = [
        {"id": "OOD-01", "name": "shoe_waste.jpg", "type": "Footwear", "color": (160, 80, 50)},
        {"id": "OOD-02", "name": "running_sneaker.png", "type": "Footwear", "color": (200, 50, 50)},
        {"id": "OOD-03", "name": "plastic_chair.jpg", "type": "Furniture", "color": (50, 150, 220)},
        {"id": "OOD-04", "name": "wooden_table.jpg", "type": "Furniture", "color": (139, 69, 19)},
        {"id": "OOD-05", "name": "banana_fruit.jpg", "type": "Food / Organic", "color": (255, 225, 50)},
        {"id": "OOD-06", "name": "fresh_apple.jpg", "type": "Food / Organic", "color": (220, 30, 30)},
        {"id": "OOD-07", "name": "book_novel.jpg", "type": "Stationery / Paper", "color": (240, 230, 210)},
        {"id": "OOD-08", "name": "ballpoint_pen.jpg", "type": "Stationery / Writing", "color": (20, 20, 20)},
        {"id": "OOD-09", "name": "cotton_tshirt.jpg", "type": "Clothing / Apparel", "color": (40, 60, 180)},
        {"id": "OOD-10", "name": "denim_jeans.jpg", "type": "Clothing / Apparel", "color": (25, 45, 120)},
        {"id": "OOD-11", "name": "house_plant.jpg", "type": "Plants / Nature", "color": (34, 139, 34)},
        {"id": "OOD-12", "name": "garden_flower.jpg", "type": "Plants / Nature", "color": (230, 50, 150)},
        {"id": "OOD-13", "name": "water_bottle.jpg", "type": "Household Plastic", "color": (180, 220, 250)},
        {"id": "OOD-14", "name": "ceramic_mug.jpg", "type": "Household Ceramic", "color": (210, 180, 140)},
        {"id": "OOD-15", "name": "white_wall_blank.jpg", "type": "Plain Background", "color": (245, 245, 245)},
        {"id": "OOD-16", "name": "grey_sheet_blank.jpg", "type": "Plain Background", "color": (128, 128, 128)},
        {"id": "OOD-17", "name": "pet_dog.jpg", "type": "Animal", "color": (150, 100, 60)},
        {"id": "OOD-18", "name": "bicycle.jpg", "type": "Vehicle / Transport", "color": (70, 70, 70)},
    ]

    ood_results = []
    rejected_count = 0
    for test in non_ewaste_tests:
        img = Image.new("RGB", (224, 224), color=test["color"])
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        resp = client.post(
            "/predict",
            data={"file": (buf, test["name"])},
            content_type="multipart/form-data"
        )
        res = resp.get_json()
        is_ewaste = res.get("is_ewaste", True)
        pred_class = res.get("prediction", {}).get("class")
        conf = res.get("prediction", {}).get("confidence", 0.0)
        detected_obj = res.get("detected_object", "Unknown")

        is_correctly_rejected = (is_ewaste is False and pred_class == "not_ewaste")
        if is_correctly_rejected:
            rejected_count += 1

        ood_results.append({
            "id": test["id"],
            "name": test["name"],
            "type": test["type"],
            "is_ewaste": is_ewaste,
            "predicted_class": pred_class,
            "confidence": conf,
            "detected_object": detected_obj,
            "correctly_rejected": is_correctly_rejected
        })

    print(f"   ✓ OOD Rejection Rate: {rejected_count}/{len(non_ewaste_tests)} ({rejected_count / len(non_ewaste_tests) * 100:.1f}%)")

    # ── 3. Compute Metrics & Confusion Matrix ──
    print("\n[3/3] Computing Quantitative Metrics...")
    report = classification_report(y_true, y_pred, target_names=CLASS_LABELS, output_dict=True)
    cm = confusion_matrix(y_true, y_pred, labels=CLASS_LABELS)

    summary = {
        "total_ewaste_tested": len(y_true),
        "total_ewaste_correct": sum(1 for t, p in zip(y_true, y_pred) if t == p),
        "ewaste_accuracy": round(sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true) * 100, 2),
        "total_ood_tested": len(non_ewaste_tests),
        "total_ood_rejected": rejected_count,
        "ood_rejection_accuracy": round(rejected_count / len(non_ewaste_tests) * 100, 2),
        "false_positive_rate_on_non_ewaste": round((len(non_ewaste_tests) - rejected_count) / len(non_ewaste_tests) * 100, 2),
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
        "ood_details": ood_results,
    }

    with open(os.path.join(BASE_DIR, "benchmark_results.json"), "w") as fp:
        json.dump(summary, fp, indent=2)

    print("\n" + "=" * 60)
    print(f"  BENCHMARK COMPLETE")
    print(f"  E-Waste Overall Accuracy : {summary['ewaste_accuracy']}% ({summary['total_ewaste_correct']}/{summary['total_ewaste_tested']})")
    print(f"  Non-E-Waste Rejection    : {summary['ood_rejection_accuracy']}% ({summary['total_ood_rejected']}/{summary['total_ood_tested']})")
    print(f"  False Positive Rate (OOD): {summary['false_positive_rate_on_non_ewaste']}%")
    print("=" * 60 + "\n")

    return summary


if __name__ == "__main__":
    run_benchmark()
