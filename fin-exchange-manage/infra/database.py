from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

engine = create_engine('postgresql+psycopg2://root:root@localhost:5432/postgres', convert_unicode=True)


def _generate_session_maker() -> sessionmaker:
    return sessionmaker(autocommit=False,
                        autoflush=False,
                        bind=engine)


Base = declarative_base()


def init_db():
    # 在这里导入所有的可能与定义模型有关的模块，这样他们才会合适地
    # 在 metadata 中注册。否则，您将不得不在第一次执行 init_db() 时
    # 先导入他们。
    import model
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> scoped_session:
    """Provide a transactional scope around a series of operations."""

    session = scoped_session(_generate_session_maker())
    if session is None:
        raise Exception('schema is wrong')
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
