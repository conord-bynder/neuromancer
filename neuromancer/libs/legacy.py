""" Library file dedicated to legacy coldfusion utilities we cannot get
    rid of yet.
"""
import logging
import uuid
from typing import (
    Any,
    Optional,
    Union)

from sqlalchemy import String, types

log = logging.getLogger(__name__)


# pylint: disable=abstract-method
class UUID(types.TypeDecorator):  # pragma: no cover
    """ Model UUID type representation.
    """
    impl = String

    def __init__(self) -> None:
        self.impl.length = 36
        super().__init__(length=self.impl.length)

    def process_bind_param(
            self, value: Any, dialect: Any = None) -> Optional[str]:
        ret_val = None
        if value and isinstance(value, uuid.UUID):
            ret_val = str(value)
        elif value and not isinstance(value, uuid.UUID):
            ret_val = str(uuid.UUID(value))
        return ret_val

    def process_result_value(
            self, value: Any, dialect: Any = None) -> Optional[uuid.UUID]:
        if not value:
            return None
        try:
            if isinstance(value, str):
                # Sometimes SQLAlchemy can return values padded with spaces.
                # UUIDs should never contain spaces, thus stripping them is
                # safe.
                value = value.strip()
            return uuid.UUID(value)
        except ValueError:
            log.debug("UUID %r not valid", value)
            raise


# pylint: disable=abstract-method
class CFUUID(UUID):  # pragma: no cover
    """ Model CFUUID type representation.
    """
    def process_bind_param(self, value: Any, dialect: Any = None) -> str:
        if value == '':  # This is for when it's an empty string in the db
            return value
        if value:
            if isinstance(value, uuid.UUID):
                return uuid_to_cfuuid(value)
            tmp_uuid = uuid.UUID(value)

            return uuid_to_cfuuid(tmp_uuid)
        return ''


def uuid_to_cfuuid(value: Union[str, uuid.UUID]) -> str:
    """ Convert a regular python UUID to the legacy coldfusion uuid format.
    """
    hex_ = str(value).upper().replace('-', '')
    return "-".join([hex_[:8], hex_[8:12], hex_[12:16], hex_[16:]])


def generate_cfuuid() -> str:
    """ Create a new uuid in the legacy coldfusion uuid format.
    """
    uuid_str = str(uuid.uuid4()).upper()
    split_uuid = uuid_str.split('-')
    return "-".join(split_uuid[:4]) + split_uuid[-1]
