import asyncio
import json

import structlog
from bs4 import BeautifulSoup

from llms import predict_marketing_email, run_unsubscribe_loop
from util import connect_and_retrieve_emails, load_config

log = structlog.get_logger()

config = load_config()
emails = connect_and_retrieve_emails(
    config.imap_server, config.email_address, config.password
)


# Main loop
async def run():
    for email in emails:
        # Get the next email
        content = email.content
        # Check if it has an unsubscribe link at the end
        marketing_email_obj = await predict_marketing_email(content)
        marketing_email = marketing_email_obj["unsubscribe_link"]
        # If it does, run unsubscribe flow
        if marketing_email is not None:
            try:
                soup = BeautifulSoup(content, "html.parser")
                links = {a.get_text(): a["href"] for a in soup.find_all("a")}
                await run_unsubscribe_loop(links[marketing_email])
            except Exception as e:
                log.warn("exception running unsubscribe", exception=str(e))
        else:
            pass


asyncio.run(run())
