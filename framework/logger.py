import time, datetime, os
from isobot.colors import Colors

class Logger(Colors):
    """The library used for logging information.
    
    Valid commands:
    - info(text)
    - warn(text)
    - error(text)"""
    def __init__(self, log_path:str, error_path:str):
        self.log_path = log_path
        self.error_path = error_path
        print(f"[Framework/Loader] {Colors.green}Logger initialized.{Colors.end}")
    def info(self, text:str, *, nolog=False):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f'[{current_time}/INFO] {text}')
        if nolog == True: pass
        else:
            with open(self.log_path, 'a') as f:
                f.write(f'[{current_time}/INFO] {text}\n')
                f.close()
    def warn(self, text:str, *, nolog=False):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f'[{current_time}/WARN] {text}')
        if nolog == True: pass
        else:
            with open(self.log_path, 'a') as f:
                f.write(f'[{current_time}/WARN] {text}\n')
                f.close()
    def error(self, text:str, *, nolog=False):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f'{Colours.red}[{current_time}/ERROR] {text}{Colours.end}')
        if nolog == True: pass
        else:
            with open(self.error_path, 'a') as f:
                f.write(f'[{current_time}/ERROR] {text}\n')
                f.close()
