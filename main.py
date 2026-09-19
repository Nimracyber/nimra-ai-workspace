from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests

app = FastAPI(title="Nimra AI Persona Interface")

# Pydantic schema for strict JSON request checking
class ChatRequest(BaseModel):
    prompt: str

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "nimra-ai"

# 1. FRONTEND: Renders a beautiful chat application right in the browser
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nimra AI Persona Companion</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            body { background-color: #1e1e2e; display: flex; justify-content: center; align-items: center; height: 100vh; color: #cdd6f4; }
            .chat-container { width: 100%; max-width: 650px; height: 85vh; background-color: #252538; border-radius: 12px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.3); border: 1px solid #45475a; }
            .chat-header { background-color: #11111b; padding: 20px; text-align: center; border-bottom: 1px solid #45475a; }
            .chat-header h2 { font-size: 1.4rem; color: #cba6f7; }
            .chat-header p { font-size: 0.85rem; color: #a6adc8; margin-top: 4px; }
            .messages-box { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
            .message { max-width: 80%; padding: 12px 16px; border-radius: 14px; line-height: 1.5; font-size: 0.95rem; white-space: pre-wrap; }
            .user-msg { background-color: #cba6f7; color: #11111b; align-self: flex-end; border-bottom-right-radius: 2px; font-weight: 500; }
            .ai-msg { background-color: #313244; color: #cdd6f4; align-self: flex-start; border-bottom-left-radius: 2px; border: 1px solid #45475a; }
            .input-area { padding: 15px; background-color: #11111b; display: flex; gap: 10px; border-top: 1px solid #45475a; }
            input[type="text"] { flex: 1; padding: 12px 16px; border-radius: 8px; border: 1px solid #45475a; background-color: #1e1e2e; color: #cdd6f4; font-size: 0.95rem; outline: none; }
            input[type="text"]:focus { border-color: #cba6f7; }
            button { padding: 12px 24px; background-color: #cba6f7; color: #11111b; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 0.95rem; transition: background 0.2s; }
            button:hover { background-color: #b4befe; }
            button:disabled { background-color: #585b70; cursor: not-allowed; }
            .typing-indicator { font-style: italic; color: #a6adc8; font-size: 0.85rem; align-self: flex-start; display: none; }
        </style>
    </head>
    <body>

    <div class="chat-container">
        <div class="chat-header">
            <h2>Personalized AI Companion</h2>
            <p>Running locally via FastAPI & Ollama</p>
        </div>
        
        <div class="messages-box" id="messagesBox">
            <div class="message ai-msg">Hello Nimra! How can I assist you today with your studies, projects, or applications?</div>
            <div class="typing-indicator" id="typingIndicator">AI companion is thinking...</div>
        </div>

        <div class="input-area">
            <input type="text" id="userInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
            <button id="sendBtn" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const messagesBox = document.getElementById('messagesBox');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        const typingIndicator = document.getElementById('typingIndicator');

        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }

        async function sendMessage() {
            const promptText = userInput.value.trim();
            if (!promptText) return;

            // Render User Message
            appendMessage(promptText, 'user-msg');
            userInput.value = '';
            
            // Show Typing State
            sendBtn.disabled = true;
            userInput.disabled = true;
            typingIndicator.style.display = 'block';
            messagesBox.scrollTop = messagesBox.scrollHeight;

            try {
                // Post cleanly structured JSON body directly to the backend API endpoint
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: promptText })
                });

                const data = await response.json();
                
                if (response.ok) {
                    appendMessage(data.response, 'ai-msg');
                } else {
                    appendMessage("Error: " + (data.detail || "Failed to process message."), 'ai-msg');
                }
            } catch (err) {
                appendMessage("Error: Network disconnected or server offline.", 'ai-msg');
            } finally {
                // Reset Input State
                sendBtn.disabled = false;
                userInput.disabled = false;
                typingIndicator.style.display = 'none';
                messagesBox.scrollTop = messagesBox.scrollHeight;
                userInput.focus();
            }
        }

        function appendMessage(text, className) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${className}`;
            msgDiv.textContent = text;
            messagesBox.insertBefore(msgDiv, typingIndicator);
        }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# 2. BACKEND API: Communicates securely with Ollama
@app.post("/api/chat")
async def chat_with_persona(payload: ChatRequest):
    try:
        ollama_payload = {
            "model": MODEL_NAME,
            "prompt": payload.prompt,
            "stream": False
        }
        
        response = requests.post(OLLAMA_API_URL, json=ollama_payload)
        response.raise_for_status()
        return {"response": response.json().get("response")}
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Connection to local Ollama service failed. Ensure terminal is active. Details: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)