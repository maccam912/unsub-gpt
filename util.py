import email
import imaplib
from email.header import decode_header
from typing import List

import structlog
import toml
from pydantic import BaseModel

log = structlog.get_logger()


class Config(BaseModel):
    """
    Configuration model.
    """

    imap_server: str
    email_address: str
    password: str


class Email(BaseModel):
    """
    Email model.
    """

    subject: str
    content: str
    from_address: str


def load_config(path: str = "config.toml") -> Config:
    """
    Loads the configuration file.

    :param path: Path to the configuration file

    :return: Configuration dictionary
    """
    # load from config.toml
    log.debug("Loading config", path=path)
    toml_config = toml.load(path)
    return Config(**toml_config)


def get_content(msg: email.message.Message) -> str:
    """
    Gets the HTML content of the email message.

    :param msg: Email message object
    :return: HTML content or an empty string if none is found
    """
    if msg.is_multipart():
        # Iterate over each part of a multipart message
        for part in msg.walk():
            # Check the content type of each part
            if part.get_content_type() == "text/html":
                # Get the payload, decode it and return the content
                payload = part.get_payload(decode=True)
                charset = (
                    part.get_content_charset() or "utf-8"
                )  # Default to 'utf-8' if no charset is specified
                return payload.decode(charset)
    else:
        # If the message is not multipart, just check if it is HTML
        if msg.get_content_type() == "text/html":
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset() or "utf-8"
            return payload.decode(charset)

    # If no HTML content was found
    return ""


def decode_field(field: str) -> str:
    decoded_header = decode_header(field)
    field_parts = [
        part.decode(encoding or "utf-8") if isinstance(part, bytes) else part
        for part, encoding in decoded_header
    ]
    return "".join(field_parts)


def connect_and_retrieve_emails(
    imap_server: str, email_address: str, password: str
) -> List[Email]:
    """
    Connects to the email account and fetches the last 100 emails.

    :param imap_server: IMAP server address
    :param email_address: User's email address
    :param password: User's password
    :return: List of email messages
    """
    log.debug("Connecting to email account")
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_address, password)
    log.debug("Connected to email account")
    mail.select()
    typ, data = mail.search(None, "ALL")
    email_ids = data[0].split()[-30:]
    emails: List[Email] = []
    for e_id in email_ids:
        log.debug(f"Fetching email {e_id}")
        typ, data = mail.fetch(e_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        subj = msg.get("Subject")
        print(subj)
        decoded_subj = decode_field(subj)  # Decode the subject line
        from_address = msg.get("From")
        decoded_from = decode_field(from_address)  # Decode the from address
        content = get_content(msg)
        e = Email(
            subject=decoded_subj, content=content, from_address=decoded_from
        )  # Include the from address
        emails.append(e)
    mail.logout()
    return emails


# Main loop
# Get the next email
# Check if it has an unsubscribe link at the end
# If it does, run unsubscribe flow
