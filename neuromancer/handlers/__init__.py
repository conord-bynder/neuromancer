from aiohttp_prometheus import MetricsView
from neuromancer.handlers.initiate import (
    initiate_full_scan,
    initiate_scan)


def setup_routes(app) -> None:
    app.router.add_get('/metrics', MetricsView)
    app.router.add_put('/initiate/{portal_id}', initiate_scan)
    app.router.add_put('/initiate_full/', initiate_full_scan)


