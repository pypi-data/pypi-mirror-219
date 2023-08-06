from .protector import Protector
from dotenv import load_dotenv
import os

""" Settings """
api_key = None
default_client = None
load_dotenv()

if "ZETANE_API_KEY" in os.environ:
    api_key = os.getenv("ZETANE_API_KEY")

def config(*args, **kwargs):
  return _proxy('config', *args, **kwargs)

def upload_dataset(*args, **kwargs):
  return _proxy('upload_dataset', *args, **kwargs)

def upload_model(*args, **kwargs):
  return _proxy('upload_model', *args, **kwargs)

def get_entries(*args, **kwargs):
  return _proxy('get_entries', *args, **kwargs)

def get_orgs_and_projects(*args, **kwargs):
  return _proxy('get_orgs_and_projects', *args, **kwargs)

def report(*args, **kwargs):
  return _proxy('report', *args, **kwargs)

def get_report_status(*args, **kwargs):
  return _proxy('get_report_status', *args, **kwargs)

def create_project(*args, **kwargs):
  return _proxy('create_project', *args, **kwargs)

def delete_project(*args, **kwargs):
  return _proxy('delete_project', *args, **kwargs)

def _proxy(method, *args, **kwargs):
    """Create an analytics client if one doesn't exist and send to it."""
    global default_client
    if not default_client:
      if api_key is not None:
        default_client = Protector(api_key)

      elif 'api_key' in kwargs:
        default_client = Protector(kwargs['api_key'])

      elif len(args) > 0:
        default_client = Protector(args[0])

      else:
         print("** Please set your api key with zetane.config(api_key=\"your_api_key\") before calling other methods. **\n")

         raise TypeError('Failed to authenticate API key, no API key provided.')

    fn = getattr(default_client, method)
    return fn(*args, **kwargs)
