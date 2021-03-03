import logging
from uuid import UUID
from aiohttp.web import Request

from neuromancer.libs.constants.features import FEATURES
from neuromancer.libs.constants.settings import (
    SETTINGS,
    DESIRED_SETTINGS,
    DESIRED_VALUES
)
from neuromancer.libs.constants.scoring import (
    SCORING,
    TOTAL_SCORE
)
from neuromancer.libs.legacy import uuid_to_cfuuid
from neuromancer.repositories.feature import FeatureRepository
from neuromancer.repositories.portal import PortalRepository
from neuromancer.repositories.portal_setting import PortalSettingRepository
from neuromancer.repositories.portal_feature import PortalFeatureRepository

from neuromancer.services import ServiceBase

log = logging.getLogger(__name__)


class ScanService(ServiceBase):

    def initiate_scan(self, portal_id: str) -> None:
        """ Scans a single portal to see if its secure
        """
        portal_repo = PortalRepository(self.alchemy_transaction)

        portal = portal_repo.get_by_pk(UUID(portal_id))
        portal_scan = self.scan_portal(portal_id)

        # If portal is not secure, then update accounts table with hack theme
        # and marks as insecure
        if portal_scan['status'] == 'Unsecure':
            log.error("WARNING WARNING PORTAL IS INSECURE")
            portal.is_secure = False
            portal.theme = 'custom-conor'
        if portal_scan['status'] == 'Secure':
            portal.is_secure = True

    def initiate_full_scan(self) -> None:
        """ Scans all active portals to see if they are secure
        """
        portal_repo = PortalRepository(self.alchemy_transaction)
        portals = portal_repo.list_by(filters={'is_active': True})

        for portal in portals:
            # Hardcode to only work for my portal for demo
            if portal.portal_id == UUID('FA905A75-39AA-4112-BF562F4E1B976B46'):
                log.error("SCANNING PORTAL: %s", portal.domain)
                portal_scan = self.scan_portal(portal.portal_id)
                if portal_scan['status'] == 'Unsecure':
                    log.error("WARNING WARNING PORTAL IS INSECURE")
                    portal.is_secure = False
                    portal.theme = 'custom-conor'
                if portal_scan['status'] == 'Secure':
                    portal.is_secure = True
                    portal.theme = ''

    def scan_portal(self, portal_id: str) -> dict:
        portal_setting_repo = PortalSettingRepository(self.alchemy_transaction)
        portal_feature_repo = PortalFeatureRepository(self.alchemy_transaction)
        portal_settings = portal_setting_repo.list_by(
            filters={'portal_id': portal_id})
        portal_features = portal_feature_repo.list_by(
            filters={'portal_id': portal_id})
        score = 0.0
        for feature in portal_features:
            if uuid_to_cfuuid(feature.feature_id) in FEATURES.keys():
                feat_score = SCORING[uuid_to_cfuuid(feature.feature_id)]
                score = score + feat_score

        for setting in portal_settings:
            setting_id = uuid_to_cfuuid(setting.setting_id)
            if setting_id in SETTINGS.keys():
                if setting_id in DESIRED_SETTINGS:
                    set_score = SCORING[setting_id]
                    score = score + set_score
                else:
                    desired_value = DESIRED_VALUES[setting_id]
                    set_score = SCORING[setting_id]
                    if desired_value in setting.value:
                        score = score + set_score
                    else:
                        score = score - set_score
        if score > TOTAL_SCORE:
            return {'status': 'Secure'}
        return {'status': 'Unsecure'}
