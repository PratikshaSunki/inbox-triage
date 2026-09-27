

from models import Email


def email_exists(session, gmail_id: str) -> bool:
    # check if an email with the given gmail_id already exists in the database.
    return session.get(Email, gmail_id) is not None


def save_email(session, email_data: dict) -> Email:
    """
    email_data is expected to have: id, from, subject, snippet, body
    Safe to call repeatedly with the same email - it won't duplicate,
    since gmail_id is the primary key and we check existence first.
    """
    if email_exists(session, email_data["id"]):
        return session.get(Email, email_data["id"])

    email = Email(
        gmail_id=email_data["id"],
        sender=email_data["from"],
        subject=email_data["subject"],
        snippet=email_data["snippet"],
        body=email_data["body"],
    )
    session.add(email)
    session.commit()
    session.refresh(email)
    return email


def get_all_emails(session):
    return session.query(Email).order_by(Email.fetched_at.desc()).all()