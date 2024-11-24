"""create dog_walker and order model

Revision ID: 423d28a926b3
Revises: 
Create Date: 2024-11-24 22:42:36.192218

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "423d28a926b3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dog_walkers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False, comment="Имя выгульщика собак"),
        sa.Column(
            "phone_number",
            sa.String(length=15),
            nullable=False,
            comment="Контактный номер выгульщика собак",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "apartment_number",
            sa.Integer(),
            nullable=False,
            comment="Номер квартиры заказчика",
        ),
        sa.Column("pet_name", sa.String(), nullable=False, comment="Кличка питомца"),
        sa.Column("pet_breed", sa.String(), nullable=False, comment="Порода питомца"),
        sa.Column(
            "walk_date",
            sa.DateTime(),
            nullable=False,
            comment="Дата и время начала прогулки",
        ),
        sa.Column(
            "dog_walker_id",
            sa.Integer(),
            nullable=False,
            comment="ID выгульщика",
        ),
        sa.ForeignKeyConstraint(
            ["dog_walker_id"], ["dog_walkers.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("walk_date", "dog_walker_id", name="unique_order"),
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table("orders")
    op.drop_table("dog_walkers")
    # ### end Alembic commands ###
