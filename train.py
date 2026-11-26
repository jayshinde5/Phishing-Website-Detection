"""Trains 4 models, compares them, saves the best one."""
import os
import joblib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, ConfusionMatrixDisplay)
from features import extract_url_features

EXTRA = ["domain_age_days", "has_login_form", "has_iframe", "external_link_ratio"]

df = pd.read_csv("data/phishing_data.csv")
X = pd.DataFrame([extract_url_features(u) for u in df["url"]])
X[EXTRA] = df[EXTRA].values
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": SVC(kernel="rbf"),
    "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
    "Naive Bayes": GaussianNB(),
}

results, fitted = [], {}
for name, clf in models.items():
    pipe = make_pipeline(StandardScaler(), clf)
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    fitted[name] = (pipe, pred)
    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred),
        "Recall": recall_score(y_test, pred),
        "F1": f1_score(y_test, pred),
    })

res = pd.DataFrame(results).sort_values("F1", ascending=False).round(3)
print("\n", res.to_string(index=False))

best = res.iloc[0]["Model"]
print(f"\nBest model: {best}")

os.makedirs("outputs", exist_ok=True)
joblib.dump({"model": fitted[best][0], "columns": list(X.columns)}, "outputs/best_model.joblib")
res.to_csv("outputs/model_comparison.csv", index=False)

# charts
res.set_index("Model")[["Accuracy", "Precision", "Recall", "F1"]].plot(kind="bar", figsize=(8, 5))
plt.title("Model comparison"); plt.ylim(0.7, 1.02); plt.xticks(rotation=15)
plt.tight_layout(); plt.savefig("outputs/model_comparison.png"); plt.close()

ConfusionMatrixDisplay(confusion_matrix(y_test, fitted[best][1]),
                       display_labels=["Legit", "Phishing"]).plot(cmap="Blues")
plt.title(f"Confusion matrix - {best}")
plt.savefig("outputs/confusion_matrix.png"); plt.close()
print("Saved model and charts in the outputs/ folder.")
