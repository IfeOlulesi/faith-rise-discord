from typing import Literal

def emit_log(type: Literal["good", "info", "warn", "err"], log_text):
  # Types: Info, Warning, Error
  types_dict = {
    'good': '✅ SUCCESS: ',
    "info": '🗒️ INFO: ',
    "warn": '⚠️ WARNING: ',
    "err": '❌ ERROR: '
  }
  
  print(f"{types_dict[type]} {log_text}")