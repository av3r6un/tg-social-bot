from bot.config import Settings
from pytube import YouTube
import ffmpeg
import os
import re

class YtMusic:
  proxies = {
    'http': 'voidspace:EQuM2VZT@77.238.252.86:44200'
  }
  def __init__(self, logger) -> None:
    self.logger = logger
    self.settings = self._import_settings()
    self.latest = None
    self.abr = None
    self.yt = None

  @classmethod
  def video_info(cls, link) -> tuple[str, str]:
    yt = YouTube(link)
    return yt.video_id, yt.title, cls.choose_type(link)
  
  @staticmethod
  def choose_type(link) -> str:
    pattern = r'(https?://)?(www\.)?(youtube\.com/shorts/)[\w-]+'
    return 'shorts' if re.match(pattern, link) else 'video'

  @property
  def info(self) -> dict:
    return {'origin': self.origin, 'filename': self.filename}

  def download(self, type, link) -> str:
    self.yt = YouTube(link, proxies=self.proxies)
    self.title = self.yt.title
    self.origin = self.yt.video_id
    author = self.yt.author
    file, ext = self._download_shorts() if type == 'shorts' else self._download_song()
    print(file.url)
    self.filename = f'{self._allowed_filename(author)}-{self._allowed_filename(file.title)}'
    if not self._is_worth_downloading():
      raise ValueError('Filesize is too large')
    return file.url if type == 'shorts' else self._convert()
    # file.download(output_path=f'{self.settings.STORAGE}', filename=f'{self.filename}{ext}')
    # self.logger.info(f'Downloaded {self.filename} with abr/resolution: {self.abr if type == 'shorts' else file.resolution}')
    # return self._convert()

  def delete_latest(self) -> None:
    return os.remove(self.latest)
  
  def _download_shorts(self):
    shorts = self.yt.streams.filter(only_video=True).first()
    print(shorts.resolution, shorts)
    return shorts, '.mp4'
  
  def _download_song(self):
    highest_abr = self._get_highest_abr()
    song = self.yt.streams.filter(only_audio=True, abr=highest_abr).first()
    return song, '.wav'

  def _get_highest_abr(self) -> str:
    br = [b.abr for b in self.yt.streams.filter(only_audio=True)]
    i = max([i for i, br in enumerate(br)])
    self._abr = int(br[i].replace('kpbs', ''))
    return br[i]

  def _allowed_filename(self, title) -> bool:
    repl = {' ': '_'} | {k: '' for k in self.settings.BANNED_CHARS}
    return ''.join(repl.get(c, c) for c in title).strip('_')

  def _is_worth_downloading(self) -> bool:
    fs = ((self._abr * self.yt.length) / 8) / 10**6
    if fs < 50:
      return True
    return False

  def _convert(self) -> str:
    self.latest = f'{self.settings.STORAGE}/{self.filename}.mp3'
    try:
      proc = (
        ffmpeg
        .input(f'{self.settings.STORAGE}/{self.filename}.wav')
        .output(f'{self.settings.STORAGE}/{self.filename}.mp3', **{'c:a': 'libmp3lame'})
        .overwrite_output()
        .global_args('-loglevel', 'quiet')
        .run_async(pipe_stdout=True)
      )
      proc.wait()
      self.logger.info(f'Successfully converted {self.filename} into MP3 format.')
      return f'{self.settings.STORAGE}/{self.filename}.mp3'
    except Exception as ex:
      self.logger.error(f'Conversion into MP3 format failed. Traceback: {str(ex)}')
    finally:
      os.remove(f'{self.settings.STORAGE}/{self.filename}.wav')

  def _import_settings(self) -> Settings:
    from bot import s
    return s



