from dotenv import load_dotenv
import yaml
import sys
import os

load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env'))


class Settings:
  ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../..')

  def __init__(self) -> None:
    self.STORAGE = os.path.join(self.ROOT, 'storage.yaml')
    self.__init_settings()

  def __init_settings(self) -> None:
    self._sensitive_info()

    fp = os.path.join(self.ROOT, 'bot', 'config', 'settings.yaml')
    try:
      with open(fp, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
      self.__dict__.update(data)
    except FileNotFoundError:
      print('Config file not found! Exiting..')
      sys.exit(-1)
  
  def _sensitive_info(self):
    info = {
      'TOKEN': os.getenv('TOKEN'),
      "RAPID_API": os.getenv('RAPID_API'),
      "RAPID_HOST": os.getenv('RAPID_HOST'),
      "RAPID_INDEX": os.getenv('RAPID_INDEX'),
    }
    self.__dict__.update(info)
