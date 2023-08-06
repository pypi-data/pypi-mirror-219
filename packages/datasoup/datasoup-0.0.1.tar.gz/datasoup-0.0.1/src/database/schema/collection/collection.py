import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base


class Collection(Base):
    __tablename__ = "collection"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    type = mapped_column(String(50), nullable=False)
    datetime_start = mapped_column(DateTime, nullable=True)
    datetime_end = mapped_column(DateTime, nullable=True)

    epoch_id = mapped_column(ForeignKey("project_epoch.id"))
    epoch = relationship("ProjectEpoch", back_populates="collections")

    __mapper_args__ = {
        "polymorphic_identity": "collection",
        "polymorphic_on": "type",
    }
    def __repr__(self) -> str:
        return repr_factory(self)
