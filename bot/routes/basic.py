from aiogram.filters import Command
from aiogram.types import Message
from urllib.parse import urlparse
from aiogram import Router, F
main = Router()


@main.message(Command('start'))
async def say_hi(m: Message):
  await m.answer(f'Привет, {m.from_user.first_name}! Отправь мне ссылку, взамен получишь фото/видео.')

