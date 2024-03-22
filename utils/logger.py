# Imports
import time
import datetime

# Variables and Classes
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
          if module is not None: f.write(f'[{current_time}] [{module}] {text}\n')
          else: f.write(f'[{current_time}] {text}\n')
          f.close()

def warn(text:str, *, nolog=False, module=None):
    """Logs a client warning to the console and the log file.\n`nolog=True` option skips logging to file."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if module is not None: print(f'{colours.warning}[{module}] WARN: {text}{colours.end}')
    else: print(f'{colours.warning}WARN: {text}{colours.end}')
    if nolog == True: pass
    else:
      with open(log_path, 'a') as f:
          if module is not None: f.write(f'[{current_time}] [{module}] WARN: {text}\n')
          else: f.write(f'[{current_time}] WARN: {text}\n')
          f.close()

def error(text:str, *, nolog=False, module=None):
    """Logs an error to the console and the errors log file.\n`nolog=True` option skips logging to file."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if module is not None: print(f'{colours.error}[{module}] ERROR: {text}{colours.end}')
    else: print(f'{colours.error}ERROR: {text}{colours.end}')
    if nolog == True: pass
    else:
      with open(error_path, 'a') as f:
          if module is not None: f.write(f'[{current_time}] [{module}] ERROR: {text}\n')
          else: f.write(f'[{current_time}] ERROR: {text}\n')
          f.close()

# Startup Log Class
class StartupLog():
    def __init__(self, log_path: str, *, add_timestamps: bool = False, clear_old_logs: True):
        """Used to log the isobot client's startup logs."""
        self.log_path = log_path
        self.add_timestamps = add_timestamps
        if clear_old_logs:
            with open(log_path, 'w+', encoding="utf-8") as f:
                f.write("# Startup log will be shown here!\n")
                f.close()

    def clean(self, data: str):
        """Cleans out any extra metadata (like colour codes) from the data."""
        color_codes = ['\033[91m', '\033[92m', '\033[93m', '\033[33m', '\033[0m']
        data_d = data  # Specify new isolated variable for performing string operations on
        for x in color_codes:
            if x in data_d:
                data_d = data_d.replace(x, "")
        return data_d

    def log(self, data: str, *, print_log: bool = True):
        """Writes a log to the specified log file."""
        if print_log: print(data)
        data = self.clean(data)
        with open(self.log_path, 'a', encoding="utf-8") as f:
            if self.add_timestamps:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                f.write(f"[{current_time}] {data}\n")
            else: f.write(f"{data}\n")
            f.close()
