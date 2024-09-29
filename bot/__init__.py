from aiogram import Dispatcher, Bot
from .config import Settings
from .routes import routers
from .modules import Logger, Storage


s = Settings()
logger = Logger(log_fmt=s.LOG_FMT, date_fmt=s.DATE_FMT)
storage = Storage(s.STORAGE)

def main():
  dp = Dispatcher()
  dp.include_routers(*routers)
  bot = Bot(s.TOKEN)

  import asyncio
  asyncio.run(dp.start_polling(bot))
