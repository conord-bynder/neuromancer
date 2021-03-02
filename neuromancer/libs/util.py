from datetime import (
    datetime,
    timezone)
from math import floor
from typing import (
    Dict,
    List)

from sqlalchemy.orm.collections import InstrumentedList


class ModelUtils:
    SERIALIZATION_FIELDS: List[str] = []

    def serialize_to_json(self,  # pragma : no cover
                          fields: List = None) -> Dict:
        if fields is None:
            fields = self.SERIALIZATION_FIELDS

        serialized_model = {}
        for field in fields:
            value = getattr(self, field, None)
            if isinstance(value, InstrumentedList):
                value = [p.serialize_to_json() for p in value]
            elif value not in [None, True, False]:
                value = str(value)
            serialized_model[field] = value
        return serialized_model


def convert_date_to_timestamp(date_time: datetime) -> int:
    """ Take a datetime format and convert it to a long timestamp.
    """
    return floor(
        date_time.replace(tzinfo=timezone.utc).timestamp() * 1000)
