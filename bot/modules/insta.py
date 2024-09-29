from requests import Request, Session
from .logger import Logger
import json


class InstaSaver:
  logger: Logger = None
  def __init__(self, index, host, api, logger = None):
    self.logger = logger
    self.request = Request(
      'GET', index,
      {
        "X-RapidAPI-Key": api,
        "X-RapidAPI-Host": host
      }
    )
    self.session = Session()
    self.shortcode = None

  @staticmethod
  def _get_shortcode(url):
    return url.split('/')[-2]
  
  @classmethod
  def shortcode(cls, url):
    return cls._get_shortcode(url), url

  def _parse_response(self, resp) -> dict:
    try:
      resp = json.loads(resp.text)
      if not resp:
        raise IndexError('Cannot receive data from API')
    except json.JSONDecodeError as ex:
      if self.logger: self.logger.error(str(ex))
    response = dict()
    if not 'Type' in resp:
      print(resp)
      raise ValueError("Can't parse given url")
    if resp['Type'] in ['Post-Image', 'Image']:
      response['type'] = 'image'
      response['type_text'] = 'Изображение'
    if resp['Type'] == 'Post-Video':
      response['type'] = 'video'
      response['type_text'] = 'Видео'
    response['direct_url'] = resp['media']
    return response
  
  def _get_video_info(self, url) -> dict:
    req_params = {"url": url}
    self.shortcode = self._get_shortcode(url)
    self.request.params = req_params
    prepared_request = self.request.prepare()
    return self._parse_response(self.session.send(prepared_request))

  def get_media(self, url) -> dict:
    return self._get_video_info(url)
