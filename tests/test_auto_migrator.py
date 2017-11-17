import unittest
from auto_migrator import MigrationModel
from peewee import SqliteDatabase

from auto_migrator import MigrationsRepository
from tests.sample_model import Person

test_db = SqliteDatabase('my_database.db')
if MigrationModel.table_exists():
    MigrationModel.drop_table()

if Person.table_exists():
    Person.drop_table()


class TestMigrationRepository(unittest.TestCase):
    repo: MigrationsRepository = MigrationsRepository(test_db, 'tests.test_migrations')

    def tearDown(self):
        if MigrationModel.table_exists():
            MigrationModel.drop_table()

    def test_coded_migration_should_load_at_least_one(self):
        migrations = self.repo.code_migrations()
        self.assertNotEqual(len(migrations), 0)
        self.assertEqual(migrations[0].name, 'm_201711161820_init')

    def test_db_migration_should_return_zero_on_empty(self):
        db_migrations = self.repo.db_migrations()
        self.assertEqual(len(db_migrations), 0)

    def test_all_migrations_one_not_applied_on_empty(self):
        migrations = self.repo.code_migrations()
        all_migrations = self.repo.all_migrations()

        self.assertEqual(len(all_migrations), 1)
        self.assertEqual(all_migrations[0].applied, False)

    def test_save_migration_should_insert_all_rows(self):
        self.repo.save(self.repo.all_migrations().pop())
        db_migrations = self.repo.db_migrations()

        self.assertEqual(len(db_migrations), 1)
        self.assertEqual(db_migrations[0].applied, True)


if __name__ == '__main__':
    unittest.main()
