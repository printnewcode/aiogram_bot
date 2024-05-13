import os

from aiogram import Bot, Dispatcher
import asyncio
from dotenv import load_dotenv
import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from handlers.user.__init__ import get_user_handlers_router
from handlers.admin.__init__ import get_admin_handlers_router
from services.database import RelationalDatabase as RelatDb

load_dotenv()

logging.basicConfig(level=logging.INFO)  # Включаем логирование


async def main() -> None:
    bot = Bot(token=os.getenv("TOKEN"))
    engine = create_async_engine('postgresql+asyncpg:///base2.db', echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    db = RelatDb(engine, async_session)
    dp = Dispatcher(
        bot=bot,
        engine=engine,
        db=db,
        async_session=async_session

    )
    dp.include_routers(get_admin_handlers_router(), get_user_handlers_router())
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
