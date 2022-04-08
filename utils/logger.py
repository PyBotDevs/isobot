import time
import datetime
log_path = "./Desktop/Stock/logs/info-log.txt"
error_path = "./Desktop/Stock/logs/info-log.txt"
def info(text:str):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    with open(log_path, 'a') as f:
        f.write(f'[{current_time}/INFO] {text}.\n')
        f.close()
def warn(text:str):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    with open(log_path, 'a') as f:
        f.write(f'[{current_time}/WARN] {text}.\n')
        f.close()
def error(text:str):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    with open(error_path, 'a') as f:
        f.write(f'[{current_time}/ERROR] {text}.\n')
        f.close()
