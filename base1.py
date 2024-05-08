import sqlalchemy as sqla
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

engine = sqla.create_engine('sqlite:///base2.db', echo=True)  # Создаем engine для sqla
conn = engine.connect()  # Открываем соединение
metadata = sqla.MetaData()  # Создаем метадату

Users = sqla.Table('users', metadata,
                   sqla.Column('id_user', sqla.Integer, primary_key=True),
                   sqla.Column('username', sqla.Text)
                   )

metadata.create_all(engine)  # Создаем и добавляем таблицу в database


async def adding_data(username: str, user_id: int) -> None:
    """ Принимает имя и id пользователя; если еще не создан - добавляет его в Database. """
    adding = Users.insert().values([
        {'id_user': user_id, 'username': username}
    ])
    try:
        conn.execute(adding)
        conn.commit()
    except IntegrityError:
        print(f"Пользователь {username} уже создан!")


async def counting() -> int:
    """ Считает количество пользователей в боте. """
    select_all_query = sqla.select(Users)
    select_all_results = conn.execute(select_all_query)
    return len(select_all_results.fetchall())
