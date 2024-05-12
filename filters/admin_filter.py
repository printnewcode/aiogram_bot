from aiogram import types
from aiogram.filters import Filter

from services.settings import ADMIN_LIST


class AdminFilter(Filter):
    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def __call__(self, message: types.Message) -> bool:
        if str(message.from_user.id) in ADMIN_LIST:
            return True
        else:
            return False
