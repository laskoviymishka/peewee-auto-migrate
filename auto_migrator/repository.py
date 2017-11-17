from peewee import Database, Model, CharField
from auto_migrator.model import BaseMigration
from auto_migrator.model import MigrationModel
from auto_migrator.model import Migration
from playhouse.migrate import SqliteMigrator, SchemaMigrator, migrate
from abc import ABCMeta
from typing import List, TypeVar, Callable

from auto_migrator.utils import find

migrations: List[Migration] = []


def get_name(cls: type) -> str:
    return cls.__mro__[0].__module__.split('.').pop()


def migration(cls):
    migrations.append(Migration(get_name(cls), cls, None))
    return cls


class MigrationsRepository:
    def __init__(self, db: Database, migration_path: str = 'migrations'):
        self.db = db
        self.migrator = SchemaMigrator.from_database(self.db)
        MigrationModel._meta.database = db
        __import__(migration_path, locals=locals(), globals=globals())

    def code_migrations(self) -> List[Migration]:
        return migrations

    def db_migrations(self) -> List[Migration]:
        result = []
        if not MigrationModel.table_exists():
            MigrationModel.create_table()

        for row in MigrationModel.select():
            coded_item = find(migrations, lambda x: x.name == row.migration_id)
            if coded_item is None:
                raise ImportError('migration is not codded ' + row.migration_id)

            result.append(Migration(row.migration_id, coded_item, True))
        return result

    def all_migrations(self) -> List[Migration]:
        total = self.db_migrations()

        for migration in self.code_migrations():
            if not any(item.name == migration.name for item in total):
                migration.applied = False
                total.append(migration)

        return total

    def save(self, migration: Migration) -> None:
        with self.db.atomic():
            MigrationModel.insert(migration_id=migration.name).execute()


class CodeScafolder:
    def generate(self, migration: Migration) -> str:
        pass


class Migrator:
    def __init__(self, migration_repo: MigrationsRepository):
        self.migration_repo: MigrationsRepository = migration_repo

    def migrate(self, target_migration: str = None) -> None:
        with self.db.atomic():
            for migration in self.migration_repo.all_migrations():
                if not migration.applied and migration.name > target_migration:
                    migrate(migration.cls().up(self.migrator))
                    self.migration_repo.save(migration)
