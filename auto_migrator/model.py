from abc import ABCMeta, abstractmethod
from playhouse.migrate import Operation
from typing import Set
from peewee import Model
from peewee import CharField
from playhouse.migrate import SchemaMigrator


class BaseMigration(metaclass=ABCMeta):
    @abstractmethod
    def up(self, migrator: SchemaMigrator) -> Set[Operation]: ...

    @abstractmethod
    def down(self, migrator: SchemaMigrator) -> Set[Operation]: ...


class MigrationModel(Model):
    migration_id = CharField(primary_key=True)

    class Meta:
        db_table = '__migrations_history'


class Migration:
    def __init__(self, name: str, cls: type, applied: [bool or None]):
        self.name = name
        self.cls = cls
        self.applied = applied
