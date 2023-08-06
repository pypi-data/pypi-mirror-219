import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base


class ProjectEpoch(Base):
    __tablename__ = "project_epoch"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = mapped_column(String(50), nullable=False)

    goals = mapped_column(Text, nullable=True)
    datetime_start = mapped_column(DateTime, nullable=True)
    datetime_end = mapped_column(DateTime, nullable=True)

    project_id = mapped_column(ForeignKey("project.id"))
    project = relationship("Project", back_populates="epochs")

    collections = relationship("Collection", back_populates="epoch")

    def __repr__(self) -> str:
        return repr_factory(self)
