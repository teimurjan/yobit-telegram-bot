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

  def should_receive_msg(self, msg):
    prev_volume, currency_name, current_volume = \
      msg.get_prev_volume(), msg.get_currency_name(), msg.get_current_volume()
    if not prev_volume:
      return False
    ignored_currencies = self.get().ignored_currencies.select()
    is_ignored_currency = ignored_currencies.where(IgnoredCurrency.value == currency_name).exists()
    is_volume_raised = self.volume_raise_limit < current_volume - prev_volume
    volume_allowed = self.max_allowed_volume is not None and current_volume < self.max_allowed_volume
    return not is_ignored_currency and volume_allowed and is_volume_raised

  def __str__(self):
    return 'Name: {}, Login: {}, {}'.format(self.name, self.login, 'ACTIVE' if self.is_active else 'NOT_ACTIVE')

  @hybrid_property
  def about(self):
    return 'Login: {}, Volume raised bound: {}, Max allowed volume: {}.'.format(self.login, self.volume_raise_limit,
                                                                                self.max_allowed_volume)

  class Meta:
    database = db


class IgnoredCurrency(Model):
  value = CharField(null=False)
  user = ForeignKeyField(rel_model=User, related_name='ignored_currencies')

  class Meta:
    database = db
