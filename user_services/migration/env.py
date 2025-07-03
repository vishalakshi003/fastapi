import os
import logging
from logging.config import fileConfig
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from src.core.database import Base
from src.models.address import Address
from src.models.user_profile import UserPersonalProfile
from src.models.customuser import CustomUser
from src.models.rolemaster import RoleMaster
from src.models.rolemapping import RoleMapping
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# logger.info(f"Initial sys.path: {sys.path}")
# logger.info(f"__file__: {__file__}")
config = context.config


database_url = os.getenv("DATABASE_URL")
if database_url:

    # logger.info(f"Alembic using DATABASE_URL from environment: {database_url}")
    config.set_main_option("sqlalchemy.url", database_url)
else:
    print('Alembic using DATABASE_URL from alembic.ini')
    # logger.info("Alembic using DATABASE_URL from alembic.ini")



if config.config_file_name is not None:
    fileConfig(config.config_file_name)


connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

with connectable.connect() as connection:
    context.configure(
        connection=connection, target_metadata=Base.metadata
    )

    with context.begin_transaction():
        context.run_migrations()


