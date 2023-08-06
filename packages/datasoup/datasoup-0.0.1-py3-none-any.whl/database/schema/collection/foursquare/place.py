import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.schema.collection.collection import Collection
from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base

class FoursquarePlaceSearch(Collection):

    __tablename__ = "foursquare_place_search"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collection.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    method = mapped_column(String(50), nullable=False)
    version = mapped_column(String(25), nullable=False)
    params = mapped_column(Text, nullable=False)

    queries = relationship("FoursquarePlaceSearchQuery", back_populates="search")

    __mapper_args__ = {
        "polymorphic_identity": "foursquare_place_search",
    }

    def __repr__(self) -> str:
        return repr_factory(self, id=self.id, user=self.method, blah=self.version, params=self.params)


class FoursquarePlaceSearchQuery(Base):

    __tablename__ = "foursquare_place_search_query"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    depth = mapped_column(SmallInteger, nullable=False, default=0)
    latitude_n = mapped_column(Float, nullable=False)
    longitude_e = mapped_column(Float, nullable=False)
    latitude_s = mapped_column(Float, nullable=False)
    longitude_w = mapped_column(Float, nullable=False)
    datetime = mapped_column(DateTime, nullable=False)
    status = mapped_column(SmallInteger, nullable=False, default=0)
    error = mapped_column(Text, nullable=False, default="")

    search_id = mapped_column(ForeignKey("foursquare_place_search.id"))
    search = relationship("FoursquarePlaceSearch", back_populates="queries")

    query_attributes = relationship("FoursquarePlaceSearchQueryAttribute", back_populates="query")

    results = relationship("FoursquarePlaceSearchResult", back_populates="query")
    def __repr__(self) -> str:
        return repr_factory(self)


class FoursquarePlaceSearchQueryAttribute(Base):

    __tablename__ = "foursquare_place_search_query_attribute"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    key = mapped_column(String(50), nullable=False)
    value = mapped_column(String(100), nullable=False)

    query_id = mapped_column(ForeignKey("foursquare_place_search_query.id"))
    query = relationship("FoursquarePlaceSearchQuery", back_populates="query_attributes")

class FoursquarePlaceSearchResult(Base):

    __tablename__ = "foursquare_place_search_result"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    rank = mapped_column(SmallInteger, nullable=False)
    distance = mapped_column(SmallInteger, nullable=False)

    query_id = mapped_column(ForeignKey("foursquare_place_search_query.id"))
    query = relationship("FoursquarePlaceSearchQuery", back_populates="results")

    entity_id = mapped_column(ForeignKey("foursquare_place_entity.id"))
    entity = relationship("FoursquarePlaceEntity", back_populates="query_results")

    def __repr__(self) -> str:
        return repr_factory(self)


class FoursquarePlaceEntity(Base):

    __tablename__ = "foursquare_place_entity"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(100), nullable=False)
    fsq_id = mapped_column(String(50), nullable=False)
    fsq_link = mapped_column(String(75), nullable=False)
    latitude = mapped_column(Float, nullable=False)
    longitude = mapped_column(Float, nullable=False)

    description = mapped_column(Text, nullable=True)
    date_closed = mapped_column(DateTime, nullable=True)
    website = mapped_column(String(100), nullable=True)
    email = mapped_column(String(100), nullable=True)
    tel = mapped_column(String(100), nullable=True)
    fax = mapped_column(String(100), nullable=True)
    twitter = mapped_column(String(100), nullable=True)
    facebook = mapped_column(String(100), nullable=True)
    instagram = mapped_column(String(100), nullable=True)
    verified = mapped_column(Boolean, nullable=True)
    store_id = mapped_column(String(50), nullable=True)
    price = mapped_column(SmallInteger, nullable=True)
    rating = mapped_column(Float, nullable=True)
    popularity = mapped_column(Float, nullable=True)
    addr_sub = mapped_column(String(100), nullable=True)
    addr_street = mapped_column(String(100), nullable=True)
    addr_locality = mapped_column(String(100), nullable=True)
    addr_region = mapped_column(String(25), nullable=True)
    addr_postcode = mapped_column(String(25), nullable=True)
    addr_country = mapped_column(String(2), nullable=True)
    addr_format = mapped_column(String(100), nullable=True)
    timezone = mapped_column(String(50), nullable=True)
    total_photos = mapped_column(SmallInteger, nullable=True)
    total_ratings = mapped_column(SmallInteger, nullable=True)
    total_tips = mapped_column(SmallInteger, nullable=True)

    query_results = relationship("FoursquarePlaceSearchResult", back_populates="entity")
    categories = relationship("FoursquarePlaceEntityCategory", back_populates="entity")
    features = relationship("FoursquarePlaceEntityFeature", back_populates="entity")
    attributes = relationship("FoursquarePlaceEntityAttribute", back_populates="entity")
    related_places = relationship("FoursquarePlaceEntityRelated", back_populates="entity")
    hours = relationship("FoursquarePlaceEntityHours", back_populates="entity")
    tips = relationship("FoursquarePlaceEntityTip", back_populates="entity")
    photos = relationship("FoursquarePlaceEntityPhoto", back_populates="entity")

    def __repr__(self) -> str:
        return repr_factory(self)


class FoursquarePlaceEntityCategory(Base):

    __tablename__ = "foursquare_place_entity_category"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)

    entity_id = mapped_column(ForeignKey("foursquare_place_entity.id"))
    entity = relationship("FoursquarePlaceEntity", back_populates="categories")

    def __repr__(self) -> str:
        return repr_factory(self)


class FoursquarePlaceEntityFeature(Base):

    __tablename__ = "foursquare_place_entity_feature"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    value = mapped_column(Boolean, nullable=False)

    entity_id = mapped_column(ForeignKey("foursquare_place_entity.id"))
    entity = relationship("FoursquarePlaceEntity", back_populates="features")

    def __repr__(self) -> str:
        return repr_factory(self)


class FoursquarePlaceEntityAttribute(Base):

    __tablename__ = "foursquare_place_entity_attribute"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    value = mapped_column(String(100), nullable=False)

    entity_id = mapped_column(ForeignKey("foursquare_place_entity.id"))
    entity = relationship("FoursquarePlaceEntity", back_populates="attributes")

    def __repr__(self) -> str:
        return repr_factory(self)


class FoursquarePlaceEntityRelated(Base):

    __tablename__ = "foursquare_place_entity_related"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(100), nullable=False)
    type = mapped_column(String(25), nullable=False)

    fsq_id = mapped_column(String(50), nullable=True)

    entity_id = mapped_column(ForeignKey("foursquare_place_entity.id"))
    entity = relationship("FoursquarePlaceEntity", back_populates="related_places")

    def __repr__(self) -> str:
        return repr_factory(self)


class FoursquarePlaceEntityHours(Base):

    __tablename__ = "foursquare_place_entity_hours"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    day = mapped_column(SmallInteger, nullable=False)

    open = mapped_column(Time, nullable=True)
    close = mapped_column(Time, nullable=True)

    entity_id = mapped_column(ForeignKey("foursquare_place_entity.id"))
    entity = relationship("FoursquarePlaceEntity", back_populates="hours")

    def __repr__(self) -> str:
        return repr_factory(self)


class FoursquarePlaceEntityTip(Base):

    __tablename__ = "foursquare_place_entity_tip"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


    text = mapped_column(Text, nullable=False)

    created_at = mapped_column(DateTime, nullable=True)

    entity_id = mapped_column(ForeignKey("foursquare_place_entity.id"))
    entity = relationship("FoursquarePlaceEntity", back_populates="tips")

    def __repr__(self) -> str:
        return repr_factory(self)


class FoursquarePlaceEntityPhoto(Base):

    __tablename__ = "foursquare_place_entity_photo"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    url = mapped_column(String(100), nullable=False)

    created_at = mapped_column(DateTime, nullable=True)
    classification = mapped_column(Text, nullable=True)

    entity_id = mapped_column(ForeignKey("foursquare_place_entity.id"))
    entity = relationship("FoursquarePlaceEntity", back_populates="photos")

    def __repr__(self) -> str:
        return repr_factory(self)
