import unittest
from auto_migrator import MigrationModel
from peewee import SqliteDatabase

from auto_migrator import BaseMigration, MigrationsRepository

test_db = SqliteDatabase(':memory:')

class Test_MigrationRepository(unittest.TestCase):
    repo = MigrationsRepository(test_db, 'tests.test_migrations')

    def test_coded_migration_should_load_at_least_one(self):
        migrations = self.repo.code_migrations()
        self.assertNotEqual(len(migrations), 0)
        self.assertEqual(migrations[0].name, 'm_201711161820_init')

    def test_db_migration_should_return_zero(self):
        db_migrations = self.repo.db_migrations()

        self.assertEqual(len(db_migrations), 0)


    def test_all_migrations_one_not_applied(self):
        all_migrations = self.repo.all_migrations()

        self.assertEqual(len(all_migrations), 1)
        self.assertEqual(all_migrations[0].applied, False)

    def test_save_migration_should_insert_all_rows(self):
        #act
        self.repo.save(self.repo.all_migrations().pop())
        all_migrations = self.repo.all_migrations()

        #assert
        self.assertEqual(len(all_migrations), 1)
        self.assertEqual(all_migrations[0].applied, True)

        #cleanup
        MigrationModel.drop_table()

if __name__ == '__main__':
    unittest.main()
