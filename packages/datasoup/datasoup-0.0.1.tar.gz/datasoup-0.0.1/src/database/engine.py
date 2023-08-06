from contextlib import contextmanager
from typing import ContextManager, Callable

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database.schema.client.client import Client
from database.schema.client.contact import ClientContact
from database.schema.client.note import ClientNote
from database.schema.collection.google.places.detail import GooglePlacesDetail
from database.schema.collection.google.places.search import GooglePlacesSearch
from database.schema.collection.google.search.search import GoogleWebSearch
from database.schema.collection.webscrape.webscrape import WebScrape
from database.schema.project.epoch import ProjectEpoch
from database.schema.project.notes import ProjectNote
from database.schema.project.project import Project
from src.database.schema.base import Base
from src.database.schema.collection.foursquare.place import FoursquarePlaceSearch


def initialize_db(path: str, echo=True) -> Callable[[], ContextManager[Session]]:

    sqla_engine = create_engine(f"sqlite:///{path}", echo=echo)

    Base.metadata.create_all(sqla_engine)

    @contextmanager
    def db_session() -> Callable[[], ContextManager[Session]]:
        session = Session(sqla_engine)
        try:
            yield session
        finally:
            session.close()

    return db_session


some_session2 = initialize_db("lala.db")

print(Client)
print(ClientContact)
print(ClientNote)
print(Project)
print(ProjectNote)
print(ProjectEpoch)

print(FoursquarePlaceSearch)
print(GooglePlacesSearch)
print(GooglePlacesDetail)
print(GoogleWebSearch)
print(WebScrape)



# with some_session2() as session:
#     f1 = GooglePlacesDetailSearch(method="blah", version="blah", params="blah")
#     session.add(f1)
#     session.commit()
#
#     f2 = session.scalars(select(FoursquarePlaceSearch)).all()
#     print(f2)
#
