# Health-Risk-Chatbot

 🩺 Health Risk Assessment Chatbot

A smart AI-powered chatbot that helps assess your diabetes risk using medical input features. After prediction, it allows interactive follow-up questions related to health, medication, and nearby doctor suggestions — powered by OpenAI GPT.


 🔍 Project Overview

This full-stack application allows users to:
- Enter health data and get a diabetes risk prediction
- Ask intelligent health-related follow-up questions
- Receive personalized responses with real-time medical reasoning
- Get suggestions on lifestyle, medication, and even local doctors (via optional API)


 ✨ Features

- ✅ Diabetes risk prediction using a trained ML model
- 💬 Smart GPT-powered health conversation
- 📈 Personalized explanation of prediction result
- 🧠 Dynamic chatbot memory (follows up based on user input)
- 🌐 Ready to integrate with APIs like Google Places for doctor lookup
- 🎙️ Voice input support (optional)
- ☁️ Can be deployed to Streamlit Cloud or AWS


 🧰 Tech Stack

| Layer         | Technology Used           |
|---------------|---------------------------|
| Frontend      | Streamlit                 |
| Backend       | Python, FastAPI (optional)|
| AI Chat       | OpenAI GPT (via API)      |
| ML Model      | Logistic Regression       |
| Data Storage  | CSV (diabetes dataset)    |
| Styling       | Custom Streamlit + CSS    |



 🗂️ Folder Structure
 risk_health_chatbot/ ├── frontend/ │ └── app.py # Main Streamlit UI ├── backend/ │ ├── model_handler.py # ML prediction logic │ └── chat_handler.py # GPT response logic ├── data/ │ └── diabetes.csv # Training dataset ├── requirements.txt # Python dependencies ├── .gitignore └──




 

