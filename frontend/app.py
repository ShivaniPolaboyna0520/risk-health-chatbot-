
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backend.model_handler import predict_diabetes
from backend.chat_handler import get_chat_response

st.set_page_config(page_title="🩺 Health Risk Chatbot", page_icon="💬")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2874/2874822.png", width=100)
    st.markdown("### 👩‍⚕️ Your Health Assistant")
    st.markdown("Ask questions related to diabetes, health, wellness, and fitness.")
    st.markdown("---")
    st.markdown("### 📊 BMI Categories")
    st.markdown("""
| BMI Value | Category |
|-----------|----------|
| < 18.5    | Underweight |
| 18.5–24.9 | Normal weight |
| 25–29.9   | Overweight |
| 30+       | Obese |
""")
    st.markdown("---")
    st.markdown("### 🩸 Glucose Levels (Fasting)")
    st.markdown("""
| Glucose (mg/dL) | Category |
|-----------------|----------|
| 70–99           | Normal |
| 100–125         | Prediabetes |
| 126+            | Diabetes |
""")

# Initialize session state
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'prediction' not in st.session_state:
    st.session_state.prediction = None
if 'probability' not in st.session_state:
    st.session_state.probability = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("🩺 Health Risk Assessment Chatbot")

# Health input form
if not st.session_state.prediction_made:
    with st.form("health_form"):
        st.subheader("🧾 Enter Your Health Details")
        pregnancies = st.number_input("Pregnancies", min_value=0)
        glucose = st.number_input("Glucose", min_value=0)
        blood_pressure = st.number_input("Blood Pressure", min_value=0)
        skin_thickness = st.number_input("Skin Thickness", min_value=0)
        insulin = st.number_input("Insulin", min_value=0)
        bmi = st.number_input("BMI", min_value=0.0)
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0)
        age = st.number_input("Age", min_value=0)
        submitted = st.form_submit_button("🔍 Predict Risk")

    if submitted:
        # Save inputs
        st.session_state.pregnancies = pregnancies
        st.session_state.glucose = glucose
        st.session_state.blood_pressure = blood_pressure
        st.session_state.skin_thickness = skin_thickness
        st.session_state.insulin = insulin
        st.session_state.bmi = bmi
        st.session_state.dpf = dpf
        st.session_state.age = age

        features = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]
        prediction, probability = predict_diabetes(features)
        st.session_state.prediction_made = True
        st.session_state.prediction = prediction
        st.session_state.probability = probability

        st.session_state.chat_history = [
            {"role": "system", "content": "You are a friendly and reliable health assistant. You answer health-related questions professionally. For casual greetings (like 'how are you', 'hello', 'good morning'), you respond warmly and politely like a human assistant would."},
            {"role": "user", "content": f"My health details show I have a {'high' if prediction else 'low'} risk of diabetes with a probability of {probability}."}
        ]
        st.rerun()

# After prediction
if st.session_state.prediction_made:
    st.subheader("📊 Prediction Result")
    st.success(f"Risk Level: {'High' if st.session_state.prediction else 'Low'}")
    st.info(f"Probability: {st.session_state.probability}")

    # Present Sugar
    st.subheader("🩸 Present Blood Sugar Level")
    st.success(f"Your blood glucose level is approximately: **{st.session_state.glucose} mg/dL**")

    if st.session_state.glucose < 70:
        st.warning("⚠️ Low blood sugar detected. Consult a doctor immediately!")
    elif 70 <= st.session_state.glucose <= 99:
        st.info("✅ Normal fasting blood sugar level.")
    elif 100 <= st.session_state.glucose <= 125:
        st.warning("⚠️ Prediabetes range. Lifestyle changes recommended.")
    else:
        st.error("🚨 Diabetes level detected. Please consult an endocrinologist.")

    # Why You Might Be at Risk (with emojis)
    st.subheader("🧠 Why You Might Be at Risk")

    reasons = []
    if st.session_state.glucose >= 100:
        reasons.append("🩸 High glucose level detected.")
    if st.session_state.bmi >= 25:
        reasons.append("⚖️ Overweight or obesity range BMI.")
    if st.session_state.insulin >= 25:
        reasons.append("🧬 Higher fasting insulin level indicating insulin resistance.")
    if st.session_state.dpf >= 0.5:
        reasons.append("👨‍👩‍👧‍👦 Elevated Diabetes Pedigree Function (family history risk).")
    if st.session_state.blood_pressure >= 130:
        reasons.append("💓 Higher blood pressure than normal.")

    if reasons:
        for reason in reasons:
            st.warning(reason)
    else:
        st.success("✅ Your entered health parameters look mostly within normal ranges!")

    # Personalized Advice
    st.subheader("🩺 Personalized Health Advice")

    if st.session_state.glucose < 70:
        st.error("🔴 Critical: Please consult a doctor immediately. Carry fast-acting sugar (like juice) with you.")
    elif 70 <= st.session_state.glucose <= 99:
        st.success("🟢 Excellent! Maintain your healthy lifestyle: balanced diet, regular exercise, good sleep.")
    elif 100 <= st.session_state.glucose <= 125:
        st.warning("🟡 Caution: Focus on low-sugar, high-fiber diet. Aim for 30 mins exercise daily. Recheck sugar levels in 3-6 months.")
    else:
        st.error("🔴 Warning: Immediate consultation with an endocrinologist is recommended. You may require medication and lifestyle intervention.")

    # Chatbot Follow-up
    st.subheader("💬 Chat with Health Assistant")

    for msg in st.session_state.chat_history[2:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your health-related question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("🤖 Bot is thinking..."):
            prompt_lower = prompt.lower()

            if "sugar level" in prompt_lower or "glucose" in prompt_lower:
                response = f"🩸 Your current blood glucose level is **{st.session_state.glucose} mg/dL**."
            elif "bmi" in prompt_lower:
                response = f"⚖️ Your recorded BMI is **{st.session_state.bmi}**."
            elif "age" in prompt_lower:
                response = f"🎂 Your recorded age is **{st.session_state.age} years**."
            elif "diabetes risk" in prompt_lower or "risk level" in prompt_lower:
                response = f"📈 Your predicted diabetes risk level is **{'High' if st.session_state.prediction else 'Low'}** with a probability of **{round(st.session_state.probability*100,2)}%**."
            else:
                response = get_chat_response(st.session_state.chat_history)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

    if st.button("🔁 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
