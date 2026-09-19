from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="Nimra AI Persona Backend")

# Add CORS Middleware so your future frontend (Vue.js / Next.js) can communicate with it safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits requests from any development port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the exact incoming structure expected from the client
class ChatRequest(BaseModel):
    prompt: str

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "nimra-ai"

# Simple home route to verify the API is alive in the browser
@app.get("/")
def home():
    return {"status": "FastAPI is running successfully! Go to /docs to test your model."}

# The main endpoint handling your AI generation requests
@app.post("/api/chat")
async def chat_with_persona(payload: ChatRequest):
    try:
        # Format payload structure explicitly for the local Ollama backend service
        ollama_payload = {
            "model": MODEL_NAME,
            "prompt": payload.prompt,
            "stream": False
        }
        
        # Call the local Ollama instance running on your computer
        response = requests.post(OLLAMA_API_URL, json=ollama_payload)
        response.raise_for_status()
        
        response_data = response.json()
        return {"response": response_data.get("response")}
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Could not connect to Ollama. Make sure 'ollama run {MODEL_NAME}' is open in a separate terminal. Error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    # Starts your server application locally
    uvicorn.run(app, host="127.0.0.1", port=8000)