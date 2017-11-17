from peewee import CharField, DateField, BooleanField, Model


class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        db_table = 'sample_person_table'
