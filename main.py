from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RISK_KEYWORDS = {
    "medical_claims": [
        "cure", "treat", "heal", "diagnose", "medical", "doctor approved"
    ],
    "guarantees": [
        "guaranteed", "100%", "instant results", "no risk"
    ],
    "personal_attributes": [
        "you are", "your condition", "suffering from", "struggling with"
    ],
    "financial_claims": [
        "make money", "earn", "profit", "income", "get rich"
    ]
}

@app.post("/scan")
async def scan_creative(
    file: UploadFile,
    headline: str = Form(...),
    primary_text: str = Form(...),
    description: str = Form(""),
    category: str = Form(...)
):
    text = f"{headline} {primary_text} {description}".lower()

    flags = []
    score = 0

    for rule, keywords in RISK_KEYWORDS.items():
        for word in keywords:
            if word in text:
                flags.append({
                    "type": rule,
                    "keyword": word
                })
                score += 15

    score = min(score, 100)

    risk = "Low" if score < 30 else "Medium" if score < 60 else "High"

    return {
        "risk_level": risk,
        "risk_score": score,
        "flags": flags,
        "recommendations": [
            "Avoid medical or financial claims.",
            "Remove guarantees or absolute language.",
            "Rewrite copy to be educational, not outcome-driven.",
            "Avoid referencing personal attributes."
        ]
  }
