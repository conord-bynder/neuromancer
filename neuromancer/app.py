import logging

from aiohttp.web import (
    Application)
from aiohttp_prometheus import MetricsMiddleware

from bynder_connectors.connections.alchemy import (
    setup_connection_manager_for_aiohttp,
    setup_alchemy_read_write_connection_for_aiohttp)

from bynder_connectors.interfaces.async_http import AsyncHTTPInterface
from bynder_connectors.interfaces.header_factories import AuthHeaderFactory
from bynder_connectors.transactions import transaction_middleware
from bynder_connectors.transactions.alchemy import (
    setup_alchemy_read_write_transaction_middleware)


from neuromancer.handlers import setup_routes

log = logging.getLogger(__name__)


async def run_app() -> Application:
    app = Application(middlewares=[
        transaction_middleware,
        setup_alchemy_read_write_transaction_middleware()])

    app.middlewares.append(MetricsMiddleware())

    setup_connection_manager_for_aiohttp(app)
    setup_alchemy_read_write_connection_for_aiohttp(app)

    log.info('Neuromancer plugging in')

    setup_routes(app)

    return app
