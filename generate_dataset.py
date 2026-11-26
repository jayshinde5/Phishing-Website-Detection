"""Creates a synthetic dataset (data/phishing_data.csv) so the project runs offline.
Want real data? Drop your own CSV with columns: url, domain_age_days,
has_login_form, has_iframe, external_link_ratio, label (1 = phishing)."""
import random
import pandas as pd

random.seed(42)
BRANDS = ["paypal", "amazon", "google", "microsoft", "apple", "netflix", "sbi", "hdfcbank"]
GOOD = ["wikipedia", "github", "stackoverflow", "bbc", "nytimes", "mit", "python",
        "reddit", "linkedin", "coursera", "flipkart", "zomato", "irctc"]
WORDS = ["login", "verify", "update", "secure", "account", "confirm", "signin", "wallet"]
BAD_TLDS = [".xyz", ".top", ".tk", ".ml", ".click", ".info"]


def legit():
    host = random.choice(GOOD + BRANDS) + random.choice([".com", ".org", ".edu", ".in", ".net"])
    if random.random() < 0.3:
        host = "www." + host
    path = "/".join(random.choice(["home", "about", "products", "docs", "blog", "help"])
                    for _ in range(random.randint(0, 3)))
    scheme = "https" if random.random() < 0.9 else "http"
    return {
        "url": f"{scheme}://{host}/{path}",
        "domain_age_days": int(random.gauss(2500, 1200)) % 9000 + 200,
        "has_login_form": int(random.random() < 0.2),
        "has_iframe": int(random.random() < 0.1),
        "external_link_ratio": round(random.uniform(0.0, 0.4), 2),
        "label": 0,
    }


def phishing():
    kind = random.random()
    brand, word = random.choice(BRANDS), random.choice(WORDS)
    if kind < 0.2:
        host = ".".join(str(random.randint(1, 255)) for _ in range(4))
    elif kind < 0.5:
        host = f"{brand}.{word}-{random.choice(WORDS)}{random.choice(BAD_TLDS)}"
    elif kind < 0.75:
        host = f"{brand}-{word}-{random.randint(10, 999)}{random.choice(BAD_TLDS + ['.com'])}"
    else:
        host = random.choice(["bit.ly", "tinyurl.com", "goo.gl"])
    path = f"{word}/{random.choice(WORDS)}.php?id={random.randint(1000, 99999)}"
    if random.random() < 0.2:
        host = f"{brand}.com@{host}"
    scheme = "https" if random.random() < 0.45 else "http"
    return {
        "url": f"{scheme}://{host}/{path}",
        "domain_age_days": random.randint(1, 400),
        "has_login_form": int(random.random() < 0.8),
        "has_iframe": int(random.random() < 0.45),
        "external_link_ratio": round(random.uniform(0.3, 1.0), 2),
        "label": 1,
    }


rows = [legit() for _ in range(1500)] + [phishing() for _ in range(1500)]
df = pd.DataFrame(rows).sample(frac=1, random_state=42)

# add a little noise so the task isn't trivially perfect
flip = df.sample(frac=0.04, random_state=1).index
df.loc[flip, "label"] = 1 - df.loc[flip, "label"]

import os
os.makedirs("data", exist_ok=True)
df.to_csv("data/phishing_data.csv", index=False)
print(f"Saved {len(df)} rows to data/phishing_data.csv")
