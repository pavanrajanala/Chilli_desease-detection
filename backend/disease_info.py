"""
Static reference information shown alongside model predictions.
This is general educational info, NOT a substitute for expert agricultural advice.
"""

DISEASE_INFO = {
    "Healthy_Leaf": {
        "display_name": "Healthy",
        "symptoms": "No visible spots, discoloration, curling, or powdery residue. Leaf color and shape look normal.",
        "recommendation": "No action needed. Keep monitoring your plants weekly, especially after rain or humid spells."
    },
    "Bacterial_Spot": {
        "display_name": "Bacterial Leaf Spot",
        "symptoms": "Small, water-soaked spots that turn dark brown/black with a yellow halo, often with irregular edges.",
        "recommendation": "Avoid overhead watering, remove and destroy affected leaves, improve air circulation, and consider a copper-based bactericide. Consult a local agricultural expert if it spreads."
    },
    "Cercospora_Leaf_Spot": {
        "display_name": "Cercospora Leaf Spot (Frog-eye spot)",
        "symptoms": "Circular grey/tan spots with a dark brown border, resembling a frog's eye; older leaves may yellow and drop.",
        "recommendation": "Remove heavily infected leaves, avoid wetting foliage while watering, and consider a fungicide labeled for Cercospora if it is spreading. Verify with an expert before repeated fungicide use."
    },
    "Curl_Virus": {
        "display_name": "Leaf Curl (Viral)",
        "symptoms": "Upward/downward curling of leaves, crinkling, stunted growth, and sometimes yellowing along veins. Often spread by whiteflies.",
        "recommendation": "Control whitefly populations (yellow sticky traps, neem-based sprays), remove severely affected plants to reduce spread, and avoid planting near infected fields. No cure once infected — focus on prevention for new growth."
    },
    "Nutrition_Deficiency": {
        "display_name": "Nutrient Deficiency (not an infectious disease)",
        "symptoms": "Yellowing (often between veins), pale or stunted leaves, without the spotting or curling typical of infections.",
        "recommendation": "Check soil nutrition (especially nitrogen, magnesium, iron) and watering consistency. A balanced fertilizer or soil test is usually more useful here than a fungicide/pesticide."
    },
    "Powdery_Mildew": {
        "display_name": "Powdery Mildew",
        "symptoms": "White/greyish powdery coating on the leaf surface, sometimes with mild yellowing underneath.",
        "recommendation": "Improve air circulation, avoid excess nitrogen fertilizer, and consider a sulfur-based or neem-based fungicide. Isolate affected plants if possible."
    },
}

GENERAL_DISCLAIMER = (
    "This result is from an AI-based preliminary screening tool and is not a guaranteed "
    "diagnosis. Leaf symptoms can have multiple causes (disease, pests, nutrient issues, "
    "environmental stress). For valuable crops or persistent symptoms, please consult a "
    "local agricultural extension officer or plant pathologist."
)


def get_info(class_name: str) -> dict:
    """Return symptom/recommendation info for a class name, with a safe fallback."""
    return DISEASE_INFO.get(
        class_name,
        {
            "display_name": class_name.replace("_", " "),
            "symptoms": "No reference information available for this class yet.",
            "recommendation": "Consider consulting an agricultural expert for confirmation.",
        },
    )
