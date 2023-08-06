import sys
from typing import Literal
import time

from ..staircase_env import StaircaseEnvironment


async def build(
    ci_env: StaircaseEnvironment,
    bundle_url,
    type: Literal["service", "data", "frontend"] = "service",
) -> str:
    if type == "service":
        url = "infra-builder/builds"
    elif type == "data":
        url = "infra-builder/data"
    elif type == "frontend":
        url = "infra-builder/frontend"

    r = await ci_env.http_client.async_request(url, "POST", data={"source_url": bundle_url})
    r = await r.json()
    id_ = r["build_id"]

    while True:
        response = await ci_env.http_client.async_request(f"{url}/{id_}")
        response_body = await response.json()

        status = response_body.get("status")
        if status in ("IN_PROGRESS", "RUNNING"):
            time.sleep(15)
        elif status == "FAILED":
            if logs := response_body.get("logs"):
                logs = "".join(logs) if isinstance(logs, list) else logs
            raise BuildFailed(logs)
        else:
            url = response_body["artifacts_url"]
            return url


class BuildFailed(Exception):
    ...
