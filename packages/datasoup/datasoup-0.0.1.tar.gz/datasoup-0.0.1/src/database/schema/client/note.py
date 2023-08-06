import datetime
import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base


class ClientNote(Base):
    __tablename__ = "client_note"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = mapped_column(String(50), nullable=False)
    note = mapped_column(Text, nullable=False)
    created = mapped_column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = mapped_column(DateTime, nullable=False, onupdate=datetime.datetime.now)

    client_id = mapped_column(ForeignKey("client.id"))
    client = relationship("Client", back_populates="notes")

    def __repr__(self) -> str:
        return repr_factory(self)
