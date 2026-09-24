import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Route to serve the frontend UI
@app.get("/")
async def serve_frontend():
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Route to handle the multimodal logic
@app.post("/navigate")
async def navigate(audio: UploadFile = File(...), image: str = Form(...)):
    audio_bytes = await audio.read()
    
    try:
        # 1. Speech-to-Text
        transcription = client.audio.transcriptions.create(
            file=("audio.webm", audio_bytes),
            model="whisper-large-v3-turbo",
            response_format="text"
        )
        user_question = transcription.strip()
        print(f"User asked: {user_question}")

        if not user_question:
            user_question = "Describe what you see in front of me."

        # 2. Vision Model (Using Groq vision model qwen/qwen3.8-27b)
        chat_completion = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": f"You are assisting a visually impaired person. Keep your answer brief and conversational. Answer this based on the image: {user_question}"
                        },
                        {
                            "type": "image_url", 
                            "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                        },
                    ], 
                }
            ]
        )
        ai_answer = chat_completion.choices[0].message.content
        print(f"AI answers: {ai_answer}")
        return {"answer": ai_answer}
    except Exception as e:
        print(f"Error during processing: {e}")
        return {"answer": f"Sorry, there was an error processing your request: {str(e)}"}