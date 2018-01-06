import json

from telegram.ext import Updater, CallbackQueryHandler

from bot.handlers.auth import log_in_handler, become_admin_handler
from bot.handlers.ignore_currency import add_ignore_currency_handler, show_ignore_currencies_handler, \
  delete_ignore_currency_handler
from bot.handlers.user import add_user_handler, show_yourself_handler, set_user_max_volume_handler, \
  set_user_raise_limit_handler, show_users_handler, delete_user_handler
from bot.utils import DELETE_CURRENCY_ACTION_KEY, DELETE_USER_ACTION_KEY
from models import User


class YobitBot(object):
  def __init__(self, token, logger):
    self.token = token
    self.inline_callback_router = {
      DELETE_CURRENCY_ACTION_KEY: delete_ignore_currency_handler,
      DELETE_USER_ACTION_KEY: delete_user_handler
    }
    self.logger = logger
    self.updater = None

  def start(self) -> None:
    self.updater = Updater(token=self.token)
    self._init_handlers()
    self.updater.start_polling(poll_interval=2)

  def _init_handlers(self) -> None:
    dispatcher = self.updater.dispatcher
    inline_btn_handler = CallbackQueryHandler(self.inline_btn_callback)
    dispatcher.add_handler(add_user_handler)
    dispatcher.add_handler(add_ignore_currency_handler)
    dispatcher.add_handler(log_in_handler)
    dispatcher.add_handler(show_yourself_handler)
    dispatcher.add_handler(set_user_max_volume_handler)
    dispatcher.add_handler(set_user_raise_limit_handler)
    dispatcher.add_handler(become_admin_handler)
    dispatcher.add_handler(show_users_handler)
    dispatcher.add_handler(show_ignore_currencies_handler)
    dispatcher.add_handler(inline_btn_handler)
    dispatcher.add_error_handler(self._handle_error)

  def _handle_error(self, bot, update, error):
    self.logger.error(str(error))

  def inline_btn_callback(self, bot, update) -> None:
    data = json.loads(update.callback_query.data)
    action_name, action_kwargs = data.popitem()
    if action_name is not None:
      handler = self.inline_callback_router[action_name]
      handler(bot, update, **action_kwargs)

  def dispatch_message(self, msg) -> None:
    bot = self.updater.dispatcher.bot
    for user in User.select().where(User.is_active == True):
      try:
        prev_volume, currency_name, current_volume = \
          msg.get_prev_volume(), msg.get_currency_name(), msg.get_current_volume()
        is_volume_raised = user.volume_raise_limit < current_volume - prev_volume
        is_volume_allowed = user.max_allowed_volume is None or current_volume < user.max_allowed_volume
        if not user.is_ignore_currency(currency_name):
          if is_volume_allowed and is_volume_raised:
            bot.send_message(user.chat_id, text=str(msg))
            self.logger.info(msg)
        else:
          self.logger.info('User {} ignored {}'.format(user, currency_name))
      except Exception as e:
        self.logger.error('{}. Couldn\'t send msg to user {}'.format(str(e), str(user)))
