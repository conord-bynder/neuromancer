from aiohttp.web import Request


class ServiceBase:
    def __init__(self, request: Request):

        self.config = request.app['config']

        if request['alchemy_transaction']:
            self.alchemy_transaction = request['alchemy_transaction']
        if request.app['connection_manager']:
            self.connection = request.app['connection_manager']
