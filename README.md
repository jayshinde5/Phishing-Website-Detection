# Phishing Website Detection

A small machine learning project that flags suspicious websites by looking at the URL, basic domain info and a few webpage traits. Phishing sites love long messy URLs, fake brand names, odd TLDs and brand‑new domains, so a model can pick up on those patterns quickly.

## What it does
- Extracts features from a URL (length, dots, hyphens, `@`, IP address, https, suspicious words, shortened links, odd TLDs)
- Adds domain/page features (domain age, login form, iframe, external link ratio)
- Trains **Logistic Regression, SVM, Decision Tree and Naive Bayes**
- Compares them, saves the best one, and lets you test any URL
- Includes a simple **Streamlit** web app for checking URLs in the browser

## Project structure
```
phishing-detection/
├── generate_dataset.py   # makes a sample dataset (works offline)
├── features.py           # URL feature extraction
├── train.py              # trains + compares models
├── predict.py            # check a single URL (command line)
├── app.py                # Streamlit web app
├── requirements.txt
└── README.md
```

## How to run
1. Open the folder in VS Code and open a terminal.
2. (Optional) create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   ```
3. Install the libraries:
   ```
   pip install -r requirements.txt
   ```
4. Create the dataset:
   ```
   python generate_dataset.py
   ```
5. Train and compare the models:
   ```
   python train.py
   ```
6. Test a URL:
   ```
   python predict.py "http://paypal.secure-login.xyz/verify.php" --age 5 --login-form 1
   python predict.py "https://github.com/about"
   ```

7. Launch the web app:
   ```
   streamlit run app.py
   ```
   It opens at `http://localhost:8501`. (If you skipped step 5, it trains the model automatically on first launch.)

Results (comparison table, bar chart, confusion matrix, saved model) land in the `outputs/` folder.

## Using real data
The included dataset is synthetic so the project runs anywhere. To use a real one (e.g. from Kaggle or PhishTank), save it as `data/phishing_data.csv` with the columns: `url, domain_age_days, has_login_form, has_iframe, external_link_ratio, label` (1 = phishing, 0 = legit).

## Notes
- Metrics here come from synthetic data, so treat them as a demo, not real‑world accuracy.
- `predict.py` can't fetch live domain age or page content, so you pass those as optional flags.
