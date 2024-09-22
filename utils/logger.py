from typing import Literal

def emit_log(type: Literal["info", "warn", "err"], log_text):
  # Types: Info, Warning, Error
  types_dict = {
    "info": '🗒️ INFO: ',
    "warn": '⚠️ WARNING: ',
    "err": '❌ ERROR: '
  }
  
  print(f"{types_dict[type]} {log_text}")