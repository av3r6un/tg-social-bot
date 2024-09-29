from bot.wrappers import StorageInfo
from aiogram.filters import Filter
from bot.modules import InstaSaver
from urllib.parse import urlparse
from aiogram.types import Message
from aiogram import Router
import asyncio


class IgFilter(Filter):
  DOMAINS = ['www.instagram.com', 'instagram.com']

  async def __call__(self, message) -> bool:
    return urlparse(message.text).netloc in self.DOMAINS


insta_route = Router()


@insta_route.message(IgFilter())
async def insta_handler(m: Message) -> None:
  from bot import s, logger, storage
  insta = InstaSaver(s.RAPID_INDEX, s.RAPID_HOST, s.RAPID_API, logger)
  shortcode, full_link = InstaSaver.shortcode(m.text)
  mime_type, local_file = storage.search(shortcode)
  if local_file:
    await m.chat.do(f'upload_{mime_type}')
    await asyncio.sleep(2)
    await getattr(m, f'answer_{mime_type}')(**{mime_type: local_file.file_id})
  else:
    try:
      await m.chat.do('record_video')
      data = insta.get_media(full_link)
      mime_type = data['type']
      info_message = await m.answer(f'Загрузка {data["type_text"].lower()}:')
      if info_message: await info_message.delete()
      stored_message = await getattr(m, f'answer_{mime_type}')(data['direct_url'])
      info = StorageInfo(stored_message, mime_type, shortcode)
      storage.add(mime_type, info.json)
    except ValueError:
      await m.answer('Ошибка подключения к серверу.')
    except IndexError as err:
      logger.error(str(err))
  


