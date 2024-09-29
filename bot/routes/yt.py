from bot.wrappers import StorageInfo
from aiogram.filters import Filter
from bot.modules import YtMusic
from urllib.parse import urlparse
from aiogram.types import Message
from aiogram import Router
import asyncio


class YtFilter(Filter):
  DOMAINS = ['www.youtube.com', 'youtu.be', 'youtube.com']

  async def __call__(self, message: Message) -> bool:
    return urlparse(message.text).netloc in self.DOMAINS


yt_route = Router()


@yt_route.message(YtFilter())
async def yt_handler(m: Message) -> None:
  from bot import logger, storage
  yt = YtMusic(logger)
  uid, title, mimetype = YtMusic.video_info(m.text)
  # mimetype, local_file = storage.search(uid)
  url = yt.download(mimetype, m.text)
  m.answer_video(video=url)

  

