import requests
import os

def send_whatsapp_message(recipients: list, message: str):
    """
    Placeholder Whatsapp sender. Replace the body with your provider's API.
    This example assumes a generic HTTP API that accepts phone numbers and message.
    Implement authentication (Bearer/Token) with env vars.
    Returns (success: bool, error: str|None)
    """
    WA_API_URL = os.environ.get("WA_API_URL")  # e.g. Twilio or Meta WhatsApp Cloud endpoint
    WA_TOKEN = os.environ.get("WA_API_TOKEN")

    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json",
    }

    for to in recipients:
        payload = {
            "to": to,
            "message": message
        }
        try:
            resp = requests.post(WA_API_URL, json=payload, headers=headers, timeout=10)
            if resp.status_code in (200, 201, 202):
                continue
            else:
                return False, f"Status {resp.status_code}: {resp.text}"
        except Exception as exc:
            return False, str(exc)

    return True, None
