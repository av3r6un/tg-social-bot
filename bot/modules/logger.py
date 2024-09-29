from datetime import datetime as dt
import os


class Logger:
  def __init__(self, filename=None, date_fmt=None, log_fmt=None) -> None:
    self.filename = filename if filename else os.getenv('LOG_FILENAME')
    self.date_fmt = date_fmt if date_fmt else os.getenv('DATE_FMT')
    self.log_fmt = log_fmt if log_fmt else os.getenv('LOG_FMT')
    self.separated = False
  
  def error(self, message) -> None:
    self._make_log('error', message)

  def info(self, message) -> None:
    self._make_log('info', message)

  def _separate(self) -> None:
    if not self.separated:
      message = f'{"="*25}\t[Started {dt.now().strftime(self.date_fmt)}]\t{"="*25}\n'
      with open(self.filename, 'a', encoding='utf-8') as file:
        file.write(message)
      self.separated = True
  
  def _make_log(self, level, message) -> None:
    self._separate()
    time = dt.now().strftime(self.date_fmt)
    msg = self.log_fmt.format(time=time, level=level.upper(), message=message) + '\n'
    with open(self.filename, 'a', encoding='utf-8') as file:
      file.write(msg)
  
  def action(self, user_id, action) -> None:
    msg = f'User {user_id} performed {action}'
    self.info(msg)
    