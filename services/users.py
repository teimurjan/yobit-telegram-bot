from models import User
from messages import NO_LOGIN_SENT, USER_ALREADY_EXISTS, USER_NOT_EXISTS, ADD_SUCCESS, DELETE_SUCCESS


def show() -> str:
  users = [str(user) for user in User.select()]
  return '\n'.join(users)


def add(login) -> str:
  if not login or login == '':
    return NO_LOGIN_SENT
  user, created = User.get_or_create(login=login)
  if not created:
    return USER_ALREADY_EXISTS
  else:
    return ADD_SUCCESS


def delete(login) -> str:
  found_user = User.select().where(User.login == login)
  if not found_user.exists():
    return USER_NOT_EXISTS
  User.delete().where(User.login == login).execute()
  return DELETE_SUCCESS
