import uuid

from sqlalchemy.orm import DeclarativeBase

from src.database.utils.fields.custom_uuid import CustomUUID


class Base(DeclarativeBase):
    type_annotation_map = {
        uuid.UUID: CustomUUID,
    }