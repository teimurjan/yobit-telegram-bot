from telegram.ext import Updater, CommandHandler

from models import Chat

START_COMMAND = 'start'
REGISTRATION_SUCCESS_MSG = 'Registration completed successfully!'
ALREADY_REGISTERED_MSG = 'You have already registered'


class YobitBot(object):
  def __init__(self, token):
    self.token = token

  def start(self):
    self.updater_ = Updater(token=self.token)
    self._init_commands_handlers()
    self.updater_.start_polling()

  def _init_commands_handlers(self):
    dispatcher = self.updater_.dispatcher
    start_handler = CommandHandler(START_COMMAND, self._handle_start_command)
    dispatcher.add_handler(start_handler)

  def _handle_start_command(self, bot, update):
    chat_id = update.message.chat_id
    chat, created = Chat.get_or_create(chat_id=chat_id)
    if created:
      bot.send_message(chat_id=chat_id, text=REGISTRATION_SUCCESS_MSG)
    else:
      bot.send_message(chat_id=chat_id, text=ALREADY_REGISTERED_MSG)

  def send_msg(self, msg):
    bot = self.updater_.dispatcher.bot
    for chat in Chat.select():
      bot.send_message(chat.chat_id, text=msg)
