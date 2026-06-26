import os
import uuid

from dotenv import load_dotenv
from posthog import Posthog

load_dotenv()

client = Posthog(
    project_api_key=os.getenv("POSTHOG_API_KEY"),
    host=os.getenv("POSTHOG_HOST")
)


def track(event, properties=None):

    if properties is None:
        properties = {}

    client.capture(
        distinct_id=str(uuid.uuid4()),
        event=event,
        properties=properties
    )

    client.flush() 