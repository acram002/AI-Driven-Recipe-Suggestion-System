from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    preferences = relationship("UserPreferences", back_populates="user", uselist=False)

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dietary_preferences = Column(String(255))
    allergies = Column(String(255))
    disliked_ingredients = Column(String(255))

    user = relationship("User", back_populates="preferences")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

class UserRecipeSuggestion(Base):
    __tablename__ = "user_recipe_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    ingredients_input = Column(String(255))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="recipe_suggestions")
    recipe = relationship("Recipe")