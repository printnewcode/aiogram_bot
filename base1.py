import sqlalchemy as sqla
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine('sqlite+aiosqlite:///base2.db', echo=True)  # Создаем engine для sqla
metadata = sqla.MetaData()  # Создаем метадату

Users = sqla.Table('users', metadata,
                   sqla.Column('id_user', sqla.Integer, primary_key=True),
                   sqla.Column('username', sqla.Text)
                   )


async def adding_data(username: str, user_id: int) -> None:
    """ Принимает имя и id пользователя; если еще не создан - добавляет его в Database. """

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)  # Создаем и добавляем таблицу в database
    adding = Users.insert().values([
        {'id_user': user_id, 'username': username}
    ])
    try:
        async with engine.begin() as conn:
            await conn.execute(adding)
            await conn.commit()
    except IntegrityError:
        print(f"Пользователь {username} уже создан!")


async def counting() -> int:
    """ Считает количество пользователей в боте. """
    select_all_query = sqla.select(Users)
    async with engine.begin() as conn:
        select_all_results = await conn.execute(select_all_query)
    return len(select_all_results.fetchall())
