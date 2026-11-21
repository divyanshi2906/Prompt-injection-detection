
import streamlit as st
import joblib
import re
import os

# =================================================
# 1. PAGE CONFIGURATION
# =================================================

st.set_page_config(
    page_title="Prompt Injection Detector",
    page_icon="🛡️",
    layout="centered"
)

# =================================================
# 2. LOAD MODEL
# =================================================

MODEL_PATH = "model/prompt_detector.pkl"
INFO_PATH = "model/model_info.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("Model not found! Run train.py first.")
    st.stop()

model = joblib.load(MODEL_PATH)
model_info = joblib.load(INFO_PATH)

# =================================================
# 3. CUSTOM CSS
# =================================================

st.markdown("""
<style>

.stApp {
    background-color: #10131c;
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

textarea {
    background-color: #202635 !important;
    color: white !important;
}

.stButton > button {
    background-color: #635bff;
    color: white;
    border-radius: 10px;
    border: none;
    height: 45px;
    width: 100%;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #817aff;
    color: white;
}

.metric-card {
    background-color: #202635;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =================================================
# 4. TEXT PREPROCESSING
# =================================================

def clean_text(text):

    text = str(text)

    text = re.sub(r"<[^>]+>", " ", text)

    text = re.sub(r"\s+", " ", text)

    text = text.lower().strip()

    return text

# =================================================
# 5. HEADER
# =================================================

st.title("🛡️ Prompt Injection Detector")

st.markdown(
    "### Machine Learning Based Security System"
)

st.write(
    "Enter a prompt below to identify whether "
    "it is safe or contains a possible prompt injection."
)

st.divider()

# =================================================
# 6. INPUT PROMPT
# =================================================

user_prompt = st.text_area(
    "Enter your prompt:",
    placeholder="Example: Ignore all previous instructions...",
    height=160
)

# =================================================
# 7. PREDICTION
# =================================================

if st.button("🔍 Detect Prompt Injection"):

    if not user_prompt.strip():

        st.warning("Please enter a prompt first.")

    else:

        cleaned_prompt = clean_text(user_prompt)

        prediction = model.predict([cleaned_prompt])[0]

        st.divider()

        st.subheader("Detection Result")

        if prediction == 1:

            st.error("🚨 MALICIOUS PROMPT DETECTED")

            st.write(
                "This prompt has been classified as "
                "a potential prompt injection attempt."
            )

        else:

            st.success("✅ SAFE PROMPT")

            st.write(
                "No prompt injection was detected "
                "by the trained classifier."
            )

        st.caption(
            "This is an ML classification result, "
            "not a guarantee of security."
        )

# =================================================
# 8. MODEL PERFORMANCE
# =================================================

st.divider()

st.subheader("📊 Model Performance")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Accuracy",
        f"{model_info['accuracy'] * 100:.2f}%"
    )

    st.metric(
        "Precision",
        f"{model_info['precision'] * 100:.2f}%"
    )

with col2:

    st.metric(
        "Recall",
        f"{model_info['recall'] * 100:.2f}%"
    )

    st.metric(
        "F1 Score",
        f"{model_info['f1_score'] * 100:.2f}%"
    )

st.info(
    f"Selected Algorithm: {model_info['best_model']}"
)

# =================================================
# 9. FOOTER
# =================================================

st.divider()

st.caption(
    "Prompt Injection Detection | Machine Learning Project"
)
