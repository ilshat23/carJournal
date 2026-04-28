from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, String, Table, Integer, \
    Numeric, \
    ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from slugify import slugify

from app.core.constants import TagDBConstants as TC
from app.core.database import Base


repairs_tags = Table(
    'repairs_tags',
    Base.metadata,
    Column(
        'repair_id',
        Integer,
        ForeignKey('repairs.id'),
        index=True,
        primary_key=True
    ),
    Column(
        'tag_id',
        Integer,
        ForeignKey('tags.id'),
        index=True,
        primary_key=True
    )
)


class Repair(Base):
    __tablename__ = 'repairs'
    __table_args__ = (
        CheckConstraint('mileage >= 0', name='check_mileage_positive'),
        CheckConstraint('cost >= 0', name='check_cost_positive'),
        {
            'info': {'verbose_name': 'Ремонт',
                     'verbose_name_plural': 'Ремонты'}
        },
    )

    added_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    repaired_at: Mapped[datetime] = mapped_column(
        DateTime
    )
    description: Mapped[str] = mapped_column(String)
    mileage: Mapped[int | None] = mapped_column(Integer)
    cost: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))

    vehicle_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('vehicles.id')
    )
    vehicle: Mapped['Vehicle'] = relationship(
        'Vehicle',
        back_populates='repairs'
    )

    tags:Mapped[list['Tag']] = relationship(
        'Tag',
        secondary=repairs_tags,
        back_populates='repairs'
    )


class Tag(Base):
    __tablename__ = 'tags'
    __table_args__ = (
        {
            'info': {'verbose_name': 'Тег',
                     'verbose_name_plural': 'Теги'}
        },
    )

    name: Mapped[str] = mapped_column(String(TC.TAG_NAME_LEN), unique=True)
    slug: Mapped[str] = mapped_column(String(TC.TAG_NAME_LEN), unique=True)
    description: Mapped[str | None] = mapped_column(String(TC.TAG_DESC_LEN))

    repairs: Mapped[list['Repair']] = relationship(
        'Repair',
        secondary=repairs_tags,
        back_populates='tags'
    )

    def __init__(self, **kwargs):
        if 'slug' not in kwargs and 'name' in kwargs:
            kwargs['slug'] = slugify(
                kwargs['name'],
                lowercase=True,
                separator='-'
            )
            super().__init__(**kwargs)

    def __repr__(self):
        return f'<Tag {self.name}>'
