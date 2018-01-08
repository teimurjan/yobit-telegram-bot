from peewee import Model, CharField, SqliteDatabase, BooleanField, IntegerField, ForeignKeyField, FloatField
from playhouse.hybrid import hybrid_property

db = SqliteDatabase('yobit_bot.db')


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
