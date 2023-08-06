import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base


class Project(Base):
    __tablename__ = "project"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = mapped_column(String(50), nullable=False)
    description = mapped_column(Text, nullable=False, default="")

    client_id = mapped_column(ForeignKey("client.id"))
    client = relationship("Client", back_populates="projects")

    notes = relationship("ProjectNote", back_populates="project")
    epochs = relationship("ProjectEpoch", back_populates="project")

    def __repr__(self) -> str:
        return repr_factory(self)
