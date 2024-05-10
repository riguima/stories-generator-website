from datetime import date
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from stories_generator_website.database import db
from stories_generator_website.utils import get_today_date


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    authenticated: Mapped[Optional[bool]] = mapped_column(default=False)
    is_admin: Mapped[Optional[bool]] = mapped_column(default=False)

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    create_date: Mapped[Optional[date]] = mapped_column(
        default=get_today_date()
    )
    name: Mapped[str]
    formatted_old_value: Mapped[Optional[str]]
    formatted_value: Mapped[str]
    installment: Mapped[Optional[str]]
    image_url: Mapped[str]
    url: Mapped[str]
    website: Mapped[str]


class Configuration(Base):
    __tablename__ = 'configurations'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    facebook: Mapped[Optional[str]]
    youtube: Mapped[Optional[str]]
    instagram: Mapped[Optional[str]]
    telegram: Mapped[Optional[str]]
    whatsapp: Mapped[Optional[str]]


Base.metadata.create_all(db)
