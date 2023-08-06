import uuid
import datetime

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base


class ProjectNote(Base):
    __tablename__ = "project_note"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = mapped_column(String(50), nullable=False)
    note = mapped_column(Text, nullable=False)
    created = mapped_column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = mapped_column(DateTime, nullable=False, onupdate=datetime.datetime.now)

    project_id = mapped_column(ForeignKey("project.id"))
    project = relationship("Project", back_populates="notes")

    def __repr__(self) -> str:
        return repr_factory(self)
