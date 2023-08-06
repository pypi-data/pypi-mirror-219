import pytest  # noqa: pycharm
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg

from kaiju_tools.docker import DockerContainer, DockerImage
from kaiju_tools.tests.fixtures import get_app

from kaiju_db.services import *

__all__ = [
    'postgres',
    'postgres_glob',
    'database_service',
    'test_table',
    'database_settings',
    'migrations_file',
    'migrations_service',
]

DB_NAME = 'pytest'
DB_PORT = 5444
ROOT_CREDENTIALS = {'user': 'postgres', 'password': 'postgres'}
DEFAULT_CREDENTIALS = {'user': 'test', 'password': 'test'}


@pytest.fixture
def database_settings():
    """Get default test database settings."""
    return {
        'host': 'localhost',
        'port': DB_PORT,
        'database': 'pytest',
        'user': 'test',
        'password': 'test',
        'root_user': 'postgres',
        'root_password': 'postgres',
        'root_database': 'postgres',
        'init_db': True,
        'init_tables': True,
        'pool_size': 10,
        'idle_connection_lifetime': 3600,
        'extensions': ['uuid-ossp', 'ltree'],
    }


def _pg_container(app):
    return DockerContainer(
        image=DockerImage(app=app, tag='postgres', version='14'),
        name='pytest-postgres',
        ports={'5432': str(DB_PORT)},
        env={'POSTGRES_USER': 'postgres', 'POSTGRES_PASSWORD': 'postgres'},
        healthcheck={
            'test': 'pg_isready',
            'interval': 100000000,
            'timeout': 3000000000,
            'start_period': 1000000000,
            'retries': 3,
        },
        sleep_interval=1,
        remove_on_exit=True,
        app=app,
    )


@pytest.fixture
def postgres(app):
    """Return a new database container. See `kaiju_tools.tests.fixtures.container` for more info."""
    with _pg_container(app) as c:
        yield c


@pytest.fixture(scope='session')
def postgres_glob(logger):
    """Return a new database container. See `kaiju_tools.tests.fixtures.per_session_container` for more info."""
    app = get_app(logger)
    with _pg_container(app) as c:
        yield c


@pytest.fixture
def database_service(postgres_glob, app, database_settings) -> DatabaseService:
    """Return a new instance of database service."""
    service = DatabaseService(app, metadata=sa.MetaData(), **database_settings)
    app.services.add_service(service)
    return service


@pytest.fixture
def migrations_file(tmp_path):
    path = tmp_path / 'migrations.json'
    return path


@pytest.fixture
def migrations_service(postgres_glob, app, database_service, mock_locks, migrations_file) -> DatabaseMigrationService:
    """Return a new instance of database service."""
    service = DatabaseMigrationService(
        app, database_service=database_service, migrations_file=str(migrations_file), locks_service=mock_locks
    )
    app.services.add_service(service)
    return service


@pytest.fixture
def test_table(database_service):
    t = sa.Table(
        'test_table',
        database_service.metadata,
        sa.Column('id', sa_pg.TEXT, primary_key=True),
        sa.Column('name', sa_pg.TEXT),
        sa.Column('value', sa_pg.INTEGER),
        sa.Column('enabled', sa_pg.BOOLEAN),
        sa.Column('timestamp', sa_pg.INTEGER),
        sa.Column('created', sa_pg.TIMESTAMP),
    )
    return t
