from datetime import datetime, date
from typing import List, Optional

from fastapi_users.db import (SQLAlchemyBaseUserTable,
                              SQLAlchemyBaseOAuthAccountTable)
from sqlalchemy import (Table, Column, JSON, TIMESTAMP, 
                        Boolean, Integer, String, ForeignKey,
                        ARRAY, DATE)
from sqlalchemy.orm import mapped_column, Mapped, relationship, declared_attr

from .enums import SexEnum, RelationshipStatusEnum
from database import Base
from utils import unique_int_list
# ИМПЕРАТИВНЫЙ 
# role = Table(
#     'role',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String, nullable=False),
#     Column('permissions', JSON),
#     # extend_existing=True
# )
class Role(Base):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(56))
    permissions: Mapped[Optional[dict]] = mapped_column(JSON)

    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="role"
    )

# advice: называть классы и таблицы в ед. числе, чтобы были одинаковые имена
# и не было ошибок
# ДЕКЛАРАТИВНЫЙ заставляет писать FastAPI, но в целом без разницы, как удобнее так и пишем
class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'
    # __table_args__ = {'extend_existing':True}   

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(Role.id))
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    friend_list: Mapped[unique_int_list]
    sent_friend_reqest: Mapped[unique_int_list]
    received_friend_requests: Mapped[unique_int_list]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users"
    )
    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship(
        "OAuthAccount", 
        back_populates= "user",
        lazy="joined"
    )
    user_data: Mapped["UserDataExtended"] = relationship(
        "UserDataExtended",
        back_populates= "user"
    )


class UserDataExtended(Base):
    __tablename__ = "user_data_extended"

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="cascade"),primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    unique_id: Mapped[str] = mapped_column(String(58), nullable=True, unique=True)
    birth_date: Mapped[date] = mapped_column(DATE, nullable=True)
    sex: Mapped["SexEnum"] = mapped_column(nullable=True) 
    relat_status: Mapped["RelationshipStatusEnum"] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    education: Mapped[str] = mapped_column(String(100), nullable=True)
    interests: Mapped[str] = mapped_column(String(500), nullable=True)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_data"
    )

#OAuth
class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
    __tablename__ = "oauth_account"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, 
                                         ForeignKey(User.id, ondelete="cascade"), nullable=False)
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates= "oauth_accounts"
    )
    #SQLAlchemyBaseOAuthAccountTable ожидается, 
    #что общий тип будет определять фактический тип используемого вами идентификатора.
    # @declared_attr
    # def user_id(cls) -> Mapped[int]:
    #     return mapped_column(Integer, 
    #     ForeignKey("user_id", ondelete="cascade"), nullable=False