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

import torch

import requests

print(torch.version.cuda)
print(torch.cuda.is_available())


from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()


# # ✅ STEP 3: Define the input schema
# class SuggestionRequest(BaseModel):
#     ingredients: str

# # ✅ STEP 4: Load DeepSeek 7B + your LoRA adapter ONCE
# print("⏳ Loading model...")

# # Set model name
# base_model_name = "deepseek-ai/deepseek-llm-7b-base"
# lora_adapter_path = "deepseek-7b-recipe-lora2"  # local or Hugging Face repo

# # Load tokenizer
# tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)

# # Load base model
# base_model = AutoModelForCausalLM.from_pretrained(base_model_name, trust_remote_code=True)

# # Apply LoRA adapter
# model = PeftModel.from_pretrained(base_model, lora_adapter_path)

# # Move model to appropriate device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# print("✅ Model loaded!")

# inputs = tokenizer("Suggest a recipe with potatoes and cheese", return_tensors="pt").to("cpu")
# model = model.to("cpu")
# outputs = model.generate(**inputs, max_new_tokens=100)
# print(tokenizer.decode(outputs[0], skip_special_tokens=True))



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
    model_server_url = "https://f48d-35-230-120-101.ngrok-free.app/generate"

    stop_phrases = [
        "Note:", "Enjoy!", "submitted by", "Serves", "Source",
        "let me know", "Thanks for visiting", ".com", "@", "Photo credit"
    ]

    # 👤 User identifier (if available)
    user_tag = f"User: {current_user.name}" if hasattr(current_user, "name") else "User"

    # 📜 Prompt: clear, structured, and tag-delimited
    prompt = (
        f"<|user|>\n{user_tag}\n"
        f"Generate a structured recipe using ONLY these ingredients: {request.ingredients}. "
        "Only provide:\n"
        "- A recipe title\n"
        "- Ingredients list\n"
        "- Step-by-step instructions\n"
        "<|assistant|>"
    )

    # 🧠 Generation settings
    payload = {
        "prompt": prompt,
        "max_new_tokens": 300,
        "do_sample": True,
        "top_k": 40,
        "top_p": 0.92,
        "temperature": 0.7,
        "repetition_penalty": 1.15
    }

    try:
        response = requests.post(model_server_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with model server: {str(e)}")

    generated_text = response.json().get("generated_text", "").strip()

    if not generated_text:
        raise HTTPException(status_code=500, detail="Empty response from model server")

    # 🧹 Extract just the assistant reply
    recipe = generated_text.split("<|assistant|>")[-1].strip()

    # 🚫 Remove stop phrases (truncation cleanup)
    for phrase in stop_phrases:
        if phrase in recipe:
            recipe = recipe.split(phrase)[0].strip()

    # 📝 Save the generated recipe
    new_recipe = Recipe(
        title=request.ingredients[:100],  # Placeholder title or parse one from `recipe` if needed
        description=recipe
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    # 📌 Log suggestion
    suggestion = UserRecipeSuggestion(
        user_id=current_user.id,
        recipe_id=new_recipe.id,
        ingredients_input=request.ingredients,
        timestamp=datetime.utcnow()
    )
    db.add(suggestion)
    db.commit()

    return {
        "recipes": [{
            "title": new_recipe.title,
            "description": new_recipe.description,
            "recipe_id": new_recipe.id
        }]
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




from pydantic import BaseModel

class LikeDislikeRequest(BaseModel):
    suggestion_id: int
    liked: bool  # True for Like, False for Dislike

from sqlalchemy import and_

@app.post("/suggestion/feedback/")
def give_feedback(
    feedback: LikeDislikeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find the suggestion by recipe ID + user ID
    suggestion = db.query(UserRecipeSuggestion).filter(
        UserRecipeSuggestion.recipe_id == feedback.suggestion_id,
        UserRecipeSuggestion.user_id == current_user.id
    ).first()

    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    # Check if the recipe was already liked by this user
    already_liked = db.query(UserRecipeSuggestion).filter(
        and_(
            UserRecipeSuggestion.recipe_id == suggestion.recipe_id,
            UserRecipeSuggestion.user_id == current_user.id,
            UserRecipeSuggestion.liked == 1
        )
    ).first()

    if feedback.liked:
        if already_liked:
            return {"message": "Already liked"}
        suggestion.liked = 1
    else:
        suggestion.liked = 0

    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)

    return {"message": f"Recipe {'liked' if feedback.liked else 'disliked'} successfully"}



@app.get("/user/liked_recipes/")
def get_liked_recipes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    liked = (
        db.query(UserRecipeSuggestion)
        .filter(
            UserRecipeSuggestion.user_id == current_user.id,
            UserRecipeSuggestion.liked == 1
        )
        .order_by(UserRecipeSuggestion.timestamp.desc())  # sort newest first
        .all()
    )

    return [
        {
            "suggestion_id": l.id,
            "title": l.recipe.title if l.recipe else "Unknown",
            "description": l.recipe.description if l.recipe else "",
            "ingredients_used": l.ingredients_input,
            "suggested_at": l.timestamp
        }
        for l in liked
    ]





from sqlalchemy import func

@app.get("/user/disliked_recipes/")
def get_disliked_recipes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # ✅ Step 1: Get latest feedback for each recipe for this user
    subquery = (
        db.query(
            UserRecipeSuggestion.recipe_id,
            func.max(UserRecipeSuggestion.timestamp).label("max_time")
        )
        .filter(UserRecipeSuggestion.user_id == current_user.id)
        .group_by(UserRecipeSuggestion.recipe_id)
        .subquery()
    )

    # ✅ Step 2: Now find actual records matching these latest feedback
    disliked = (
        db.query(UserRecipeSuggestion)
        .join(subquery, (UserRecipeSuggestion.recipe_id == subquery.c.recipe_id) & (UserRecipeSuggestion.timestamp == subquery.c.max_time))
        .join(Recipe, Recipe.id == UserRecipeSuggestion.recipe_id)
        .filter(UserRecipeSuggestion.liked == 0)  # ✅ Only the latest feedback being dislike
        .all()
    )

    # ✅ Step 3: Return clean results
    return [
        {
            "suggestion_id": d.id,
            "title": d.recipe.title,
            "description": d.recipe.description,
            "ingredients_used": d.ingredients_input,
            "suggested_at": d.timestamp
        }
        for d in disliked
    ]

