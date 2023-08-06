import aiohttp
from quart import Quart

from bovine.crypto import build_validate_http_signature

from bovine_store import BovineStore
from .retrieve_public_key import retrieve_public_key


async def configure_bovine_store(app: Quart):
    if "session" not in app.config:
        app.config["session"] = aiohttp.ClientSession()

    app.config["bovine_store"] = BovineStore(
        session=app.config["session"],
    )

    app.config["validate_http_signature"] = build_validate_http_signature(
        retrieve_public_key
    )


def tortoise_config(db_url: str) -> dict:
    return {
        "connections": {"default": db_url},
        "apps": {
            "models": {
                "models": [
                    "bovine_store.models",
                ],
                "default_connection": "default",
            },
        },
    }
