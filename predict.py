"""Check a single URL:  python predict.py "http://paypal.secure-login.xyz/verify.php" """
import argparse
import joblib
import pandas as pd
from features import extract_url_features

p = argparse.ArgumentParser()
p.add_argument("url")
p.add_argument("--age", type=int, default=365, help="domain age in days")
p.add_argument("--login-form", type=int, default=0, help="page has login form (0/1)")
p.add_argument("--iframe", type=int, default=0, help="page has iframe (0/1)")
p.add_argument("--ext-links", type=float, default=0.2, help="share of external links (0-1)")
a = p.parse_args()

bundle = joblib.load("outputs/best_model.joblib")
row = extract_url_features(a.url)
row.update({"domain_age_days": a.age, "has_login_form": a.login_form,
            "has_iframe": a.iframe, "external_link_ratio": a.ext_links})
X = pd.DataFrame([row])[bundle["columns"]]

pred = bundle["model"].predict(X)[0]
print("⚠️  PHISHING / suspicious" if pred == 1 else "✅ Looks legitimate")
