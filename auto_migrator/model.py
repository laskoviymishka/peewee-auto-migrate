from abc import ABCMeta
from playhouse.migrate import Operation
from typing import Set
from peewee import Model
from peewee import CharField
from playhouse.migrate import SchemaMigrator

class BaseMigration(metaclass=ABCMeta):
    def up(self, migrator: SchemaMigrator) -> Set[Operation]:
        pass

    def down(self, migrator: SchemaMigrator) -> Set[Operation]:
        pass


class MigrationModel(Model):
    migration_id = CharField(primary_key=True)

    class Meta:
        db_table = '__migrations_history'

class Migration:
    def __init__(self, name:str, cls:type, applied:bool):
        self.name = name
        self.cls = cls
        self.applied = applied
