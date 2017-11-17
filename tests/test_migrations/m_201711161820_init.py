from auto_migrator.model import BaseMigration
from tests.sample_model import Person
from auto_migrator.repository import migration
from peewee import CharField
from playhouse.migrate import SchemaMigrator

@migration
class init(BaseMigration):
    def up(self, migrator: SchemaMigrator):
        Person._meta.database = migrator.database
        Person.create_table()
        return (
            migrator.add_column('sample_person_table', 'test1', CharField(default='sample_test2_value')),
            migrator.add_column('sample_person_table', 'test2', CharField(default='sample_test2_value'))
        )


    def down(self, migrator):
        return (
            migrator.drop_column('sample_person_table', 'test1'),
            migrator.drop_column('sample_person_table', 'test2'),
        )
