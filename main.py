from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from models import Base, User, UserPreferences
from auth import hash_password, verify_password, create_access_token
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
from fastapi import Form
from fastapi import Response
from models import Recipe, UserRecipeSuggestion
from datetime import datetime

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

import torch

print(torch.version.cuda)
print(torch.cuda.is_available())


Base.metadata.create_all(bind=engine)  # Create tables automatically

app = FastAPI()


# ✅ STEP 3: Define the input schema
class SuggestionRequest(BaseModel):
    ingredients: str

# ✅ STEP 4: Load DeepSeek 7B + your LoRA adapter ONCE
print("⏳ Loading model...")

# Set model name
base_model_name = "deepseek-ai/deepseek-llm-7b-base"
lora_adapter_path = "deepseek-7b-recipe-lora2"  # local or Hugging Face repo

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(base_model_name, trust_remote_code=True)

# Apply LoRA adapter
model = PeftModel.from_pretrained(base_model, lora_adapter_path)

# Move model to appropriate device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

print("✅ Model loaded!")

inputs = tokenizer("Suggest a recipe with potatoes and cheese", return_tensors="pt").to("cpu")
model = model.to("cpu")
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))



# Function to authenticate the user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "a94d5f0e4e1b2f85e2c5d7a97d26fae3a23456789abcdef1234567890abcdef"  # Must match the key used in login
ALGORITHM = "HS256"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Both origins
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Extract user from JWT
from fastapi import Cookie

from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(request: Request, db: Session = Depends(get_db)):
    
    token = request.cookies.get("access_token")
    print(f"Cookie received: {token}")  # Debugging line    
    print(f"All cookies received: {request.cookies}")  # Debug all cookies
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    
    try:
        # Strip "Bearer " prefix if it exists
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        
        print(f"Token received: {token}")  # Debugging line
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Token payload: {payload}")  # Debugging line
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError as e:
        print(f"JWTError: {e}")  # Debugging line
        raise HTTPException(status_code=401, detail="Invalid token")

    
# Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class DietaryPreferencesUpdate(BaseModel):
    dietary_preferences: str
    allergies: str
    disliked_ingredients: str

# Register User
@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# Login API
@app.post("/login/")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):  
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token({"sub": str(user.id)})
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False,       # False for HTTP (no HTTPS)
        samesite="Lax",     # Use "Lax" for HTTP (not "None")
        path="/",
    )



    return {"message": "Login successful"}

# Get User Profile (Authenticated)
@app.get("/user/profile/")
def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }

# Get User Preferences (Authenticated)
@app.get("/user/preferences/")
def get_user_preferences(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_preferences = db.query(UserPreferences).filter(UserPreferences.user_id == current_user.id).first()
    
    if not db_preferences:
        raise HTTPException(status_code=404, detail="User preferences not found")

    return {
        "user_id": db_preferences.user_id,
        "dietary_preferences": db_preferences.dietary_preferences,
        "allergies": db_preferences.allergies,
        "disliked_ingredients": db_preferences.disliked_ingredients
    }

# Update User Preferences (Authenticated)
@app.put("/user/preferences/")
def update_preferences(
    preferences: DietaryPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_preferences = db.query(UserPreferences).filter(UserPreferences.user_id == current_user.id).first()

    if not db_preferences:
        # Create new preferences if none exist
        new_preferences = UserPreferences(
            user_id=current_user.id,
            dietary_preferences=preferences.dietary_preferences or "",
            allergies=preferences.allergies or "",
            disliked_ingredients=preferences.disliked_ingredients or ""
        )
        db.add(new_preferences)
        db.commit()
        db.refresh(new_preferences)
        return {
            "message": "Preferences created successfully",
            "preferences": {
                "dietary_preferences": new_preferences.dietary_preferences,
                "allergies": new_preferences.allergies,
                "disliked_ingredients": new_preferences.disliked_ingredients
            }
        }

    # Update existing preferences
    db_preferences.dietary_preferences = preferences.dietary_preferences or db_preferences.dietary_preferences
    db_preferences.allergies = preferences.allergies or db_preferences.allergies
    db_preferences.disliked_ingredients = preferences.disliked_ingredients or db_preferences.disliked_ingredients
    db.commit()
    db.refresh(db_preferences)

    return {
        "message": "Preferences updated successfully",
        "preferences": {
            "dietary_preferences": db_preferences.dietary_preferences,
            "allergies": db_preferences.allergies,
            "disliked_ingredients": db_preferences.disliked_ingredients
        }
    }

# Add this with other Pydantic models
class SuggestionRequest(BaseModel):
    ingredients: str

# Add this near the bottom with the other routes
@app.post("/suggest/")
async def suggest_recipe(
    request: SuggestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fake recipe results (to be replaced later with real model output)
    fake_results = [
        {"title": "Spaghetti Aglio e Olio", "description": "Simple pasta with garlic, olive oil, and chili flakes."},
        {"title": "Veggie Stir Fry", "description": "Mixed vegetables sautéed in soy sauce and ginger."},
        {"title": "Tomato Basil Soup", "description": "Creamy tomato soup with fresh basil and garlic."},
    ]

    saved_recipes = []
    for result in fake_results:
        # Check if recipe already exists in DB
        recipe = db.query(Recipe).filter(Recipe.title == result["title"]).first()
        if not recipe:
            recipe = Recipe(title=result["title"], description=result["description"])
            db.add(recipe)
            db.commit()
            db.refresh(recipe)

        # Save suggestion to user history
        suggestion = UserRecipeSuggestion(
            user_id=current_user.id,
            recipe_id=recipe.id,
            ingredients_input=request.ingredients,
            timestamp=datetime.utcnow()
        )
        db.add(suggestion)
        saved_recipes.append(recipe)

    db.commit()

    return {
        "recipes": [{"title": r.title, "description": r.description} for r in saved_recipes]
    }

@app.get("/user/history/")
def get_user_suggestion_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    history = (
        db.query(UserRecipeSuggestion)
        .join(Recipe, Recipe.id == UserRecipeSuggestion.recipe_id)
        .filter(UserRecipeSuggestion.user_id == current_user.id)
        .order_by(UserRecipeSuggestion.timestamp.desc())
        .all()
    )

    return [
        {
            "title": h.recipe.title,
            "description": h.recipe.description,
            "ingredients_used": h.ingredients_input,
            "suggested_at": h.timestamp
        }
        for h in history
    ]



@app.post("/logout/")
async def logout(response: Response):
    response.delete_cookie("access_token")  # ✅ Provide the cookie key
    return {"message": "Logged out successfully"}

