from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    String,
    Text)

from neuromancer.libs.legacy import CFUUID
from neuromancer.libs.util import ModelUtils
from neuromancer.transactions import ModelBase

ACCOUNT_SETTING_TYPES = {'account', 'reseller', 'default'}


class PortalSetting(ModelBase, ModelUtils):
    __tablename__ = "account_settings"

    portal_setting_id = Column('id', CFUUID(), primary_key=True)
    portal_id = Column('contentId', CFUUID(), ForeignKey('accounts.id'))
    setting_id = Column('settingId', CFUUID())
    value = Column(Text(length=65535))
    locale = Column(String(10), default='')
    type = Column(Enum(*ACCOUNT_SETTING_TYPES,
                       name='account_setting_type'), default='account')
