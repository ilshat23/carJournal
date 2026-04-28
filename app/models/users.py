from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import UserDBConstants as UC
from app.core.database import Base


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(UC.USERNAME_LEN))
    email: Mapped[str] = mapped_column(String(UC.EMAIL_LEN))
    hashed_password: Mapped[str] = mapped_column(String(UC.PASSWORD_LEN))
    first_name: Mapped[str | None] = mapped_column(
        String(UC.FIRST_NAME_LEN)
    )
    last_name: Mapped[str | None] = mapped_column(
        String(UC.LAST_NAME_LEN)
    )
    avatar_url: Mapped[str | None] = mapped_column(String(UC.AVATAR_URL_LEN))
    registered_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=datetime.utcnow()
    )

    vehicles: Mapped[list['Vehicle']] = relationship(
        'Vehicle',
        cascade='all, delete-orphan',
        back_populates='user'
    )
    followers: Mapped[list['Subscription']] = relationship(
        'Subscription',
        foreign_keys='Subscription.following_id',
        back_populates='following',
        cascade='all, delete-orphan'
    )
    followings: Mapped[list['Subscription']] = relationship(
        'Subscription',
        foreign_keys='Subscription.follower_id',
        back_populates='follower',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Subscription(Base):
    __tablename__ = 'subscriptions'

    following_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    follower_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # followed_at: Mapped[datetime] = mapped_column(
    #     DateTime,
    #     defaut=datetime.utcnow()
    # )

    following: Mapped['User'] = relationship(
        'User',
        back_populates='followers',
        foreign_keys=[following_id]
    )
    follower: Mapped['User'] = relationship(
        'User',
        back_populates='followings',
        foreign_keys=[follower_id]
    )

    def __repr__(self) -> str:
        follower = self.follower.username if hasattr(self, 'follower') else self.follower_id
        following = self.following.username if hasattr(self, 'following') else self.following_id
        return f'<Subscription: {follower} follows {following}>'
