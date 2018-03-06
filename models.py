from peewee import Model, CharField, BooleanField, IntegerField, ForeignKeyField, FloatField, \
    PostgresqlDatabase
from playhouse.hybrid import hybrid_property
from settings import DATABASE_URL
from utils import parse_database_url

database_info = parse_database_url(DATABASE_URL)
db = PostgresqlDatabase(database=database_info['db_name'],
                        user=database_info['user'],
                        password=database_info['password'],
                        host=database_info['host'],
                        port=database_info['port'])


class User(Model):
    login = CharField(null=False)
    name = CharField(null=True, default='')
    chat_id = CharField(null=True)
    telegram_user_id = IntegerField(unique=True, null=True)
    is_admin = BooleanField(default=False)
    volume_raise_limit = FloatField(default=1)
    max_allowed_volume = IntegerField(null=True)

    @hybrid_property
    def is_active(self):
        return self.chat_id is not None and self.telegram_user_id is not None

    def __str__(self):
        return 'Name: {}, Login: {}, {}'.format(self.name, self.login, 'ACTIVE' if self.is_active else 'NOT_ACTIVE')

    @hybrid_property
    def about(self):
        return 'Login: {}, Volume raised limit: {}, Max allowed volume: {}.'.format(self.login, self.volume_raise_limit,
                                                                                    self.max_allowed_volume)

    class Meta:
        database = db


class IgnoredCurrency(Model):
    value = CharField(null=False)
    user = ForeignKeyField(rel_model=User, related_name='ignored_currencies')

    class Meta:
        database = db
