import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.schema.collection.collection import Collection
from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base


class GoogleWebSearch(Collection):
    __tablename__ = "google_web_search"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collection.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    method = mapped_column(String(50), nullable=False)
    version = mapped_column(String(25), nullable=False)
    params = mapped_column(Text, nullable=False)

    queries = relationship("GoogleWebSearchQuery", back_populates="search")

    __mapper_args__ = {
        "polymorphic_identity": "google_web_search",
    }

    def __repr__(self) -> str:
        return repr_factory(self, id=self.id, user=self.method, blah=self.version, params=self.params)


class GoogleWebSearchQuery(Base):
    __tablename__ = "google_web_search_query"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    query_string = mapped_column(String(50), nullable=False)
    datetime = mapped_column(DateTime, nullable=False)
    status = mapped_column(SmallInteger, nullable=False, default=0)
    error = mapped_column(Text, nullable=False, default="")

    search_id = mapped_column(ForeignKey("google_web_search.id"))
    search = relationship("GoogleWebSearch", back_populates="queries")

    query_attributes = relationship("GoogleWebSearchQueryAttribute", back_populates="query")

    results = relationship("GoogleWebSearchResult", back_populates="query")

    def __repr__(self) -> str:
        return repr_factory(self)


class GoogleWebSearchQueryAttribute(Base):
    __tablename__ = "google_web_search_query_attribute"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    key = mapped_column(String(50), nullable=False)
    value = mapped_column(String(100), nullable=False)

    query_id = mapped_column(ForeignKey("google_web_search_query.id"))
    query = relationship("GoogleWebSearchQuery", back_populates="query_attributes")


class GoogleWebSearchResult(Base):
    __tablename__ = "google_web_search_result"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    rank = mapped_column(SmallInteger, nullable=False)

    query_id = mapped_column(ForeignKey("google_web_search_query.id"))
    query = relationship("GoogleWebSearchQuery", back_populates="results")

    object_id = mapped_column(ForeignKey("google_web_search_object.id"))
    object = relationship("GoogleWebSearchObject", back_populates="query_results")

    def __repr__(self) -> str:
        return repr_factory(self)


class GoogleWebSearchObject(Base):
    __tablename__ = "google_web_search_object"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    kind = mapped_column(String(50), nullable=False)
    title = mapped_column(String(100), nullable=False)
    html_title = mapped_column(String(150), nullable=False)
    link = mapped_column(String(250), nullable=False)
    display_link = mapped_column(String(250), nullable=False)
    snippet = mapped_column(Text, nullable=False)
    html_snippet = mapped_column(Text, nullable=False)
    cache_id = mapped_column(String(50), nullable=False)
    formatted_url = mapped_column(String(250), nullable=False)
    html_formatted_url = mapped_column(String(250), nullable=False)

    mime = mapped_column(String(50), nullable=True)
    file_format = mapped_column(String(50), nullable=True)

    query_results = relationship("GoogleWebSearchResult", back_populates="object")
    labels = relationship("GoogleWebSearchObjectLabel", back_populates="object")
    pagemaps = relationship("GoogleWebSearchObjectPageMap", back_populates="object")
    images = relationship("GoogleWebSearchObjectImage", back_populates="object")


    def __repr__(self) -> str:
        return repr_factory(self)


class GoogleWebSearchObjectLabel(Base):
    __tablename__ = "google_web_search_object_label"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    label = mapped_column(String(50), nullable=False)

    object_id = mapped_column(ForeignKey("google_web_search_object.id"))
    object = relationship("GoogleWebSearchObject", back_populates="labels")

    def __repr__(self) -> str:
        return repr_factory(self)
    


class GoogleWebSearchObjectPageMap(Base):
    __tablename__ = "google_web_search_object_pagemap"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    key = mapped_column(String(50), nullable=False)
    value = mapped_column(String(100), nullable=False)

    object_id = mapped_column(ForeignKey("google_web_search_object.id"))
    object = relationship("GoogleWebSearchObject", back_populates="pagemaps")

    def __repr__(self) -> str:
        return repr_factory(self)

class GoogleWebSearchObjectImage(Base):
    __tablename__ = "google_web_search_object_image"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    context_link = mapped_column(String(50), nullable=False)
    thumbnail_link = mapped_column(String(50), nullable=False)

    object_id = mapped_column(ForeignKey("google_web_search_object.id"))
    object = relationship("GoogleWebSearchObject", back_populates="images")

    def __repr__(self) -> str:
        return repr_factory(self)

