from aiogram import types
from aiogram.filters import Filter

from services.settings import ADMIN_LIST


class AdminFilter(Filter):
    key = "is_admin"

    def __init__(self, is_admin: bool) -> None:
        self.is_admin = is_admin

    async def __call__(self, message: types.Message) -> bool:
        if (message.from_user.id in ADMIN_LIST) is self.is_admin:
            return True
        else:
            return False
