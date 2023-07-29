from alembic import command

import bot
from alembic.config import Config as AlembicConfig
from config import settings

if __name__ == "__main__":
    alembic_config = AlembicConfig("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    command.upgrade(alembic_config, "head")
    bot.main()
