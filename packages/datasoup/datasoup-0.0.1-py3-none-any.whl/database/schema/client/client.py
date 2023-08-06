import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base


class Client(Base):
    __tablename__ = "client"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    given_name = mapped_column(String(50), nullable=False)
    surname = mapped_column(String(50), nullable=False)

    org = mapped_column(String(50), nullable=True)

    notes = relationship("ClientNote", back_populates="client")
    contacts = relationship("ClientContact", back_populates="client")
    projects = relationship("Project", back_populates="client")

    def __repr__(self) -> str:
        return repr_factory(self)
