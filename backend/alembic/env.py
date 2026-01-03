# alembic/env.py
##FIXME: Need to fix the async for alembic migrations

from logging.config import fileConfig

import app.models  # noqa: F401
from alembic import context
from app.core.config import settings
from app.db.base import Base  # this triggers model imports via base.py
from sqlalchemy import engine_from_config, pool

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = settings.database_url_sync
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()
    
    

def run_migrations_online() -> None:
    config.set_main_option("sqlalchemy.url", settings.database_url_sync)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()
        
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()