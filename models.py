from peewee import Model, CharField, SqliteDatabase, BooleanField
from playhouse.hybrid import hybrid_property

db = SqliteDatabase('yobit_bot.db')


class User(Model):
  login = CharField(null=False)
  name = CharField(null=True, default='')
  chat_id = CharField(null=True)
  telegram_user_id = CharField(null=True)
  is_admin = BooleanField(default=False)

  @hybrid_property
  def is_active(self):
    return self.chat_id is not None and self.telegram_user_id is not None

  def __str__(self):
    return 'Name: {}, Login: {}, {}'.format(self.name, self.login, 'ACTIVE' if self.is_active else 'NOT_ACTIVE')

  class Meta:
    database = db
