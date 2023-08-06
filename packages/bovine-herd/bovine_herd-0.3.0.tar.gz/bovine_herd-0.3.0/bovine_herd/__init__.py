from typing import Awaitable

import aiohttp
from bovine_process import handle_outbox_item, process_inbox_item, process_outbox_item
from quart import Quart

from .server import default_configuration
from .server.endpoints import build_endpoints_blueprint


def BovineHerd(
    app: Quart,
    process_inbox_item: Awaitable = process_inbox_item,
    handle_outbox_item: Awaitable = handle_outbox_item,
    process_outbox_item: Awaitable = process_outbox_item,
) -> Quart:
    """Configures the quart app to use bovine herd. Requires a bovine_store compatible
    store to be available at app.config["bovine_store"]. Configures the endpoints

    * /.well-known
    * /activitypub
    * /endpoints

    :param app: The quart app to add the endpoints to.
    :param process_inbox_item: awaitable that asynchronously handles Activities
        that arrived at an inbox endpoint
    :param handle_outbox_item: awaitable that synchronously handles Activities
        that arrived at an outbox endpoint. This function should add the new id
        of the Activity to the ProcessingItem, so it can be returened in the
        location header.
    :param process_outbox_item: awaitable that asynchronously handles Activities
        that arrived at an outbox endpoint
    """

    @app.before_serving
    async def startup():
        if "session" not in app.config:
            session = aiohttp.ClientSession()
            app.config["session"] = session

    @app.after_serving
    async def shutdown():
        await app.config["session"].close()

    app.register_blueprint(default_configuration)
    endpoints = build_endpoints_blueprint(
        handle_outbox_item, process_inbox_item, process_outbox_item
    )
    app.register_blueprint(endpoints, url_prefix="/endpoints")

    return app
