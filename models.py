from peewee import Model, CharField, MySQLDatabase

from constants import DB_NAME, DB_USER, DB_PASS

db = MySQLDatabase(DB_NAME, user=DB_USER, password=DB_PASS)


class Chat(Model):
  chat_id = CharField(null=False)

  class Meta:
    database = db
