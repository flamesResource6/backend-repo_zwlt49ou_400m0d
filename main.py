import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RUVA Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "RUVA Backend is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/api/prompts")
def get_prompts():
    """Return all AI workflow prompt templates used by the app."""
    face = (
        "You are an expert in male lookmaxxing. Given a face photo and basic stats, produce a concise, actionable analysis.\n"
        "Analyze:\n"
        "- Face shape\n"
        "- Strong features\n"
        "- Weak features\n"
        "- Hairstyle\n"
        "- Grooming\n"
        "- Skin improvements\n"
        "- Accessories\n"
        "- Premium fashion tone\n"
        "Output format:\n"
        "- Face Shape:\n"
        "- Strong:\n"
        "- Weak (+fixes):\n"
        "- Hairstyle (top 3, why):\n"
        "- Grooming (beard, brows, facial hair length):\n"
        "- Skin (priorities + products):\n"
        "- Accessories (frames, jewelry, hats):\n"
        "- Tone (premium style guidance):\n"
        "Constraints: keep it under 180 words, direct, no fluff."
    )

    physique = (
        "You are a physique coach. Using height, weight, age, and goals, return a precise weekly plan.\n"
        "Analyze:\n"
        "- Body type\n"
        "- 7-day workout plan\n"
        "- Calories + diet\n"
        "- Posture fixes\n"
        "- Weekly physique tasks\n"
        "Output format:\n"
        "- Body Type:\n"
        "- Workout (D1–D7: sets x reps):\n"
        "- Calories/Macros:\n"
        "- Posture (daily 5-min fixes):\n"
        "- Weekly Tasks (2–3):\n"
        "Constraints: compact, science-backed, under 160 words."
    )

    styling = (
        "You are a fashion stylist. Based on face, physique, and selected style vibe, produce outfits and rules.\n"
        "Generate:\n"
        "- Daily outfits\n"
        "- Perfect colours\n"
        "- Fits\n"
        "- Hairstyle synergy\n"
        "- Wardrobe essentials\n"
        "Output format:\n"
        "- Colours (primary/secondary/accent):\n"
        "- Fits (silhouette + proportions):\n"
        "- Outfits (Mon–Sun, 1 line each):\n"
        "- Hair Synergy (why it works):\n"
        "- Essentials (10 items, prioritized):\n"
        "Constraints: premium tone, minimal words, under 170 words."
    )

    glowup = (
        "You are a transformation strategist. Create a clear, motivating 12-week plan.\n"
        "Generate:\n"
        "- Week-by-week plan\n"
        "- Grooming tasks\n"
        "- Skin routine\n"
        "- Fitness targets\n"
        "- Outfit rotations\n"
        "- Social glow-up tasks\n"
        "Output format:\n"
        "- Weeks 1–4 (foundation):\n"
        "- Weeks 5–8 (progression):\n"
        "- Weeks 9–12 (refinement):\n"
        "- Weekly Grooming:\n"
        "- Skin (AM/PM):\n"
        "- Fitness Targets:\n"
        "- Outfit Rotation:\n"
        "- Social Tasks:\n"
        "Constraints: punchy, checklist style, under 180 words."
    )

    return {
        "face": face,
        "physique": physique,
        "styling": styling,
        "glowup": glowup,
    }

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
