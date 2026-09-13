from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String,ForeignKey


class Base(DeclarativeBase):
    pass

class users(Base):
    __tablename__ = "users"
    id:Mapped[int]=mapped_column(primary_key=True)
    email:Mapped[str]=mapped_column(String(255),unique=True,nullable=False)
    password_hash:Mapped[str]=mapped_column(String(255),nullable=False)

class documents(Base):
    __tablename__="documents"

    id:Mapped[int]=mapped_column(primary_key=True)
    filename:Mapped[str]=mapped_column(String(255),nullable=False)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
