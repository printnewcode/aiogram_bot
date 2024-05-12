import sqlalchemy as sqla
from sqlalchemy.exc import IntegrityError


class RelationalDatabase:
    def __init__(self, engine):
        self.engine = engine
        self.metadata = sqla.MetaData()
        self.users_table = sqla.Table(
            'users',
            self.metadata,
            sqla.Column('id_user', sqla.Integer, primary_key=True),
            sqla.Column('username', sqla.String)
        )

    async def adding_data(self, username: str, user_id: int) -> None:
        """ Принимает имя и id пользователя; если еще не создан - добавляет его в Database. """

        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)  # Создаем и добавляем таблицу в database
        adding = self.users_table.insert().values([
            {'id_user': user_id, 'username': username}
        ])
        try:
            async with self.engine.begin() as conn:
                await conn.execute(adding)
                await conn.commit()
        except IntegrityError:
            print(f"Пользователь {username} уже создан!")

    async def counting(self) -> int:
        """ Считает количество пользователей в боте. """
        select_all_query = sqla.select(self.users_table)
        async with self.engine.begin() as conn:
            select_all_results = await conn.execute(select_all_query)
        return len(select_all_results.fetchall())
