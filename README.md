Accessibility Navigator 👁️🎙️

A multimodal Generative AI web application designed to assist visually impaired individuals in navigating their surroundings, identifying objects, and reading signs in real-time.

Built as a low-latency pipeline, the app captures a user's voice prompt and the smartphone's camera feed, processes both simultaneously using Groq's ultra-fast inference APIs, and speaks the contextual answer back to the user.

✨ Features

Voice-Activated Commands: Users hold a single large button to ask questions about their environment (e.g., "Describe the room," "What does this sign say?").

Lightning Fast Speech-to-Text: Utilizes the whisper-large-v3-turbo model to instantly transcribe user audio.

Multimodal Vision Processing: Uses Meta's llama-4-scout-17b-16e-instruct vision-language model to analyze the camera snapshot contextually against the user's spoken question.

Native Text-to-Speech: Leverages the browser's built-in Web Speech API for immediate, zero-latency audio feedback.

Mobile-First Design: Fully responsive UI that defaults to the smartphone's rear-facing camera.

🛠️ Tech Stack

Backend: Python, FastAPI, Uvicorn

Frontend: HTML5, Vanilla JavaScript, CSS3, Web Media/Speech APIs

AI/LLM Provider: Groq Cloud API

Environment Management: python-dotenv

🚀 Setup & Installation

1. Prerequisites

Python 3.8 or higher installed.

A free Groq API Key.

A smartphone or a computer with a webcam and microphone.

2. Clone and Install Dependencies

Open your terminal and run the following commands:

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required packages
pip install fastapi uvicorn groq python-multipart python-dotenv


3. Configure Environment Variables

Create a file named .env in the root directory of the project and add your Groq API key:

GROQ_API_KEY=gsk_your_groq_api_key_here


4. Run the Server

Start the FastAPI server on all network interfaces so it can be accessed by your phone:

uvicorn app:app --host 0.0.0.0 --port 8000 --reload


📱 Testing on a Smartphone

Because browsers require HTTPS to access camera/microphone hardware, you have two options to test this on your phone:

Option A: Local Wi-Fi (No downloads required)

Ensure your phone and laptop are on the same Wi-Fi network.

Find your laptop's local IP address (e.g., 192.168.1.5).

Open Google Chrome on your Android phone and navigate to chrome://flags/#unsafely-treat-insecure-origin-as-secure.

Enter your laptop's IP and port (e.g., http://192.168.1.5:8000), switch the dropdown to Enabled, and relaunch Chrome.

Go to http://YOUR_LAPTOP_IP:8000 in Chrome to use the app.

Option B: Using an HTTPS Tunnel (Ngrok)

Install Ngrok and authenticate your account.

Run the following command in a new terminal window:

ngrok http 8000


Open the generated https://...ngrok-free.app link on your smartphone's browser.

🔮 Future Enhancements

Native Android Wrapper: Package the web app using Capacitor or Expo to allow triggering the microphone via the physical volume hardware buttons.

Continuous Processing: Move from a "push-to-talk" model to a continuous video stream analysis using WebSockets.

Local Inference: Implement local, on-device models to ensure 100% privacy and offline capability.