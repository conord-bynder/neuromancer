import logging
from aiohttp.web import (
    json_response,
    Request,
    Response)
from neuromancer.services.scan import ScanService

log = logging.getLogger(__name__)


async def initiate_scan(request: Request) -> Response:
    ScanService(request).initiate_scan(
        request.match_info['portal_id'])
    return json_response({'status': 'started'})


async def initiate_full_scan(request: Request) -> Response:
    ScanService(request).initiate_full_scan()
    return json_response({'status': 'started'})
