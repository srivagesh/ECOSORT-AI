# ─────────────────────────────────────────────────────────
#  backend/tests/test_audit.py
#  Comprehensive Validation & Reliability Test Suite
# ─────────────────────────────────────────────────────────
import io
import json
import os
import sys
import unittest
from PIL import Image

# Ensure backend root is on path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app, MAX_FILE_SIZE
from recommendations import RECOMMENDATIONS, CLASS_LABELS


class EcoSortAIAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.dataset_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "dataset"))

    # ── 1. API Endpoints Validation ──────────────────────────

    def test_health_endpoint(self):
        """GET /health must return 200, status 'ok', and loaded backbones."""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data.get("status"), "ok")
        self.assertTrue(data.get("efficientnet"))
        self.assertTrue(data.get("mobilenet"))
        self.assertEqual(len(data.get("classes")), 6)

    def test_classes_endpoint(self):
        """GET /classes must return all 6 e-waste categories with complete schema."""
        resp = self.client.get("/classes")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("classes", data)
        classes = data["classes"]
        self.assertEqual(len(classes), 6)

        required_keys = [
            "key", "category", "icon", "confidence_label",
            "recycling_route", "safety_precautions",
            "reuse_suggestions", "environmental_impact"
        ]
        for c in classes:
            for k in required_keys:
                self.assertIn(k, c, f"Missing key '{k}' in class {c.get('key')}")
                self.assertTrue(len(str(c[k])) > 0)

    # ── 2. Upload Validation & Security ──────────────────────

    def test_missing_file_field(self):
        """POST /predict without 'file' field must return 400 Bad Request."""
        resp = self.client.post("/predict", data={})
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_empty_filename(self):
        """POST /predict with empty filename must return 400 Bad Request."""
        resp = self.client.post(
            "/predict",
            data={"file": (io.BytesIO(b"data"), "")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 400)

    def test_empty_file_bytes(self):
        """POST /predict with 0-byte file must return 400 Bad Request."""
        resp = self.client.post(
            "/predict",
            data={"file": (io.BytesIO(b""), "empty.jpg")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

    def test_oversized_file(self):
        """POST /predict with file exceeding MAX_FILE_SIZE (12 MB) must return 400."""
        oversized = b"x" * (MAX_FILE_SIZE + 1024)
        resp = self.client.post(
            "/predict",
            data={"file": (io.BytesIO(oversized), "huge.jpg")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("12 MB", resp.get_json()["error"])

    def test_corrupted_image(self):
        """POST /predict with random binary garbage must return 400 Bad Request."""
        corrupt = b"\xff\xd8\xff\xe0" + os.urandom(100)
        resp = self.client.post(
            "/predict",
            data={"file": (io.BytesIO(corrupt), "corrupted.jpg")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

    def test_text_file_renamed_to_jpg(self):
        """POST /predict with plain text masquerading as JPG must be rejected."""
        fake_jpg = b"Hello, this is just plain text content masquerading as an image."
        resp = self.client.post(
            "/predict",
            data={"file": (io.BytesIO(fake_jpg), "malicious.jpg")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

    def test_extreme_dimensions_rejected(self):
        """POST /predict with 1x1 image must be rejected safely without division by zero."""
        tiny = Image.new("RGB", (1, 1), color=(255, 0, 0))
        buf = io.BytesIO()
        tiny.save(buf, format="PNG")
        buf.seek(0)

        resp = self.client.post(
            "/predict",
            data={"file": (buf, "tiny.png")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("too small", resp.get_json()["error"])

    def test_supported_image_formats(self):
        """POST /predict must safely accept valid JPEG, PNG, and WEBP formats."""
        for fmt in ["JPEG", "PNG", "WEBP"]:
            img = Image.new("RGB", (100, 100), color=(100, 150, 200))
            buf = io.BytesIO()
            img.save(buf, format=fmt)
            buf.seek(0)
            ext = "jpg" if fmt == "JPEG" else fmt.lower()
            resp = self.client.post(
                "/predict",
                data={"file": (buf, f"valid_sample.{ext}")},
                content_type="multipart/form-data"
            )
            self.assertEqual(resp.status_code, 200, f"Format {fmt} was not accepted.")

    # ── 3. Non-E-Waste Rejection Validation ──────────────────

    def test_rejection_shoe(self):
        """Shoe / footwear must be rejected as Not an E-Waste Item."""
        img = Image.new("RGB", (224, 224), color=(160, 80, 50))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        resp = self.client.post(
            "/predict",
            data={"file": (buf, "running_shoe.jpg")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["is_ewaste"])
        self.assertEqual(data["prediction"]["class"], "not_ewaste")
        self.assertEqual(data["recommendation"]["category"], "Not an E-Waste Item")

    def test_rejection_fruit(self):
        """Fruit / food produce must be rejected as Not an E-Waste Item."""
        img = Image.new("RGB", (224, 224), color=(250, 220, 50))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        resp = self.client.post(
            "/predict",
            data={"file": (buf, "fresh_banana.jpg")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["is_ewaste"])
        self.assertEqual(data["prediction"]["class"], "not_ewaste")

    def test_rejection_clothing(self):
        """Apparel / clothing must be rejected as Not an E-Waste Item."""
        img = Image.new("RGB", (224, 224), color=(40, 60, 180))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        resp = self.client.post(
            "/predict",
            data={"file": (buf, "blue_tshirt.jpg")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["is_ewaste"])
        self.assertEqual(data["prediction"]["class"], "not_ewaste")

    def test_rejection_stationery_pen(self):
        """Stationery / pen must be rejected as Not an E-Waste Item."""
        img = Image.new("RGB", (224, 224), color=(20, 20, 20))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        resp = self.client.post(
            "/predict",
            data={"file": (buf, "ballpoint_pen.jpg")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["is_ewaste"])
        self.assertEqual(data["prediction"]["class"], "not_ewaste")

    def test_rejection_plain_background(self):
        """Plain blank background with no electronics must trigger open-set rejection."""
        img = Image.new("RGB", (224, 224), color=(240, 240, 240))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        resp = self.client.post(
            "/predict",
            data={"file": (buf, "white_wall.jpg")},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["is_ewaste"])
        self.assertEqual(data["prediction"]["class"], "not_ewaste")

    # ── 4. Classification of Valid E-Waste Classes ───────────

    def _test_class_sample(self, category):
        cat_dir = os.path.join(self.dataset_dir, category)
        self.assertTrue(os.path.isdir(cat_dir), f"Directory {cat_dir} does not exist.")
        files = [f for f in os.listdir(cat_dir) if f.lower().endswith((".jpg", ".png", ".webp"))]
        self.assertTrue(len(files) > 0, f"No image files in {cat_dir}")

        img_path = os.path.join(cat_dir, files[0])
        with open(img_path, "rb") as f:
            resp = self.client.post(
                "/predict",
                data={"file": (f, f"{category}_sample.jpg")},
                content_type="multipart/form-data"
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["is_ewaste"], f"Expected {category} to be recognized as e-waste.")
        self.assertEqual(data["prediction"]["class"], category)
        self.assertTrue(data["prediction"]["confidence"] >= 85.0)

    def test_classify_battery(self):
        self._test_class_sample("battery")

    def test_classify_charger_cable(self):
        self._test_class_sample("charger_cable")

    def test_classify_circuit_board(self):
        self._test_class_sample("circuit_board")

    def test_classify_laptop(self):
        self._test_class_sample("laptop")

    def test_classify_mobile_phone(self):
        self._test_class_sample("mobile_phone")

    def test_classify_monitor_tv(self):
        self._test_class_sample("monitor_tv")

    # ── 5. Recommendations Safety & Integrity ────────────────

    def test_recommendations_safety(self):
        """Recommendations must not promote dangerous DIY smelting or acid leaching."""
        for cat, rec in RECOMMENDATIONS.items():
            self.assertIn("safety_precautions", rec)
            self.assertIn("recycling_route", rec)
            combined = (rec["recycling_route"] + " " + " ".join(rec["safety_precautions"])).lower()
            self.assertNotIn("smelt at home", combined)
            self.assertNotIn("acid bath at home", combined)
            if "burn" in combined:
                self.assertIn("never burn", combined)


if __name__ == "__main__":
    unittest.main()
