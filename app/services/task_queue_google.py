import json
import time

from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2

from app.backend.core.config import settings


def create_http_task(
    project: str,
    queue: str,
    location: str,
    url: str,
    payload: dict,
    service_account_email: str,
    delay_seconds: int = 0,
) -> tasks_v2.Task:
    """
    Create an HTTP Task in a Google Cloud Tasks queue with OIDC authentication.
    This is the secure way for a Cloud Run service to invoke another private Cloud Run service.
    """
    client = tasks_v2.CloudTasksClient()

    parent = client.queue_path(project, location, queue)

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {"Content-type": "application/json"},
            "oidc_token": {"service_account_email": service_account_email},
        },
        "http_request.body": json.dumps(payload).encode(),
    }

    response = client.create_task(request={"parent": parent, "task": task})
    print(f"Created task: {response.name}")
    return response
