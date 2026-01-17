from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLite не поддерживает ALTER COLUMN напрямую, поэтому используем пересоздание таблицы
    # Проверяем, есть ли старые поля (для обратной совместимости)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('themes')]
    
    # Если старые поля есть, делаем миграцию данных
    if 'text_color' in columns:
        # Добавляем новые поля только если их еще нет
        if 'backgroundColor' not in columns:
            op.add_column('themes', sa.Column('backgroundColor', sa.String(length=50), nullable=True))
        if 'backgroundColorMain' not in columns:
            op.add_column('themes', sa.Column('backgroundColorMain', sa.String(length=50), nullable=True))
        if 'backgroundColorSub' not in columns:
            op.add_column('themes', sa.Column('backgroundColorSub', sa.String(length=50), nullable=True))
        if 'boxShadow' not in columns:
            op.add_column('themes', sa.Column('boxShadow', sa.String(length=100), nullable=True))
        if 'danger' not in columns:
            op.add_column('themes', sa.Column('danger', sa.String(length=50), nullable=True))
        if 'border' not in columns:
            op.add_column('themes', sa.Column('border', sa.String(length=50), nullable=True))
        if 'subtext' not in columns:
            op.add_column('themes', sa.Column('subtext', sa.String(length=50), nullable=True))
        if 'text' not in columns:
            op.add_column('themes', sa.Column('text', sa.String(length=50), nullable=True))
        if 'attention' not in columns:
            op.add_column('themes', sa.Column('attention', sa.String(length=50), nullable=True))
        if 'glowColor' not in columns:
            op.add_column('themes', sa.Column('glowColor', sa.String(length=50), nullable=True))
        if 'glowOpacity' not in columns:
            op.add_column('themes', sa.Column('glowOpacity', sa.String(length=10), nullable=True))
        if 'cards' not in columns:
            op.add_column('themes', sa.Column('cards', sa.String(length=50), nullable=True))
        if 'circleColor' not in columns:
            op.add_column('themes', sa.Column('circleColor', sa.String(length=50), nullable=True))
        
        # Заполняем новые поля из старых
        op.execute("""
            UPDATE themes SET
                backgroundColor = COALESCE(main_bg_color, '#14141A'),
                backgroundColorMain = COALESCE(main_bg_color, '#14141A'),
                backgroundColorSub = COALESCE(second_bg_color, '#272A33'),
                boxShadow = 'rgba(0, 0, 0, 0.1)',
                danger = '#ff4444',
                border = COALESCE(second_bg_color, '#272A33'),
                subtext = '#a0a0a0',
                text = COALESCE(text_color, '#ffffff'),
                attention = '#ffaa00',
                glowColor = COALESCE(contrast_color, '#6C63FF'),
                glowOpacity = CASE 
                    WHEN blur_transparency IS NOT NULL THEN CAST(blur_transparency / 100.0 AS TEXT)
                    ELSE '0.3'
                END,
                cards = '#1e1e24',
                circleColor = COALESCE(contrast_color, '#6C63FF')
        """)
        
        # Удаляем старые поля только если они есть
        if 'text_color' in columns:
            op.drop_column('themes', 'text_color')
        if 'main_bg_color' in columns:
            op.drop_column('themes', 'main_bg_color')
        if 'second_bg_color' in columns:
            op.drop_column('themes', 'second_bg_color')
        if 'contrast_color' in columns:
            op.drop_column('themes', 'contrast_color')
        if 'highlight_color' in columns:
            op.drop_column('themes', 'highlight_color')
        if 'blur_transparency' in columns:
            op.drop_column('themes', 'blur_transparency')


def downgrade() -> None:
    # Добавляем обратно старые поля
    op.add_column('themes', sa.Column('text_color', sa.String(length=7), nullable=True))
    op.add_column('themes', sa.Column('main_bg_color', sa.String(length=7), nullable=True))
    op.add_column('themes', sa.Column('second_bg_color', sa.String(length=7), nullable=True))
    op.add_column('themes', sa.Column('contrast_color', sa.String(length=7), nullable=True))
    op.add_column('themes', sa.Column('highlight_color', sa.String(length=7), nullable=True))
    op.add_column('themes', sa.Column('blur_transparency', sa.Integer(), nullable=True))
    
    # Заполняем старые поля из новых
    op.execute("""
        UPDATE themes SET
            text_color = text,
            main_bg_color = backgroundColorMain,
            second_bg_color = backgroundColorSub,
            contrast_color = glowColor,
            highlight_color = glowColor,
            blur_transparency = CAST(glowOpacity AS DECIMAL) * 100
    """)
    
    # Делаем старые поля NOT NULL
    op.alter_column('themes', 'text_color', nullable=False, server_default='#ffffff')
    op.alter_column('themes', 'main_bg_color', nullable=False, server_default='#14141A')
    op.alter_column('themes', 'second_bg_color', nullable=False, server_default='#272A33')
    op.alter_column('themes', 'contrast_color', nullable=False, server_default='#6C63FF')
    op.alter_column('themes', 'highlight_color', nullable=False, server_default='#A785FF')
    op.alter_column('themes', 'blur_transparency', nullable=False, server_default='30')
    
    # Удаляем новые поля
    op.drop_column('themes', 'backgroundColor')
    op.drop_column('themes', 'backgroundColorMain')
    op.drop_column('themes', 'backgroundColorSub')
    op.drop_column('themes', 'boxShadow')
    op.drop_column('themes', 'danger')
    op.drop_column('themes', 'border')
    op.drop_column('themes', 'subtext')
    op.drop_column('themes', 'text')
    op.drop_column('themes', 'attention')
    op.drop_column('themes', 'glowColor')
    op.drop_column('themes', 'glowOpacity')
    op.drop_column('themes', 'cards')
    op.drop_column('themes', 'circleColor')
