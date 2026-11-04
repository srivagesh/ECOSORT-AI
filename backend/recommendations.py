# ─────────────────────────────────────────────────────────
#  recommendations.py  –  Category → Recycling Guidance
# ─────────────────────────────────────────────────────────

RECOMMENDATIONS = {
    "mobile_phone": {
        "category": "Mobile Phone",
        "icon": "📱",
        "confidence_label": "Mobile Phone / Smartphone",
        "recycling_route": (
            "Take to an authorized e-waste collection centre or a mobile "
            "retailer that accepts trade-ins. Many carriers and manufacturers "
            "run mail-back programmes."
        ),
        "safety_precautions": [
            "Remove the SIM card and wipe personal data before recycling.",
            "Do not puncture or crush the lithium-ion battery.",
            "If the battery is swollen, place the device in a fireproof bag and hand it to a certified handler.",
        ],
        "reuse_suggestions": [
            "If the device powers on, consider donating it or selling it second-hand.",
            "A cracked screen can often be repaired affordably.",
            "Old phones make great backup cameras, music players, or remotes.",
        ],
        "environmental_impact": (
            "One recycled mobile phone can recover copper, silver, gold, "
            "palladium and platinum — reducing the need for destructive mining."
        ),
    },
    "laptop": {
        "category": "Laptop",
        "icon": "💻",
        "confidence_label": "Laptop / Notebook Computer",
        "recycling_route": (
            "Drop off at an authorised e-waste facility. Many manufacturers "
            "offer free take-back programmes. Hard drives should be securely "
            "erased or physically destroyed for data safety."
        ),
        "safety_precautions": [
            "Remove or securely erase the hard drive / SSD before recycling.",
            "Handle with care if the screen is cracked — LCD panels may contain mercury.",
            "Detach the battery if removable; never dispose of lithium batteries in regular waste.",
        ],
        "reuse_suggestions": [
            "If it boots, install a lightweight Linux distro for basic tasks.",
            "Donate to schools, nonprofits, or community organisations.",
            "Individual components (RAM, SSD, charger) may still be valuable.",
        ],
        "environmental_impact": (
            "A laptop contains recoverable aluminium, copper, steel and "
            "precious metals. Proper recycling prevents heavy-metal soil "
            "and water contamination."
        ),
    },
    "battery": {
        "category": "Battery",
        "icon": "🔋",
        "confidence_label": "Battery (Li-ion / NiMH / Lead-acid)",
        "recycling_route": (
            "Never place batteries in household waste. Use dedicated battery "
            "recycling drop-off points at electronics stores, supermarkets, or "
            "municipal collection events."
        ),
        "safety_precautions": [
            "Tape the terminals of lithium batteries before disposal to prevent short circuits.",
            "Do not expose to heat, fire, or water.",
            "Swollen or damaged batteries should be placed in sand or a fireproof container.",
            "Wear gloves when handling leaking batteries.",
        ],
        "reuse_suggestions": [
            "Some batteries can be reconditioned — check with a local battery service.",
            "Intact batteries from old devices may still power compatible gadgets.",
        ],
        "environmental_impact": (
            "Batteries contain cadmium, lead, lithium, and cobalt. Improper "
            "disposal leaches toxins into soil and groundwater. Recycling "
            "recovers up to 95% of materials."
        ),
    },
    "charger_cable": {
        "category": "Charger / Cable",
        "icon": "🔌",
        "confidence_label": "Charger, Power Adapter, or Cable",
        "recycling_route": (
            "Collect cables and chargers and drop them at an e-waste bin or "
            "recycling centre. Some electronics retailers accept them in-store."
        ),
        "safety_precautions": [
            "Do not cut or strip cables yourself — they may still carry residual charge.",
            "Inspect for exposed wires or melted insulation before handling.",
        ],
        "reuse_suggestions": [
            "Working chargers can often be donated or given away.",
            "Universal adapters may fit other devices — check compatibility.",
            "Coil and store unused but working cables for future use.",
        ],
        "environmental_impact": (
            "Cables contain copper, PVC, and sometimes tin. Recycling "
            "copper from cables is far less energy-intensive than mining new ore."
        ),
    },
    "circuit_board": {
        "category": "Circuit Board",
        "icon": "🖥️",
        "confidence_label": "Printed Circuit Board (PCB)",
        "recycling_route": (
            "Circuit boards contain the highest concentration of precious "
            "metals in e-waste. Take them to a specialised e-waste recycler — "
            "never burn or dump them."
        ),
        "safety_precautions": [
            "Handle with anti-static precautions if components may be reused.",
            "Some older boards contain lead solder — wash hands after handling.",
            "Do not attempt to extract metals at home; the chemicals required are hazardous.",
        ],
        "reuse_suggestions": [
            "Functional boards can be repurposed in DIY electronics projects.",
            "Components like capacitors, ICs, and connectors can be salvaged.",
        ],
        "environmental_impact": (
            "One tonne of circuit boards can yield more gold than 17 tonnes "
            "of gold ore. Responsible recycling prevents toxic runoff from "
            "lead, mercury, and brominated flame retardants."
        ),
    },
    "monitor_tv": {
        "category": "Monitor / TV",
        "icon": "🖥️",
        "confidence_label": "Monitor or Television",
        "recycling_route": (
            "Monitors and TVs are classified as hazardous e-waste in many "
            "regions. Contact your local municipality or use manufacturer "
            "take-back schemes. Never leave them at the curbside."
        ),
        "safety_precautions": [
            "CRT monitors contain lead — handle carefully and do not break the glass.",
            "LCD screens may contain mercury backlights in older models.",
            "Wear gloves if the screen is cracked.",
        ],
        "reuse_suggestions": [
            "A working monitor can be donated to schools, libraries, or community centres.",
            "Old monitors can serve as secondary displays for productivity setups.",
        ],
        "environmental_impact": (
            "A single CRT monitor can contain up to 2 kg of lead. Proper "
            "recycling prevents this from contaminating landfills and water supplies."
        ),
    },
    "not_ewaste": {
        "category": "Not an E-Waste Item",
        "icon": "🚫",
        "confidence_label": "Not E-Waste",
        "recycling_route": (
            "This item is NOT electronic waste. "
            "Please dispose of it via municipal solid waste, textile/footwear recycling, "
            "or donate wearable items to a local charity or thrift store."
        ),
        "safety_precautions": [
            "Do not dispose of non-electronic items into dedicated e-waste collection bins.",
            "If this item has an embedded battery or electronic circuit (e.g., smart/LED shoes, lighted apparel), please manually select 'Battery' or 'Circuit Board' above.",
            "Keep general solid waste and organic waste segregated from hazardous e-waste streams.",
        ],
        "reuse_suggestions": [
            "If in good or wearable condition, donate footwear, clothing, or household goods to local charities.",
            "Check for brand take-back programs (many athletic shoe brands recycle rubber and foam soles into running tracks or playground surfaces).",
            "Consider repair or resoling before discarding.",
        ],
        "environmental_impact": (
            "Dedicated e-waste facilities use specialized smelting, leaching, and shredding "
            "processes designed strictly for printed circuit boards and electronic devices. "
            "Introducing non-electronic municipal waste contaminates the recycling stream and damages sorting machinery."
        ),
    },
}

# Ordered list matching model output indices
CLASS_LABELS = [
    "battery",
    "charger_cable",
    "circuit_board",
    "laptop",
    "mobile_phone",
    "monitor_tv",
]


def get_recommendation(predicted_class: str, detected_object: str = None) -> dict:
    """Return the full recommendation dict for a predicted class label."""
    rec = dict(RECOMMENDATIONS.get(predicted_class, {
        "category": predicted_class.replace("_", " ").title(),
        "icon": "♻️",
        "confidence_label": predicted_class.replace("_", " ").title(),
        "recycling_route": "Please consult your local e-waste collection centre.",
        "safety_precautions": ["Handle electronic waste with care."],
        "reuse_suggestions": ["Check if the item is still functional before recycling."],
        "environmental_impact": "Recycling e-waste reduces landfill pollution and recovers valuable materials.",
    }))
    if detected_object:
        rec["detected_object"] = detected_object
    return rec
