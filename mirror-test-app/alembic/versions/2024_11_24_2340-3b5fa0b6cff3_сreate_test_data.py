"""сreate test data

Revision ID: 3b5fa0b6cff3
Revises: 423d28a926b3
Create Date: 2024-11-24 23:40:10.175800

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

# revision identifiers, used by Alembic.
revision: str = "3b5fa0b6cff3"
down_revision: Union[str, None] = "423d28a926b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    try:
        op.execute(
        """
        INSERT INTO dog_walkers (id, name, phone_number)
        VALUES
        (2, 'Петр', '+79001234567'),
        (3, 'Андрей', '+79007654321'),
        (4, 'Марат', '+79407654381'),
        (5, 'Кирилл', '+79807654328'),
        (6, 'Маша', '+79077654326')
        """
    )
    except IntegrityError:
        pass


def downgrade() -> None:
    pass
