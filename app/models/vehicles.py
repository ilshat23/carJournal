from datetime import datetime

from slugify import slugify
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import CategoryDBConstants as CC
from app.core.constants import VehicleDBConstants as VC
from app.core.database import Base


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        {
            'info': {'verbose_name': 'Категория ТС',
                     'verbose_name_plural': 'Категории ТС'}
        },
    )

    name: Mapped[str] = mapped_column(
        String(CC.CATEGORY_NAME_LEN),
        unique=True
    )
    slug: Mapped[str] = mapped_column(
        String(CC.CATEGORY_NAME_LEN),
        unique=True
    )
    description: Mapped[str | None] = mapped_column(
        String(CC.CATEGORY_DESC_LEN)
    )

    vehicles: Mapped[list['Vehicle']] = relationship(
        'Vehicle',
        back_populates='category'
    )

    def __init__(self, **kwargs):
        if 'slug' not in kwargs and 'name' in kwargs:
            kwargs['slug'] = slugify(
                kwargs['name'],
                lowercase=True,
                separator='-'
            )
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f'<Category {self.name}>'


class Vehicle(Base):
    __tablename__ = 'vehicles'

    name: Mapped[str] = mapped_column(String(VC.VEHICLE_NAME_LEN))
    horsepower: Mapped[int | None] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(
        String(VC.VEHICLE_DESC_LEN)
    )
    image_url: Mapped[str | None] = mapped_column(String(VC.IMAGE_URL_LEN))
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='vehicles'
    )

    category_slug: Mapped[str | None] = mapped_column(
        String,
        ForeignKey('categories.slug', ondelete='SET NULL'),
        index=True
    )
    category: Mapped['Category'] = relationship(
        'Category',
        back_populates='vehicles'
    )

    repairs: Mapped[list['Repair']] = relationship(
        'Repair',
        back_populates='vehicle',
        cascade='all, delete-orphan'
    )

