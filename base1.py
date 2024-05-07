import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker

engine = sqla.create_engine('sqlite:///base2.db', echo=True)
conn = engine.connect()
metadata = sqla.MetaData()
Session = sessionmaker(autoflush=False, bind=engine)

Users = sqla.Table('users', metadata,
                   sqla.Column('id_user', sqla.Integer),
                   sqla.Column('username', sqla.Text)
                   )

metadata.create_all(engine)


async def adding_data(username: str, user_id: int) -> None:
    adding = Users.insert().values([
        {'id_user': user_id, 'username': username}
    ])
    # Не работает
    select_all_query = sqla.select(Users)
    select_all_results = conn.execute(select_all_query)
    print()
    if user_id not in select_all_results.fetchall() or username not in select_all_results.fetchall():
        conn.execute(adding)
        conn.commit()
    else:
        print("Пользователь уже создан")
