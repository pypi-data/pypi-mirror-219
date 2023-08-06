import aiohttp
from typing import Awaitable

from quart import Quart
from tortoise.contrib.quart import register_tortoise

from .authorize import add_authorization
from .config import tortoise_config, configure_bovine_store
from .blueprint import bovine_store_blueprint


def BovineStoreManager(
    app: Quart,
    url_prefix: str = "/objects",
    db_url: str = "sqlite://bovine.sqlite3",
    retriever_blocker: Awaitable | None = None,
):
    """Adds the bovine store to the quart app

    :param app: the quart app
    :param url_prefix: the prefix objects are served under.

        Objects are served as /objects/<uuid>

        Collections are served as /objects/<uuid>/<collection_name>

    :param db_url: The database connection
    :param retriever_blocker: a coroutine that can use g.retriever or other parts of
        a request to stop it from being processed"""

    @app.before_serving
    async def startup():
        if "session" not in app.config:
            session = aiohttp.ClientSession()
            app.config["session"] = session
        await configure_bovine_store(app)

    if retriever_blocker:

        async def authorize():
            result = await add_authorization()
            if result:
                return result
            return await retriever_blocker()

        app.before_request(authorize)
    else:
        app.before_request(add_authorization)

    app.register_blueprint(bovine_store_blueprint, url_prefix=url_prefix)

    TORTOISE_ORM = tortoise_config(db_url)

    register_tortoise(
        app,
        db_url=TORTOISE_ORM["connections"]["default"],
        modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
        generate_schemas=True,
    )
