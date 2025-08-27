from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

from app.database import Base
from app.models import *  # чтобы Alembic видел модели
from app.config import settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL БД берём из настроек (переменные окружения)
config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=settings.database_url,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()