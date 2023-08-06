import os
from dataclasses import dataclass
from unittest.mock import AsyncMock
import pytest
from tortoise import Tortoise, connections
from quart import Quart

from bovine_store import BovineStore, BovineAdminStore
from bovine_store.server.authorize import add_authorization
from bovine_store.server.blueprint import bovine_store_blueprint


async def init_connection(db_url):
    await Tortoise.init(db_url=db_url, modules={"models": ["bovine_store.models"]})
    await Tortoise.generate_schemas()


async def close_connection():
    await Tortoise.close_connections()


@dataclass
class EndpointMock:
    counter: int = 1

    def generate(self):
        self.counter += 1
        return f"https://my_domain/endpoints/{self.counter}"


@pytest.fixture
async def store():
    if not os.environ.get("POSTGRES"):
        db_file = "test_db.db"
        db_url = f"sqlite://{db_file}"

        response_mock = AsyncMock()
        response_mock.raise_for_status = lambda: 1
        session_mock = AsyncMock()
        session_mock.get.return_value = response_mock

        store = BovineStore(
            db_url,
            session=session_mock,
        )

        await init_connection(db_url)

        yield store
        await close_connection()
        os.unlink(db_file)
        return

    db_url = "postgres://postgres:secret@localhost:5432/postgres"
    store = BovineStore(db_url)

    await init_connection(db_url)

    yield store
    connection = connections.get("default")
    for table in [
        "visibleto",
        "bovineuserendpoint",
        "bovineuserkeypair",
        "bovineuserproperty",
        "collectionitem",
        "storedjsonobject",
        "bovineuser",
    ]:
        await connection.execute_query(f"DROP TABLE IF EXISTS {table}")
    await close_connection()


@pytest.fixture
async def bovine_store_actor(store):
    endpoint_mock = EndpointMock()
    db_file = "test_db.db"
    db_url = f"sqlite://{db_file}"

    admin_store = BovineAdminStore(
        db_url,
        endpoint_path_function=endpoint_mock.generate,
    )

    bovine_name = await admin_store.register("MoonJumpingCow")

    yield await store.actor_for_name(bovine_name)


@pytest.fixture
async def test_app(store):
    app = Quart(__name__)

    app.config["bovine_store"] = store
    app.config["session"] = store.session

    app.config["validate_http_signature"] = AsyncMock(return_value="owner")

    try:  # FIXME
        bovine_store_blueprint.before_request(add_authorization)
    except Exception:
        ...
    app.register_blueprint(bovine_store_blueprint)

    yield app

    await store.session.close()
