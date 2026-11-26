"""Streamlit web app:  streamlit run app.py"""
import os
import subprocess
import sys
import joblib
import pandas as pd
import streamlit as st
from features import extract_url_features

st.set_page_config(page_title="Phishing Website Detector", page_icon="🛡️")


@st.cache_resource
def load_model():
    # train automatically on first run if no model exists yet
    if not os.path.exists("outputs/best_model.joblib"):
        if not os.path.exists("data/phishing_data.csv"):
            subprocess.run([sys.executable, "generate_dataset.py"], check=True)
        subprocess.run([sys.executable, "train.py"], check=True)
    return joblib.load("outputs/best_model.joblib")


bundle = load_model()

st.title("🛡️ Phishing Website Detector")
st.write("Paste a URL and add what you know about the domain and page. "
         "The model checks it for phishing signs.")

url = st.text_input("Website URL", placeholder="http://paypal.secure-login.xyz/verify.php")

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Domain age (days)", min_value=0, value=365)
    ext = st.slider("Share of external links", 0.0, 1.0, 0.2)
with col2:
    login = st.checkbox("Page has a login form")
    iframe = st.checkbox("Page uses an iframe")

if st.button("Check website", type="primary"):
    if not url.strip():
        st.warning("Please enter a URL first.")
    else:
        row = extract_url_features(url.strip())
        row.update({"domain_age_days": age, "has_login_form": int(login),
                    "has_iframe": int(iframe), "external_link_ratio": ext})
        X = pd.DataFrame([row])[bundle["columns"]]
        model = bundle["model"]
        pred = model.predict(X)[0]

        if pred == 1:
            st.error("⚠️ This looks like a PHISHING / suspicious website.")
        else:
            st.success("✅ This looks legitimate.")

        if hasattr(model, "predict_proba"):
            st.metric("Phishing probability", f"{model.predict_proba(X)[0][1]:.0%}")

        with st.expander("Features the model saw"):
            st.dataframe(X.T.rename(columns={0: "value"}))

st.caption("Demo model trained on synthetic data - not for real security decisions.")
