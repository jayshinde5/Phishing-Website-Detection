"""Pulls simple, readable features out of a raw URL."""
import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = ["login", "verify", "update", "secure", "account", "bank",
                    "confirm", "signin", "password", "wallet", "free", "bonus"]
SHORTENERS = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd"]
SUSPICIOUS_TLDS = [".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".click", ".info"]


def extract_url_features(url: str) -> dict:
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    parsed = urlparse(url)
    host = parsed.netloc.split("@")[-1].split(":")[0].lower()
    path = parsed.path + parsed.query

    return {
        "url_length": len(url),
        "host_length": len(host),
        "path_length": len(path),
        "num_dots": url.count("."),
        "num_hyphens": host.count("-"),
        "num_digits": sum(c.isdigit() for c in url),
        "num_subdomains": max(host.count(".") - 1, 0),
        "has_at_symbol": int("@" in url),
        "has_ip_address": int(bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host))),
        "uses_https": int(parsed.scheme == "https"),
        "suspicious_words": sum(w in url.lower() for w in SUSPICIOUS_WORDS),
        "is_shortened": int(host in SHORTENERS),
        "suspicious_tld": int(any(host.endswith(t) for t in SUSPICIOUS_TLDS)),
    }
