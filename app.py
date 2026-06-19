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
    
    # 1. Speech-to-Text
    transcription = client.audio.transcriptions.create(
        file=("audio.webm", audio_bytes),
        model="whisper-large-v3-turbo",
        response_format="text"
    )
    user_question = transcription
    print(f"User asked: {user_question}")

    # 2. Vision Model (Using the current Groq Llama 4 Scout model)
    chat_completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
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

    # 3. Return the text directly to the frontend (Browser handles Text-to-Speech)
    return {"answer": ai_answer}