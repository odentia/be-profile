from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('profiles',
    sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('avatar_url', sa.String(length=500), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    
    op.create_table('themes',
    sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
    sa.Column('text_color', sa.String(length=7), nullable=False),
    sa.Column('main_bg_color', sa.String(length=7), nullable=False),
    sa.Column('second_bg_color', sa.String(length=7), nullable=False),
    sa.Column('contrast_color', sa.String(length=7), nullable=False),
    sa.Column('highlight_color', sa.String(length=7), nullable=False),
    sa.Column('blur_transparency', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('themes')
    op.drop_table('profiles')

