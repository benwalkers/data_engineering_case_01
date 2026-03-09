from __future__ import annotations
import base64, hashlib, hmac, os

def tokenise_session_id(session_id: str, secret: str | None = None) -> str:
    if not session_id:
        return ""
    secret = secret or os.environ.get("PII_TOKEN_SECRET", "replace-me")
    digest = hmac.new(secret.encode(), session_id.encode(), hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return f"tok_{token[:24]}"
