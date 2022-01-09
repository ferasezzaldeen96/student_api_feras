"""Added uuid

Revision ID: 71283224890a
Revises: 
Create Date: 2022-01-06 16:20:17.458066

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '71283224890a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')


def downgrade():
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
