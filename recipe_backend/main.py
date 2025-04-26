from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define the structure of feedback request
class FeedbackRequest(BaseModel):
    recipe_text: str
    rating: int  # from 1 to 5

# Endpoint to collect feedback
@app.post("/feedback")
async def collect_feedback(feedback: FeedbackRequest):
    # Save feedback to a text file
    with open("feedback_log.txt", "a") as f:
        f.write(f"{feedback.recipe_text} | Rating: {feedback.rating}\n")
    return {"message": "Thanks for your feedback!"}
