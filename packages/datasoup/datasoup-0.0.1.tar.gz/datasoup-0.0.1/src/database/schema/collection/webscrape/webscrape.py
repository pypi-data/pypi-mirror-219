import uuid

from sqlalchemy import ForeignKey, String, Float, SmallInteger, Text, Boolean, DateTime, Time, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.schema.collection.collection import Collection
from src.database.utils.methods.repr import repr_factory
from src.database.schema.base import Base


class WebScrape(Collection):
    __tablename__ = "web_scrape"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collection.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    method = mapped_column(String(50), nullable=False)
    version = mapped_column(String(25), nullable=False)
    params = mapped_column(Text, nullable=False)

    queries = relationship("WebScrapeQueryResult", back_populates="search")

    __mapper_args__ = {
        "polymorphic_identity": "web_scrape",
    }

    def __repr__(self) -> str:
        return repr_factory(self, id=self.id, user=self.method, blah=self.version, params=self.params)


class WebScrapeQueryResult(Base):
    __tablename__ = "web_scrape_query_result"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    url = mapped_column(String(250), nullable=False)
    index = mapped_column(SmallInteger, nullable=False, default=0)
    size_kb = mapped_column(Integer, nullable=False, default=0)
    datetime = mapped_column(DateTime, nullable=False)
    status = mapped_column(SmallInteger, nullable=False, default=0)
    error = mapped_column(Text, nullable=False, default="")

    search_id = mapped_column(ForeignKey("web_scrape.id"))
    search = relationship("WebScrape", back_populates="queries")

    query_attributes = relationship("WebScrapeQueryAttribute", back_populates="query")

    object_id = mapped_column(ForeignKey("web_scrape_extract.id"))
    object = relationship("WebScrapeExtract", back_populates="query_results")

    def __repr__(self) -> str:
        return repr_factory(self)


class WebScrapeQueryAttribute(Base):
    __tablename__ = "web_scrape_query_attribute"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    key = mapped_column(String(50), nullable=False)
    value = mapped_column(String(100), nullable=False)

    query_id = mapped_column(ForeignKey("web_scrape_query_result.id"))
    query = relationship("WebScrapeQueryResult", back_populates="query_attributes")


class WebScrapeExtract(Base):
    __tablename__ = "web_scrape_extract"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    type = mapped_column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "web_scrape_extract",
        "polymorphic_on": "type",
    }

    def __repr__(self) -> str:
        return repr_factory(self)


class WebScrapeExtractBoolean(WebScrapeExtract):
    __tablename__ = "web_scrape_extract_boolean"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("web_scrape_extract.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    value = mapped_column(Boolean, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "extract_boolean",
    }

    def __repr__(self) -> str:
        return repr_factory(self)

class WebScrapeExtractInteger(WebScrapeExtract):
    __tablename__ = "web_scrape_extract_integer"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("web_scrape_extract.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    value = mapped_column(Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "extract_integer",
    }

    def __repr__(self) -> str:
        return repr_factory(self)


class WebScrapeExtractFloat(WebScrapeExtract):
    __tablename__ = "web_scrape_extract_float"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("web_scrape_extract.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    value = mapped_column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "extract_float",
    }

    def __repr__(self) -> str:
        return repr_factory(self)


class WebScrapeExtractText(WebScrapeExtract):
    __tablename__ = "web_scrape_extract_text"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("web_scrape_extract.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    value = mapped_column(Text, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "extract_text",
    }

    def __repr__(self) -> str:
        return repr_factory(self)


class WebScrapeExtractTextDict(WebScrapeExtract):
    __tablename__ = "web_scrape_extract_text_dict"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("web_scrape_extract.id"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = mapped_column(String(50), nullable=False)
    key = mapped_column(String(50), nullable=False)
    value = mapped_column(Text, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "extract_text_dict",
    }

    def __repr__(self) -> str:
        return repr_factory(self)