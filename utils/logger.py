import time
import datetime
log_path = "logs/info-log.txt"
error_path = "logs/error-log.txt"
def info(text:str, *, nolog=False):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'[{current_time}/INFO] {text}')
    if nolog == True:
      pass
    else:
      with open(log_path, 'a') as f:
          f.write(f'[{current_time}/INFO] {text}\n')
          f.close()
def warn(text:str, *, nolog=False):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'[{current_time}/WARN] {text}')
    if nolog == True:
      pass
    else:
      with open(log_path, 'a') as f:
          f.write(f'[{current_time}/WARN] {text}\n')
          f.close()
def error(text:str, *, nolog=False):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'[{current_time}/ERROR] {text}')
    if nolog == True:
      pass
    else:
      with open(error_path, 'a') as f:
          f.write(f'[{current_time}/ERROR] {text}\n')
          f.close()
