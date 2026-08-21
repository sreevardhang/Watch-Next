from sqlalchemy import String, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    watchlist_items: Mapped[list["WatchlistItem"]] = relationship(back_populates="user")

    watched_movies: Mapped[list["WatchedMovie"]] = relationship(back_populates="user")

class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    movie_id: Mapped[int] = mapped_column(nullable=False)

    movie_title: Mapped[str] = mapped_column(String(255), nullable=False)

    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="watchlist_items")

    __table_args__ = (UniqueConstraint("user_id", "movie_id"),)

class WatchedMovie(Base):
    __tablename__ = "watched_movies"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    movie_id: Mapped[int] = mapped_column(nullable=False)

    movie_title: Mapped[str] = mapped_column(String(255), nullable=False)

    watched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="watched_movies")

    __table_args__ = (UniqueConstraint("user_id", "movie_id"),)