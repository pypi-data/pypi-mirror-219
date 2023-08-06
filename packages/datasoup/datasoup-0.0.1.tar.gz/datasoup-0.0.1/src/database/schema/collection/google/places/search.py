import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.schema.collection.collection import Collection
from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base

class GooglePlacesSearch(Collection):

    __tablename__ = "google_places_search"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collection.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    method = mapped_column(String(50), nullable=False)
    version = mapped_column(String(25), nullable=False)
    params = mapped_column(Text, nullable=False)

    queries = relationship("GooglePlacesSearchQuery", back_populates="search")

    __mapper_args__ = {
        "polymorphic_identity": "google_places_search",
    }
    def __repr__(self) -> str:
        return repr_factory(self, id=self.id, user=self.method, blah=self.version, params=self.params)


class GooglePlacesSearchQuery(Base):

    __tablename__ = "google_places_search_query"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    depth = mapped_column(SmallInteger, nullable=False, default=0)
    latitude_n = mapped_column(Float, nullable=False)
    longitude_e = mapped_column(Float, nullable=False)
    latitude_s = mapped_column(Float, nullable=False)
    longitude_w = mapped_column(Float, nullable=False)
    datetime = mapped_column(DateTime, nullable=False)
    status = mapped_column(SmallInteger, nullable=False, default=0)
    error = mapped_column(Text, nullable=False, default="")

    search_id = mapped_column(ForeignKey("google_places_search.id"))
    search = relationship("GooglePlacesSearch", back_populates="queries")

    query_attributes = relationship("GooglePlacesSearchQueryAttribute", back_populates="query")

    results = relationship("GooglePlacesSearchResult", back_populates="query")
    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesSearchQueryAttribute(Base):

    __tablename__ = "google_places_search_query_attribute"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    key = mapped_column(String(50), nullable=False)
    value = mapped_column(String(100), nullable=False)

    query_id = mapped_column(ForeignKey("google_places_search_query.id"))
    query = relationship("GooglePlacesSearchQuery", back_populates="query_attributes")

class GooglePlacesSearchResult(Base):

    __tablename__ = "google_places_search_result"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    rank = mapped_column(SmallInteger, nullable=False)
    distance = mapped_column(SmallInteger, nullable=False)

    query_id = mapped_column(ForeignKey("google_places_search_query.id"))
    query = relationship("GooglePlacesSearchQuery", back_populates="results")

    entity_id = mapped_column(ForeignKey("google_places_search_entity.id"))
    entity = relationship("GooglePlacesSearchEntity", back_populates="query_results")

    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesSearchEntity(Base):

    __tablename__ = "google_places_search_entity"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(100), nullable=True)
    place_id = mapped_column(String(50), nullable=True)
    latitude = mapped_column(Float, nullable=True)
    longitude = mapped_column(Float, nullable=True)
    status = mapped_column(String(50), nullable=True)
    plus_code_global = mapped_column(String(50), nullable=True)
    plus_code_compound = mapped_column(String(50), nullable=True)
    price = mapped_column(SmallInteger, nullable=True)
    rating = mapped_column(Float, nullable=True)
    vicinity = mapped_column(String(100), nullable=True)
    total_ratings = mapped_column(SmallInteger, nullable=True)

    query_results = relationship("GooglePlacesSearchResult", back_populates="entity")
    types = relationship("GooglePlacesSearchEntityType", back_populates="entity")
    
    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesSearchEntityType(Base):

    __tablename__ = "google_places_search_entity_type"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)

    entity_id = mapped_column(ForeignKey("google_places_search_entity.id"))
    entity = relationship("GooglePlacesSearchEntity", back_populates="types")

    def __repr__(self) -> str:
        return repr_factory(self)
