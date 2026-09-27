import base64
from gmail_auth import get_gmail_service
from db import SessionLocal
from repository import save_email


def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def get_plain_text_body(payload):
    # convert gmail encoded data to plain text.
    # body contains multiple parts, so we need to recursively search for the text/plain part.
    if payload.get("mimeType") == "text/plain" and "data" in payload.get("body", {}):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode(
            "utf-8", errors="ignore"
        )

    for part in payload.get("parts", []):
        text = get_plain_text_body(part)
        if text:
            return text

    return ""


def fetch_recent_emails(max_results=10):
    # fetch 10 recent emails
    # calling gmail service from gmail_auth.py to fetch recent emails from the user's inbox.
    service = get_gmail_service()

    results = (
        service.users()
        .messages()
        .list(userId="me", maxResults=max_results, labelIds=["INBOX"])
        .execute()
    )
    messages = results.get("messages", [])

    emails = []
    for msg_ref in messages:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=msg_ref["id"], format="full")
            .execute()
        )
        headers = msg["payload"]["headers"]

        emails.append(
            {
                "id": msg["id"],
                "from": get_header(headers, "From"),
                "subject": get_header(headers, "Subject"),
                "snippet": msg.get("snippet", ""),
                "body": get_plain_text_body(msg["payload"])[:1000],  # cap for now
            }
        )

    return emails


if __name__ == "__main__":
    emails = fetch_recent_emails(max_results=10)

    session = SessionLocal()
    try:
        for e in emails:
            saved = save_email(session, e)
            print(f"Saved: {saved.subject!r} (gmail_id={saved.gmail_id})")
    finally:
        session.close()