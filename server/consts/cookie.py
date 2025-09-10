import os

SEVEN_DAYS = 604800

COOKIE_OPTIONS = {
    "max_age": SEVEN_DAYS,
    "httponly": True,
    "secure": True,
    "samesite": "none",
    "domain": os.getenv("SERVER_HOST") or "localhost",
}
