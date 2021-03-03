from typing import Type

from bynder_connectors.repositories.alchemy import AlchemyBaseRepository

from neuromancer.models.portal_setting import PortalSetting


class PortalSettingRepository(AlchemyBaseRepository):  # pragma: no cover
    """ PortalSetting repository for all main database interactions.
    """
    @property
    def typ(self) -> Type[PortalSetting]:
        return PortalSetting
