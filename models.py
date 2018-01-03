from peewee import Model, CharField, SqliteDatabase, BooleanField, IntegerField, ForeignKeyField, FloatField
from playhouse.hybrid import hybrid_property

from settings import CURRENCY_VOLUME_KEY, CURRENCY_LAST_PRICE_KEY
from utils import get_currency_name_from_pair

db = SqliteDatabase('yobit_bot.db')


class User(Model):
  login = CharField(null=False)
  name = CharField(null=True, default='')
  chat_id = CharField(null=True)
  t_id = IntegerField(unique=True, null=True)
  is_admin = BooleanField(default=False)
  volume_raise_bound = FloatField(default=1)
  max_allowed_volume = IntegerField(null=True)

  @hybrid_property
  def is_active(self):
    return self.chat_id is not None and self.t_id is not None

  def should_receive_notification(self, currency_name, currency_info, prev_volume):
    if not prev_volume:
      return False
    current_volume = currency_info[CURRENCY_VOLUME_KEY]
    ignored_currencies = self.get().ignored_currencies.select()
    is_ignored_currency = ignored_currencies.where(IgnoredCurrency.value == currency_name).exists()
    is_volume_raised = self.volume_raise_bound < current_volume - prev_volume
    volume_allowed = self.max_allowed_volume is not None and current_volume < self.max_allowed_volume
    return not is_ignored_currency and volume_allowed and is_volume_raised

  def __str__(self):
    return 'Name: {}, Login: {}, {}'.format(self.name, self.login, 'ACTIVE' if self.is_active else 'NOT_ACTIVE')

  @hybrid_property
  def about(self):
    return 'Login: {}, Volume raised bound: {}, Max allowed volume: {}.'.format(self.login, self.volume_raise_bound,
                                                                                self.max_allowed_volume)

  class Meta:
    database = db


class IgnoredCurrency(Model):
  value = CharField(null=False)
  user = ForeignKeyField(rel_model=User, related_name='ignored_currencies')

  class Meta:
    database = db
