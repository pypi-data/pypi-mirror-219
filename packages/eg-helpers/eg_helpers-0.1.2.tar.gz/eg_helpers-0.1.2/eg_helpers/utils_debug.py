#File: utils_debug.py
# Description: Utility functions for custom debugging and logging purposes.

"""
Function: dprint(msg, level=2, *args)
Description: Prints debug messages with different levels of verbosity.
Parameters: msg (str), level (int), *args

Function: debugging_prints(msg, level, current_debug_level, *args)
Description: Handles the printing of debug messages based on the provided level and current debug level.
Parameters: msg (str), level (int), current_debug_level (int), *args

Debugging Levels:
- Level 0: Deepest Debugging - Intended for critical errors and deep investigation.
- Level 1: Deep Debugging - Provides status updates at a deeper level.
- Level 2: Status Debugging - General status updates during program execution.
- Level 3: Warning Debugging - Highlights warning messages.
- Level 4: Error Debugging - Indicates errors with additional ASCII art.
- Level 5: Critical Error Debugging - Indicates critical errors with more elaborate ASCII art.
- Level 6: Small Success Debugging - Indicates small successes during program execution.
- Level 7: Great Success Debugging - Indicates significant successes during program execution.
- Level 99: Custom Debugging - For custom debugging messages.


Class: UserError(Exception)
Description: Custom exception class for user errors.
Parameters: message (str)

Usage Example:
try:
    # Your code here
    raise UserError("An example user error occurred.")
except UserError as e:
    print(f"UserError: {e}")
"""

import tempfile 
import shutil
import datetime
import os
import re
import pandas as pd
from .utils_debug_ascii_art import get_random_art


### this part is for internal troubleshooting / logging ... absurd, i know.. ###

import logging
import os

# Get the current script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Setup logging
log_file = os.path.join(script_dir, 'utils_debug_error_log.txt')  # This joins the script directory with 'app.log'

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the minimum log level

# Create a file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)  # Set the minimum log level for file output

# Create a stream handler (prints to console)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)  # Set the minimum log level for console output

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the handlers
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

"""
# Now, you can replace your 'print' statements with 'logger.info' or 'logger.debug' or appropriate level
logger.info('This is an info message')
logger.debug('This is a debug message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
"""


log_main = "log_main.txt"
debug_utils_debug = 1
#in case I would need to have dprints in this file I could enable this, but it's fucking confusing ...
current_debug_level = debug_utils_debug
#debug_level = 0

#def dprint(msg, level=2, log_timestamps=True=True, *args):
#    debugging_prints(msg, level, debug_level, log_timestamps=True, *args)



def flow(number):
    """
    Prints a flow marker message to the console to aid in debugging.
    
    This function is especially useful for visual checkpoints when traversing through a large or complex codebase. It prints 
    a standard format message to indicate a stage in the code execution, based on the input number.
    
    Parameters:
    number (int): A numeric identifier to signify a point in the codebase's flow.

    Returns:
    None
    """
    print(f"flow marker: {number}")


log_buffer_debug = False


## Buffering log output to get performance increases 
## and not drive cloud services crazy

import time
import queue
import threading
import collections


## starting point: if you want to use this, you have to initialize a log buffer with these parameters. we can do txt and csv.
# for both cases the script creates directories and files if they don't exist, for CSV you have to pass "headers" as an attribute
# Note that if the headers change for an existing file, this won't do anything. you'd need to delete the file and start a new one.
# you can run several different buffers, all of them will get their own processes. if you don't declare a main log file, the script
# will default to log_main.txt


def initialize_log_buffer(log_file, set_as_main_log_file = False, mode="txt", headers = None, buffer_size=500, flush_interval=60, max_lines=50000):
    """
    Initializes a log buffer for the provided file. If a buffer for the file already exists, it returns the existing buffer. 

    Parameters:
        log_file (str): The name of the log file.
        set_as_main_log_file (bool, optional): If true, sets this file as the main log file. Defaults to False.
        mode (str, optional): The mode for logging. Can be "txt" or "csv". Defaults to "txt".
        headers (List[str], optional): Required if mode is "csv". These are the headers for the csv file. Defaults to None.
        buffer_size (int, optional): The number of entries the buffer can hold before it is flushed. Defaults to 500.
        flush_interval (int, optional): Time in seconds after which the buffer is flushed. Defaults to 60.
        max_lines (int, optional): Maximum number of lines the log file can have. Older entries are removed if limit is exceeded. Defaults to 50000.

    Returns:
        LogBuffer: The instance of LogBuffer for the given filename.
    """
    logger.info(f"Initiliazing log buffer...")
    global log_main
    if set_as_main_log_file:
        log_main = log_file
        logger.info(f"Ok, overwritten log_main to {log_main}")
    
    LogBuffer.getInstance(log_file, mode, headers, buffer_size, flush_interval, max_lines)


class LogBuffer:
    """
    The LogBuffer class manages logging by buffering log messages and flushing them to a file in batches. 
    It supports multiple instances for different files and handles threading for parallel execution. 
    It also ensures that the log file doesn't exceed a maximum line limit.
    """

    _instances = {}

    @staticmethod
    def getInstance(filename, mode="txt", headers=None, buffer_size=500, flush_interval=60, max_lines=50000):
        if filename not in LogBuffer._instances:
            LogBuffer._instances[filename] = LogBuffer(filename, mode, headers, buffer_size, flush_interval, max_lines)

        return LogBuffer._instances[filename]

    def __init__(self, filename, mode, headers, buffer_size, flush_interval, max_lines):
        """
        Initializes the LogBuffer instance and creates worker and timer threads for handling message queue and periodic flushing of the buffer, respectively.
        """
        self.filename = filename
        self.mode = mode
        self.headers = headers
        self.buffer_size = buffer_size
        if mode == "csv":
            self.buffer = pd.DataFrame()
        else:
            self.buffer = []
        self.lock = threading.Lock()
        self.flush_interval = flush_interval
        self.max_lines = max_lines
        self.queue = queue.Queue()

        # Start the worker thread
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

        # Start the timer thread
        self.timer_thread = threading.Thread(target=self._timer, daemon=True)
        self.timer_thread.start()
        
        self.suffix = ".csv" if mode == "csv" else ".txt"
        self.tempfile = tempfile.NamedTemporaryFile(suffix=self.suffix, delete=False).name
        logger.info(f"Temp logfile initialized, path: {self.tempfile}")
        if os.path.exists(self.filename):
            shutil.copy2(self.filename, self.tempfile)

        # Initialize a threading event
        self.copy_event = threading.Event()
        # Start the copy thread
        self.copy_thread = threading.Thread(target=self._safe_file_copy, daemon=True)
        self.copy_thread.start()


    def log(self, message):
        """
        Adds a new log message to the buffer queue for later processing by the worker thread.
        
        Parameters:
        message (str): The log message to be added.
        """
        global log_buffer_debug

        #with self.lock:

        # Put the message into the queue
        self.queue.put(message)

        if log_buffer_debug:
            logger.info(f"Added message to buffer:\n{message}")

    def _worker(self):
        """
        Worker thread method to process messages from the queue and add them to the buffer. 
        If the buffer is full, it calls the flush method to empty it.
        
        Raises:
        Exception: Any error occurred during buffer flushing.
        """
        global log_buffer_debug

        while True:
            # Take a message from the queue
            message = self.queue.get()

            if self.mode == "csv":
                # Convert message to a DataFrame and add to buffer
                new_df = pd.DataFrame([message])
                if self.buffer.empty:  # If buffer is an empty DataFrame
                    self.buffer = new_df
                else:
                    self.buffer = pd.concat([self.buffer, new_df], ignore_index=True)

                if log_buffer_debug:
                    logger.info(f"Appended message to buffer:\n{new_df}")
            else:
                # In txt mode, simply append message to buffer
                self.buffer.append(message)

                if log_buffer_debug:
                    logger.info(f"Appended message to buffer:\n{message}")

            try:
                # If the buffer is full (for txt mode, we check number of lines; for csv mode, number of rows), flush it
                if len(self.buffer) >= self.buffer_size:
                    self.flush()
            except Exception as e:
                logger.error(f"Error while trying to flush debug print buffer for file {self.filename}: {e}")

            # Notify the queue that the message has been processed
            self.queue.task_done()


    def _safe_file_copy(self):
        """Safely copy a file from src to dst. If it fails, it retries up to the given number of times."""
        while True:
            # Wait for the copy event
            self.copy_event.wait()

            retries = 10
            while retries > 0:
                try:
                    shutil.copyfile(self.tempfile, self.filename)
                    logger.info(f"Successfully copied temp file to {self.filename}")
                    break
                except Exception as e:
                    logger.info(f"Failed to copy temp file to {self.filename}. Retries left: {retries-1}. Error: {e}")
                    retries -= 1
                    if retries > 0:
                        time.sleep(5)  # Wait for 1 second before retrying

            # Clear the event
            self.copy_event.clear()

    def flush(self):
        """
        Flushes the buffer to the log file in the defined format (txt or csv). If an error occurs during the process,
        it prints the error message, the contents of the buffer, and then continues.
        """
        global log_buffer_debug

        if self.mode == "txt" and not self.buffer or self.mode == "csv" and self.buffer.empty:
            return


        self.trim_log()

        try:
            if self.mode == "txt":
                with open(self.tempfile, "a", encoding="utf-8") as file:
                    for message in self.buffer:
                        file.write(message)
                        if log_buffer_debug:
                            logger.info(f"Wrote message to file:\n{message}")
                self.buffer = []
            elif self.mode == "csv":
                headers = self.headers
                df_to_write = self.buffer.copy()
                df_to_write.to_csv(self.tempfile, mode='a', index=False, header=False)
                if log_buffer_debug:
                    logger.info(f"Wrote data frame to CSV file:\n{df_to_write}")
                self.buffer = pd.DataFrame(columns=self.buffer.columns)

            # Signal the copy worker to copy the file
            self.copy_event.set()
        except Exception as e:
            logger.error(f"Failed to write buffer to file: {self.tempfile}")
            logger.error(f"Error: {e}")
            logger.info(f"content of buffer: {self.buffer}")
            logger.info(f"Ignoring and continuing...")



    def trim_log(self):
        """
        Trims log file to desired max length.
        """
        #with self.lock:
        if self.mode == "txt":
            try:
                with open(self.filename, 'r+', encoding="utf-8") as f:
                    queue = collections.deque(f, self.max_lines)
                    f.seek(0)
                    f.truncate()
                    f.writelines(queue)
                    logger.info("Trimmed log successfully.")
            except Exception as e:
                logger.error(f"Failed to trim log file: {self.filename}")
                logger.error(f"Error: {e}")
                logger.info(f"Ignoring and continuing...")

    def _timer(self):
        """
        Timer thread method to call the flush method at regular intervals defined by 'flush_interval'. 
        If an error occurs during the process, it prints the error message, the contents of the buffer, and then continues.
        """
        global log_buffer_debug

        while True:
            # Sleep for self.flush_interval seconds
            time.sleep(self.flush_interval)

            # Flush the buffer
            if log_buffer_debug:
                logger.info("Flushing buffer...")
            try:
                self.flush()
            except Exception as e:
                logger.error(f"Failed to flush buffer to log file: {self.filename}\nError: {e}\nContent of buffer:{self.buffer}")



def flush_all_buffers():
    """
    Calls the flush method for all active LogBuffer instances to flush their buffers to their respective log files.

    """
    for buffer in LogBuffer._instances.values():
        buffer.flush()




#in case I would need to have dprints in this file I could enable this, but it's fucking confusing ...
current_debug_level = debug_utils_debug
#debug_level = 0

#def dprint(msg, level=2, log_timestamps=True=True, *args):
#    debugging_prints(msg, level, debug_level, log_timestamps=True, *args)




last_debug_level = 0  # Define the variable outside the function


def debugging_prints(msg, level, current_debug_level, log_timestamps=True, *args):

    global last_debug_level  # Use the global keyword to access the variable

    received_level = level # for 0 to 99 workflow
    output1 = ""
    output2 = ""
    if level >= current_debug_level:


        if last_debug_level <= 1:  # change the level
            level = 99  


        if level == 0:
            output1 += "-" * 120 + "\n"
            output2 += "-" * 12 + "\n"
            output1 += "Deepest Debugging (I see that you're in deep shit, huh...=)\n"
            output2 += "Deepest Debugging\n"
            output1 += msg + "\n"
            output2 += msg + "\n"
            output1 += "-" * 120 + "\n"
            output2 += "-" * 12 + "\n"
        elif level == 1:
            output1 += "-" * 120 + "\n"
            output2 += "-" * 12 + "\n"
            output1 += f"Deep level status update: {msg}\n"
            output2 += f"Deep level status update: {msg}\n"
            output1 += "-" * 120 + "\n"
            output2 += "-" * 12 + "\n"
        elif level == 2:
            output1 += f"Status: {msg}\n"
            output2 += f"Status: {msg}\n"
        elif level == 3:
            output1 += "-" * 55 + " WARNING " + "-" * 55 + "\n"
            output2 += "-" * 5 + " WARNING " + "-" * 5 + "\n"
            output1 += msg + "\n"
            output2 += msg + "\n"
            output1 += "-" * 120 + "\n"
        elif level == 4:
            output1 += get_random_art(level) + "\n"
            output1 += "#" * 120 + "\n"
            output1 += "#" * 54 + "   ERROR:   " + "#" * 54 + "\n"
            output2 += "#" * 5 + "   ERROR:   " + "#" * 5 + "\n"
            output1 += msg + "\n"
            output2 += msg + "\n"
            output1 += "#" * 120 + "\n"
        elif level == 5:
            output1 += get_random_art(level) + "\n"
            output1 += "#" * 120 + "\n"
            output1 += "#" * 120 + "\n"
            output1 += "#" * 47 + "       CRITICAL ERROR     " + "#" * 47 + "\n"
            output2 += "#" * 4 + "       CRITICAL ERROR     " + "#" * 4 + "\n"
            output1 += "#" * 120 + "\n"
            output1 += "#" * 120 + "\n"
            output1 += msg + "\n"
            output2 += msg + "\n"
            output1 += "#" * 120 + "\n"
            output1 += "#" * 120 + "\n"
        elif level == 6:
            output1 += get_random_art(level) + "\n"
            output1 += "Small success: " + msg + "\n"
            output2 += "Small success: " + msg + "\n"
        elif level == 7:
            output1 += get_random_art(level) + "\n"
            output1 += "Great success: " + msg + "\n"
            output2 += "Great success: " + msg + "\n"
        elif level == 99:
            output1 += msg
            output2 += msg + "\n"

    if output1 not in [None, ""]:
        print(output1)
        
    if output2 not in [None, ""]:
        try:
            write_log_to_file(output2, log_main, log_timestamps=True)
        except:
            logger.info(f"Sth went wrong with handing over debug prints to log buffer, program should continue though!")


    if received_level <= 1 and level == 99:
        last_debug_level = 0
    else:
        last_debug_level = level



def write_log_to_file(log_msg, filename, log_timestamps=True, mode="txt", headers=None):
    """
    Writes the provided log message to the given file. Is either called by debugging_prints() or manually.
    When called 
    The function also ensures the existence of the file and its directory. 
    It supports writing logs in 'txt' and 'csv' modes. Timestamps are added if 'log_timestamps' is True.
    
    Parameters:
    log_msg (str): The log message to be written.
    filename (str): The path of the file to write the log message.
    log_timestamps (bool, optional): If True, timestamps are added to each log message.
    mode (str, optional): The mode of the log ('txt' or 'csv').
    headers (list, optional): The headers for the 'csv' mode.
    """

    # calling or creating new log buffer
    log_buffer = LogBuffer.getInstance(filename)

    # create directory if it doesn't exist
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    try:
        if mode=="txt":
            # create file if it doesnt exist
            if not os.path.isfile(filename):
                with open(filename, 'w'):
                    pass

            # Apply timestamping logic before logging
            if log_timestamps:
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_msg = f"[{current_time}] {log_msg}"

            # Use the buffer instead of directly writing to the file
            log_buffer.log(log_msg + "\n")
        elif mode == "csv": #csv logs should always have timestamps in first column
            # create file if it doesnt exist
            if headers==None:
                headers = log_buffer.headers
            create_csv_via_pandas(filename, headers)
            if log_timestamps:
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_msg.insert(0, current_time)  # Insert the timestamp at the beginning of the list
            else:
                log_msg.insert(0, '')  # Insert an empty string at the beginning when no timestamp is required
            log_buffer.log(log_msg)
    except Exception as e:
        logger.error(f"Exception when writing to log: {e}")


def clear_log_file(file=log_main):
    """
    Clears the content of the specified log file.
    
    Parameters:
    file (str, optional): The path of the log file to be cleared. If not provided, 'log_main' is used.
    """
    with open(file, "w", encoding="utf-8") as log_file:
        log_file.write('')




def create_csv_via_pandas(filename, headers):
    """
    Creates a new CSV file with the provided headers using the pandas library. 
    If the file already exists or an error occurs, an appropriate message is printed to the console.
    
    Parameters:
    filename (str): The name of the CSV file to be created.
    headers (list): The headers for the new CSV file.
    
    Raises:
    Exception: Any error occurred during CSV file creation.
    """
    try:
        if not os.path.isfile(filename) or os.stat(filename).st_size == 0:
            df = pd.DataFrame(columns=headers)
            df.to_csv(filename, index=False)
            logger.info(f"CSV file created: {filename}", 0)
    except Exception as e:
        logger.error(f"An error occurred while creating the CSV file: {e}", 2)




class UserError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# this is how to use the above:
#try:
#    # your code here
#    raise UserError("An example user error occurred.")
#except UserError as e:
#    print(f"UserError: {e}")
#do not remove the above!



def parse_exception(e):
    """
    Returns only the last line of an exception.
    """
    match = re.search(r'Unable to locate element: {.*"selector":"(.*?)"}', str(e))
    match2 = re.search(r'Message: stale element reference: {.*"selector":"(.*?)"}', str(e))
    if match:
        return f"Unable to locate element:\n{match.group(1)}"
    elif match2:
        return f"Message: stale element reference:\n{match.group(1)}"
    else:
        return e

