import atexit
import os
from datetime import datetime
from sqlalchemy import create_engine, String, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped, relationship
from dotenv import load_dotenv

load_dotenv()


PG_DSN = (f'postgresql://{os.getenv("POSTGRES_USER")}:'
          f'{os.getenv("POSTGRES_PASSWORD")}'
          f'@{os.getenv("POSTGRES_HOST")}:'
          f'{os.getenv("POSTGRES_PORT")}/'
          f'{os.getenv("POSTGRES_DB")}')

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(String(150), unique=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="ads")

    @property
    def dict(self):
        return {
            "id": self.id,
            "header": self.header,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            # "owner": self.owner_id
        }


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(180), nullable=False)
    registration_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    ads = relationship("Advertisement", back_populates="owner")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time.isoformat(),
            # "ads": Session.
        }


Base.metadata.create_all(bind=engine)

