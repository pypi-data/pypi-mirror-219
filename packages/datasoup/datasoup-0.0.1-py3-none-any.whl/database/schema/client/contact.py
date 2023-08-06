import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base


class ClientContact(Base):
    __tablename__ = "client_contact"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    type = mapped_column(String(25), nullable=False)
    contact = mapped_column(String(50), nullable=False)
    primary = mapped_column(Boolean, nullable=False, default=False)
    note = mapped_column(String(250), nullable=False, default="")

    client_id = mapped_column(ForeignKey("client.id"))
    client = relationship("Client", back_populates="contacts")

    def __repr__(self) -> str:
        return repr_factory(self)

