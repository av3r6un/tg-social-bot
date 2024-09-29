from aiogram.types import ChatPhoto, Video

class StorageInfo:
  tg_object: ChatPhoto | Video = None
  mime_type: str = None
  origin: str = None

  def __init__(self, tg_object, mime_type, origin) -> None:
    self.mime_type = mime_type
    self.tg_object = tg_object
    self.origin = origin

  @property
  def json(self) -> dict:
    file_info = getattr(self.tg_object, self.mime_type)
    info = dict(file_id=file_info.file_id, width=file_info.width, height=file_info.height,
                origin=self.origin, mime_type=file_info.mime_type)
    info.update(
      dict(duration=file_info.duration)
      if self.mime_type == 'video' else {}
    )
    return info 
