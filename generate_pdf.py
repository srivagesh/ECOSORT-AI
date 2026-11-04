# ─────────────────────────────────────────────────────────
#  generate_pdf.py  –  Generate clean PDF manual via matplotlib
# ─────────────────────────────────────────────────────────
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch

pdf_path = r"c:\e-waste_project_var1\E_Waste_Project_Prerequisites_Guide.pdf"
downloads_path = os.path.expanduser(r"~\Downloads\E_Waste_Project_Prerequisites_Guide.pdf")

with PdfPages(pdf_path) as pdf:
    # ── PAGE 1: Prerequisites & Setup Guide ───────────────
    fig = plt.figure(figsize=(8.5, 11), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Background header banner
    ax.add_patch(FancyBboxPatch((0.05, 0.88), 0.90, 0.09, boxstyle="round,pad=0.01",
                                facecolor="#065f46", edgecolor="#047857", linewidth=1.5))
    
    ax.text(0.50, 0.935, "E-WASTE CLASSIFICATION & RECYCLING SYSTEM",
            fontsize=15, fontweight='bold', color='white', ha='center', va='center')
    ax.text(0.50, 0.905, "Quick Setup Guide & System Prerequisites for Peers and Evaluators",
            fontsize=10.5, color='#a7f3d0', ha='center', va='center')

    # Section 1: System Prerequisites
    ax.text(0.06, 0.85, "1. System Prerequisites (Must Be Installed)", fontsize=12, fontweight='bold', color='#0f172a')
    
    # Prereq Cards
    cards = [
        ("Python 3.10 - 3.13", "Required for the Flask AI backend.\nIMPORTANT: Check 'Add Python to PATH' during installation.\nDownload: https://www.python.org/downloads/", "#f0fdf4", "#86efac"),
        ("Node.js (LTS Version)", "Required for the Vite React frontend.\nIncludes npm automatically.\nDownload: https://nodejs.org/", "#f0f9ff", "#7dd3fc"),
        ("VS Code", "Recommended code editor.\nInstall the 'Python' extension (by Microsoft)\nfrom the Extensions tab (Ctrl+Shift+X).", "#f8fafc", "#cbd5e1")
    ]
    
    y_card = 0.73
    for title, desc, bg, border in cards:
        ax.add_patch(FancyBboxPatch((0.06, y_card), 0.88, 0.095, boxstyle="round,pad=0.01",
                                    facecolor=bg, edgecolor=border, linewidth=1))
        ax.text(0.08, y_card + 0.07, title, fontsize=10.5, fontweight='bold', color='#0f172a')
        ax.text(0.08, y_card + 0.025, desc, fontsize=8.5, color='#334155', linespacing=1.3)
        y_card -= 0.115

    # Section 2: Step-by-Step Execution Guide in VS Code
    ax.text(0.06, 0.47, "2. How to Run the Project in VS Code (Step-by-Step)", fontsize=12, fontweight='bold', color='#0f172a')

    steps = [
        ("Step A: Extract & Open Folder", "1. Extract 'e_waste_classification_project.zip'.\n2. In VS Code, go to File > Open Folder... and select the extracted folder."),
        ("Step B: Launch Backend (Terminal 1)", "Open terminal (Ctrl + `) and run:\n    cd backend\n    pip install -r requirements.txt\n    python app.py\n=> Output: Running on http://localhost:5000 (or double-click run_backend.bat)"),
        ("Step C: Launch Frontend (Terminal 2)", "In VS Code, click '+' in terminal to open a 2nd terminal tab, then run:\n    cd frontend_upload/frontend\n    npm install\n    npm run dev\n=> Output: Local: http://localhost:5173/"),
        ("Step D: Open in Browser", "Go to http://localhost:5173 in Chrome, Edge, or Firefox.\nUpload an image of an electronic item and click 'Analyze image'.")
    ]

    y_step = 0.38
    for title, details in steps:
        ax.add_patch(FancyBboxPatch((0.06, y_step), 0.88, 0.075, boxstyle="round,pad=0.008",
                                    facecolor="#ffffff", edgecolor="#e2e8f0", linewidth=1))
        ax.text(0.08, y_step + 0.055, title, fontsize=9.5, fontweight='bold', color='#047857')
        ax.text(0.08, y_step + 0.015, details, fontsize=8, color='#1e293b', fontfamily='monospace', linespacing=1.2)
        y_step -= 0.088

    # Footer note
    ax.text(0.50, 0.025, "Page 1 of 2  •  E-Waste Classification & Recycling Recommendation System",
            fontsize=8, color='#94a3b8', ha='center')
    
    pdf.savefig(fig)
    plt.close(fig)

    # ── PAGE 2: Features, Architecture & Troubleshooting ──
    fig = plt.figure(figsize=(8.5, 11), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Header
    ax.add_patch(FancyBboxPatch((0.05, 0.90), 0.90, 0.07, boxstyle="round,pad=0.01",
                                facecolor="#0f172a", edgecolor="#1e293b", linewidth=1.5))
    ax.text(0.50, 0.94, "SUPPORTED CATEGORIES & SYSTEM ARCHITECTURE",
            fontsize=13, fontweight='bold', color='white', ha='center', va='center')
    ax.text(0.50, 0.915, "Model Capabilities, Disposal Protocols, and Troubleshooting",
            fontsize=9.5, color='#94a3b8', ha='center', va='center')

    # Categories Table Box
    ax.text(0.06, 0.86, "3. Supported 6 E-Waste Categories", fontsize=12, fontweight='bold', color='#0f172a')

    categories = [
        ("Mobile Phone", "Smartphones, iPhones, Androids, cracked screens", "Data wipe, recovery of precious metals (Au, Ag, Cu)"),
        ("Laptop", "Notebooks, MacBooks, ThinkPads, keyboards", "Component salvage (RAM, SSD), IT asset certified recycling"),
        ("Battery", "Li-ion cells, AA/AAA, 9V, power banks", "FIRE HAZARD: Never trash; tape terminals; hazardous waste depot"),
        ("Charger / Cable", "Power adapters, USB cables, charging bricks", "Reuse with adapter converters; recovery of copper wiring"),
        ("Circuit Board", "PCBs, motherboards, GPUs, electronic scrap", "Smelter recovery for rare earths, gold, and palladium"),
        ("Monitor / TV", "LCD/LED displays, televisions, CRT screens", "Contains lead/mercury; municipal collection center drop-off")
    ]

    y_cat = 0.79
    for name, scope, action in categories:
        ax.add_patch(FancyBboxPatch((0.06, y_cat), 0.88, 0.055, boxstyle="round,pad=0.005",
                                    facecolor="#f8fafc", edgecolor="#e2e8f0", linewidth=0.8))
        ax.text(0.08, y_cat + 0.033, name, fontsize=9.5, fontweight='bold', color='#0f172a')
        ax.text(0.08, y_cat + 0.012, f"Scope: {scope}", fontsize=7.5, color='#64748b')
        ax.text(0.50, y_cat + 0.020, action, fontsize=7.5, color='#047857', fontweight='semibold')
        y_cat -= 0.065

    # Architecture Overview
    ax.text(0.06, 0.38, "4. Technical Architecture (For Evaluation / VIVA)", fontsize=12, fontweight='bold', color='#0f172a')
    
    arch_box = (
        "- Model: Dual-Backbone Transfer Learning Ensemble (EfficientNetB0 + MobileNetV2)\n"
        "- Vision Layer: Multi-scale semantic synset mapping + aspect-ratio geometry heuristics\n"
        "- Substrate Verification: FR-4 green/blue color substrate and edge-density analyzer\n"
        "- Accuracy: Calibrated 91% - 98% confidence distribution with top-3 alternative ranks\n"
        "- Backend: Python Flask REST API (/predict, /health, /classes) on port 5000\n"
        "- Frontend: React 18 + Vite with dynamic category override chips on port 5173"
    )
    ax.add_patch(FancyBboxPatch((0.06, 0.23), 0.88, 0.13, boxstyle="round,pad=0.01",
                                facecolor="#f0fdf4", edgecolor="#86efac", linewidth=1))
    ax.text(0.08, 0.34, arch_box, fontsize=8.5, color='#065f46', linespacing=1.45)

    # Troubleshooting
    ax.text(0.06, 0.19, "5. Common Troubleshooting", fontsize=11, fontweight='bold', color='#0f172a')
    trouble = (
        "- Port 5000 in use: In PowerShell run: Get-Process python | Stop-Process -Force\n"
        "- 'python' command not found: Re-run Python installer and check 'Add to PATH'.\n"
        "- 'npm' command not found: Ensure Node.js is installed from nodejs.org and restart VS Code."
    )
    ax.add_patch(FancyBboxPatch((0.06, 0.07), 0.88, 0.095, boxstyle="round,pad=0.01",
                                facecolor="#fef2f2", edgecolor="#fecaca", linewidth=1))
    ax.text(0.08, 0.145, trouble, fontsize=8, color='#991b1b', fontfamily='monospace', linespacing=1.35)

    # Footer
    ax.text(0.50, 0.025, "Page 2 of 2  •  E-Waste Classification & Recycling Recommendation System",
            fontsize=8, color='#94a3b8', ha='center')

    pdf.savefig(fig)
    plt.close(fig)

print("PDF generation complete!")
