import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import event
from sqlalchemy.engine import Engine

import sunpeek.components as cmp
from sunpeek.common import utils
import sunpeek.definitions.collector_types
import sunpeek.definitions.fluid_definitions

db_url = utils.get_db_conection_string()


def init_db():
    # assert not database_exists(db_url), f"Database {db_url.split('/')[-1]} already exists, please set HIT_DB_NAME to a " \
    #                                     f"database doesn't exist yet, it will be created for you"

    utils.sp_logger.info(f'[init_db] Attempting to setup DB {os.environ.get("HIT_DB_NAME", "harvestit")} on '
                         f'{os.environ.get("HIT_DB_HOST", "localhost:5432")}')
    # engine = sqlalchemy.create_engine('/'.join(utils.get_db_conection_string().split('/')[:-1]))
    # engine.dispose()

    create_database(db_url)

    cmp.make_tables(utils.db_engine)

    with utils.S.begin() as session:
        # Add collector types
        for item in sunpeek.definitions.collector_types.all_definitions:
            session.add(item)

        # Add fluids
        for item in sunpeek.definitions.fluid_definitions.all_definitions:
            session.add(item)

        session.commit()
        session.expunge_all()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if os.environ.get('HIT_DB_TYPE', 'postgresql') == 'sqlite':
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


if __name__ == '__main__':
    init_db()
