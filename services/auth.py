from settings import ADMIN_PASSWORD
from models import User
from messages import REGISTRATION_SUCCESS_MSG, ALREADY_REGISTERED_MSG, \
  ADMIN_EXISTS, BECOME_ADMIN_SUCCESS, \
  LOG_IN_NOT_ALLOWED, NO_LOGIN, NOT_FOUND


def register(update, by='phone') -> str:
  login = update.message.contact.phone_number if by == 'phone' else update.message.from_user.username
  if not login:
    return NO_LOGIN
  chat_id = update.message.chat_id
  user_id = update.message.from_user.id
  name = update.message.from_user.name
  try:
    user_with_login = User.select().where(User.login == login).get()
    user_with_same_id_exists = User.select().where(telegram_user_id=user_id).exists()
    if user_with_login.is_active or user_with_same_id_exists:
      return ALREADY_REGISTERED_MSG
    else:
      User.update(chat_id=chat_id, telegram_user_id=user_id, name=name).where(User.login == login).execute()
      return REGISTRATION_SUCCESS_MSG
  except User.DoesNotExist:
    return LOG_IN_NOT_ALLOWED


def become_admin(update) -> str:
  try:
    user_id = update.message.from_user.id
    password = update.message.text.split(' ')[1]
    if password != ADMIN_PASSWORD:
      return NOT_FOUND
    user, created = User.get_or_create(login='admin{}'.format(user_id), telegram_user_id=user_id, name=update.message.from_user.name,
                                       chat_id=update.message.chat_id, is_admin=True)
    if not created:
      return ADMIN_EXISTS
    return BECOME_ADMIN_SUCCESS
  except(User.DoesNotExist, IndexError):
    return NOT_FOUND
