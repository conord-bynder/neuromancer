from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String,
)
from sqlalchemy.orm import relationship

from neuromancer.libs.legacy import CFUUID
from neuromancer.libs.util import ModelUtils
from neuromancer.transactions import ModelBase

FULL_SERIALIZATION_FIELDS = [
    'portal_id',
    'name',
    'domain',
    'is_active',
    'default_language',
    'date_created',
    'date_modified',
    'portal_type',
    'reseller_id']


class Portal(ModelBase, ModelUtils):
    __tablename__ = 'accounts'

    SERIALIZATION_FIELDS = ['portal_id', 'domain', 'name']

    portal_id = Column('id', CFUUID(), primary_key=True)
    name = Column(String(100))
    domain = Column(String(200))
    is_active = Column('isActive', Boolean, default=False)
    contact_name = Column('contactName', String(200))
    contact_email = Column('contactEmail', String(100))
    default_language = Column('defaultLocale', String(10), default='en_US')
    date_created = Column('dateCreated', DateTime(timezone=True),
                          default=datetime.utcnow)
    date_modified = Column('dateModified', DateTime(timezone=True),
                           default=datetime.utcnow)
    portal_type = Column('accountType', String(45))
    reseller_id = Column('resellerId', CFUUID())
    trial = Column('trial', Boolean, default=False)
    theme = Column('theme', String(100))
    bucket_prefix = Column('bucketPrefix', String(45), default='bynder')
    version = Column('version', String(5), default='')
    is_secure = Column('is_secure', Boolean, default=True)

    features = relationship('PortalFeature')
    settings = relationship('PortalSetting')
