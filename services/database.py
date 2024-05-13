import sqlalchemy as sqla
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = sqla.Column(sqla.BigInteger, primary_key=True)
    username = sqla.Column(sqla.String)


class RelationalDatabase(User):
    def __init__(self, engine, async_session):
        self.engine = engine
        self.users_table = User
        self.async_session = async_session

    async def create_tables(self):
        """ Создает таблицы в Database. """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)  # Создаем и добавляем таблицу в database
            await conn.commit()

    async def adding_user(self, username: str, user_id: int) -> None:
        """ Принимает имя и id пользователя; если еще не создан - добавляет его в Database. """
        async with self.async_session() as session:
            elem = User(user_id=user_id, username=username)
        try:
            session.add(elem)
            await session.commit()
        except IntegrityError:
            print(f"Пользователь {username} уже создан!")

    async def counting(self) -> int:
        """ Считает количество пользователей в боте. """
        async with self.async_session() as session:
            select_all_query = sqla.select(self.users_table)
            select_all_results = await session.execute(select_all_query)
            return len(select_all_results.fetchall())
