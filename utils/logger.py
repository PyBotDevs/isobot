# Imports
import time
import datetime

log_path = "logs/info-log.txt"
error_path = "logs/error-log.txt"
class colours:
    error = '\033[91m'
    success = '\033[92m'
    warning = '\033[33m'
    end = '\033[0m'

# Main Functions
def info(text:str, *, nolog=False, module=None, timestamp=False):
    """Logs a client information alert to the console and the log file.\n`nolog=True` option skips logging to file."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if module is not None:
        if not timestamp: print(f'[{module}] {text}')
        else: print(f'[{current_time}] [{module}] {text}')
    else:
        if not timestamp: print(text)
        else: print(f'[{current_time}] {text}')
    if nolog == True: pass
    else:
      with open(log_path, 'a') as f:
          f.write(f'[{current_time}/INFO] {text}\n')
          f.close()
def warn(text:str, *, nolog=False):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'[{current_time}/WARN] {text}')
    if nolog == True: pass
    else:
      with open(log_path, 'a') as f:
          f.write(f'[{current_time}/WARN] {text}\n')
          f.close()
def error(text:str, *, nolog=False):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'{colours.error}[{current_time}/ERROR] {text}{colours.end}')
    if nolog == True: pass
    else:
      with open(error_path, 'a') as f:
          f.write(f'[{current_time}/ERROR] {text}\n')
          f.close()
