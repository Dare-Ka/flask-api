import atexit
from datetime import datetime
from sqlalchemy import create_engine, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped

POSTGRES_PASSWORD = '92311'
POSTGRES_USER = 'postgres'
POSTGRES_DB = 'ad_api'
POSTGRES_HOST = '127.0.0.1'
POSTGRES_PORT = '5432'

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

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
    owner: ...

    @property
    def dict(self):
        return {
            "id": self.id,
            "header": self.header,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "owner": self.owner
        }


Base.metadata.create_all(bind=engine)

