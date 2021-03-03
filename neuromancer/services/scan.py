import logging
from uuid import UUID
from aiohttp.web import Request
from neuromancer.repositories.feature import FeatureRepository
from neuromancer.repositories.portal import PortalRepository
from neuromancer.repositories.portal_setting import PortalSettingRepository
from neuromancer.repositories.portal_feature import PortalFeatureRepository

from neuromancer.services import ServiceBase

log = logging.getLogger(__name__)


class ScanService(ServiceBase):

    def initiate_scan(self, portal_id: str) -> None:

        # portal_setting_repo = PortalSettingRepository(self.alchemy_transaction)
        # portal_feature_repo = PortalFeatureRepository(self.alchemy_transaction)
        # feature_repo = FeatureRepository(self.alchemy_transaction)
        portal_repo = PortalRepository(self.alchemy_transaction)

        portal = portal_repo.get_by_pk(UUID(portal_id))
        portal_scan = self.scan_portal(portal_id)

        if portal_scan['status'] == 'Unsecure':
            portal.is_secure = False
            portal.theme = 'custom-conor'

    def scan_portal(self, portal_id: str) -> dict:
        return {'status': 'Unsecure'}
