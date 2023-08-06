from datetime import datetime, timezone
from typing import Optional, Tuple


def webfinger_response_json(account: str, url: str) -> dict:
    """helper to generate a webfinger response"""
    return {
        "subject": account,
        "links": [
            {
                "href": url,
                "rel": "self",
                "type": "application/activity+json",
            }
        ],
    }


def parse_fediverse_handle(account: str) -> Tuple[str, Optional[str]]:
    """Splits fediverse handle in name and domain"""
    if account[0] == "@":
        account = account[1:]

    if "@" in account:
        return tuple(account.split("@", 1))
    return account, None


def now_isoformat() -> str:
    """Returns now in Isoformat, e.g. "2023-05-31T18:11:35Z", to be used as the value
    of published"""
    return (
        datetime.now(tz=timezone.utc).replace(microsecond=0, tzinfo=None).isoformat()
        + "Z"
    )
