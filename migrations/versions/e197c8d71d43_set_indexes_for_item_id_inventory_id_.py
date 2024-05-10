"""set indexes for item.id, inventory.id and inventory_item.inventory_id

Revision ID: e197c8d71d43
Revises: e5466636118d
Create Date: 2024-05-10 16:02:03.184859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e197c8d71d43'
down_revision: Union[str, None] = 'e5466636118d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_inventory_id'), 'inventory', ['id'], unique=False)
    op.create_index(op.f('ix_inventory_item_inventory_id'), 'inventory_item', ['inventory_id'], unique=False)
    op.create_index(op.f('ix_item_id'), 'item', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_id'), table_name='item')
    op.drop_index(op.f('ix_inventory_item_inventory_id'), table_name='inventory_item')
    op.drop_index(op.f('ix_inventory_id'), table_name='inventory')
    # ### end Alembic commands ###