from typing import List
import yaml

class Photo:
  file_id: str = None
  origin: str = None
  width: int = None
  height: int = None
  mime_type: str = None

  def __init__(self, file_id, origin, width: int = None, height: int = None,
               mime_type: str = None) -> None:
    self.file_id = file_id
    self.origin = origin
    self.width = width
    self.height = height
    self.mime_type = mime_type

  @property
  def json(self):
    return dict(file_id=self.file_id, origin=self.origin, width=self.width,
                height=self.height, mime_type=self.mime_type)
  
  def __str__(self) -> str:
    return f'<Photo from #{self.origin}>'
  
  def __repr__(self) -> str:
    return self.file_id
  

class Photos(List[Photo]):
  def __init__(self, *args) -> None:
    if args:
      for arg in args:
        self.append(Photo(**arg))
  
  def __getitem__(self, value) -> Photo:
    for item in self:
      if item.file_id == value or item.origin == value:
        return item
  
  def add(self, photo_info) -> None:
    self.append(Photo(**photo_info))

  @property
  def json(self) -> dict:
    return [a.json for a in self]

class Video:
  file_id: str = None
  origin: str = None
  width: int = None
  height: int = None
  duration: int = None
  mime_type: str = None

  def __init__(self, file_id, origin, width: int = None, height: int = None,
               duration: int = None, mime_type: str = None, **kwargs) -> None:
    self.file_id = file_id
    self.origin = origin
    self.width = width
    self.height = height
    self.duration = duration
    self.mime_type = mime_type

  @property
  def full_link(self):
    return f'https://instagram.com/reel/{self.origin}/'
  
  @property
  def json(self):
    return dict(file_id=self.file_id, origin=self.origin, width=self.width,
                height=self.height, duration=self.duration, mime_type=self.mime_type)

  def __str__(self) -> str:
    return f'<Video from #{self.origin}>'
  
  def __repr__(self) -> str:
    return self.file_id


class Videos(List[Video]):
  def __init__(self, *args) -> None:
    if args:
      for arg in args:
        self.append(Video(**arg))
  
  def __getitem__(self, value) -> Video:
    for item in self:
      if item.file_id == value or item.origin == value:
        return item
  
  def add(self, video_info) -> None:
    self.append(Video(**video_info))
      
  @property
  def json(self):
    return [a.json for a in self]
  

class Storage:
  videos: Videos = []
  photos: Photos = []

  def __init__(self, filepath) -> None:
    self.filepath = filepath
    videos, photos = self._load_static(filepath)
    self.videos = Videos(*videos)
    self.photos = Photos(*photos)

  def __getitem__(self, value):
    temp_dir = self.videos + self.photos
    for obj in temp_dir:
      if obj.file_id == value or obj.origin == value:
        return obj

  def search(self, value):
    mimetype = None
    local_file = None
    
    for video in self.videos:
      if video.origin == value:
         mimetype = 'video'
         local_file = video
         break
    
    for photo in self.photos:
      if photo.origin == value:
        mimetype = 'photo'
        local_file = photo
        break
    
    return mimetype, local_file

  @staticmethod
  def _load_static(fp) -> tuple[dict, dict]:
    with open(fp, 'r', encoding='utf-8') as file:
      data = yaml.safe_load(file)
    return (data.get('videos'), data.get('photos')) if data else ([], [])

  def dump(self) -> None:
    result = {
      'videos': self.videos.json,
      'photos': self.photos.json
    }
    with open(self.filepath, 'w', encoding='utf-8') as file:
      yaml.safe_dump(result, file, indent=2)

  @property
  def json(self):
    return dict(videos=self.videos.json, photos=self.photos.json)
  
  def add(self, mime_type, info) -> None:
    getattr(self, f'{mime_type}s').add(info)
    self.dump()


