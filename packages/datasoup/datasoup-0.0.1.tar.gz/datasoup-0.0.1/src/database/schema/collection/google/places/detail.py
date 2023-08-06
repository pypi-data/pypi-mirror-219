import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.schema.collection.collection import Collection
from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base

class GooglePlacesDetail(Collection):

    __tablename__ = "google_places_detail"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collection.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    method = mapped_column(String(50), nullable=False)
    version = mapped_column(String(25), nullable=False)
    params = mapped_column(Text, nullable=False)

    queries = relationship("GooglePlacesDetailQueryResult", back_populates="search")

    __mapper_args__ = {
        "polymorphic_identity": "google_places_detail",
    }

    def __repr__(self) -> str:
        return repr_factory(self, id=self.id, user=self.method, blah=self.version, params=self.params)


class GooglePlacesDetailQueryResult(Base):

    __tablename__ = "google_places_detail_query_result"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    place_id = mapped_column(String(25), nullable=False)
    datetime = mapped_column(DateTime, nullable=False)
    status = mapped_column(SmallInteger, nullable=False, default=0)
    error = mapped_column(Text, nullable=False, default="")

    search_id = mapped_column(ForeignKey("google_places_detail.id"))
    search = relationship("GooglePlacesDetail", back_populates="queries")

    query_attributes = relationship("GooglePlacesDetailQueryAttribute", back_populates="query")

    entity_id = mapped_column(ForeignKey("google_places_detail_entity.id"))
    entity = relationship("GooglePlacesDetailEntity", back_populates="query_results")

    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesDetailQueryAttribute(Base):

    __tablename__ = "google_places_detail_query_attribute"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    key = mapped_column(String(50), nullable=False)
    value = mapped_column(String(100), nullable=False)

    query_id = mapped_column(ForeignKey("google_places_detail_query_result.id"))
    query = relationship("GooglePlacesDetailQueryResult", back_populates="query_attributes")

class GooglePlacesDetailResult(Base):

    __tablename__ = "google_places_detail_result"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    query_id = mapped_column(ForeignKey("google_places_detail_query_result.id"))
    query = relationship("GooglePlacesDetailQueryResult", back_populates="results")

    entity_id = mapped_column(ForeignKey("google_places_detail_entity.id"))
    entity = relationship("GooglePlacesDetailEntity", back_populates="query_results")

    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesDetailEntity(Base):

    __tablename__ = "google_places_detail_entity"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(100), nullable=True)
    place_id = mapped_column(String(50), nullable=True)
    place_url = mapped_column(String(75), nullable=True)
    latitude = mapped_column(Float, nullable=True)
    longitude = mapped_column(Float, nullable=True)
    status = mapped_column(String(50), nullable=True)
    summary = mapped_column(Text, nullable=True)
    website = mapped_column(String(100), nullable=True)
    int_tel = mapped_column(String(100), nullable=True)
    loc_tel = mapped_column(String(100), nullable=True)
    plus_code_global = mapped_column(String(50), nullable=True)
    plus_code_compound = mapped_column(String(50), nullable=True)
    reference = mapped_column(String(50), nullable=True)
    price = mapped_column(SmallInteger, nullable=True)
    rating = mapped_column(Float, nullable=True)
    addr_sub = mapped_column(String(100), nullable=True)
    addr_street = mapped_column(String(100), nullable=True)
    addr_locality = mapped_column(String(100), nullable=True)
    addr_region = mapped_column(String(25), nullable=True)
    addr_postcode = mapped_column(String(25), nullable=True)
    addr_country = mapped_column(String(2), nullable=True)
    addr_format = mapped_column(String(100), nullable=True)
    utc_offset = mapped_column(String(50), nullable=True)
    total_ratings = mapped_column(SmallInteger, nullable=True)

    query_results = relationship("GooglePlacesDetailResult", back_populates="entity")
    types = relationship("GooglePlacesDetailEntityType", back_populates="entity")
    features = relationship("GooglePlacesDetailEntityFeature", back_populates="entity")
    attributes = relationship("GooglePlacesDetailEntityAttribute", back_populates="entity")
    hours = relationship("GooglePlacesDetailEntityHours", back_populates="entity")
    reviews = relationship("GooglePlacesDetailEntityReview", back_populates="entity")
    photos = relationship("GooglePlacesDetailEntityPhoto", back_populates="entity")

    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesDetailEntityType(Base):

    __tablename__ = "google_places_detail_entity_type"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)

    entity_id = mapped_column(ForeignKey("google_places_detail_entity.id"))
    entity = relationship("GooglePlacesDetailEntity", back_populates="types")

    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesDetailEntityFeature(Base):

    __tablename__ = "google_places_detail_entity_feature"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    value = mapped_column(Boolean, nullable=False)

    entity_id = mapped_column(ForeignKey("google_places_detail_entity.id"))
    entity = relationship("GooglePlacesDetailEntity", back_populates="features")

    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesDetailEntityAttribute(Base):

    __tablename__ = "google_places_detail_entity_attribute"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    value = mapped_column(String(100), nullable=False)

    entity_id = mapped_column(ForeignKey("google_places_detail_entity.id"))
    entity = relationship("GooglePlacesDetailEntity", back_populates="attributes")

    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesDetailEntityHours(Base):

    __tablename__ = "google_places_detail_entity_hours"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    day = mapped_column(SmallInteger, nullable=False)

    open = mapped_column(Time, nullable=True)
    close = mapped_column(Time, nullable=True)

    entity_id = mapped_column(ForeignKey("google_places_detail_entity.id"))
    entity = relationship("GooglePlacesDetailEntity", back_populates="hours")

    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesDetailEntityReview(Base):

    __tablename__ = "google_places_detail_entity_tip"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


    text = mapped_column(Text, nullable=False)

    created_at = mapped_column(DateTime, nullable=True)
    author = mapped_column(String(50), nullable=False)
    rating = mapped_column(SmallInteger, nullable=False)

    entity_id = mapped_column(ForeignKey("google_places_detail_entity.id"))
    entity = relationship("GooglePlacesDetailEntity", back_populates="reviews")

    def __repr__(self) -> str:
        return repr_factory(self)


class GooglePlacesDetailEntityPhoto(Base):

    __tablename__ = "google_places_detail_entity_photo"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    url = mapped_column(String(100), nullable=False)

    reference = mapped_column(String(50), nullable=True)

    entity_id = mapped_column(ForeignKey("google_places_detail_entity.id"))
    entity = relationship("GooglePlacesDetailEntity", back_populates="photos")

    def __repr__(self) -> str:
        return repr_factory(self)
