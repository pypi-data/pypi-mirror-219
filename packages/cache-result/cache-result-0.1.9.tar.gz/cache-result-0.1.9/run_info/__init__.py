import functools
import os
import time
import inspect

def info(description):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time

            caller_file = inspect.getfile(inspect.currentframe().f_back)
            relative_file = os.path.relpath(caller_file, os.getcwd())

            # file_name = inspect.getfile(inspect.currentframe().f_back)

            log_str = f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{relative_file:10}\t{func.__name__:10}\t{execution_time:5.1f}s\t{description}"

            with open('log.txt', 'a', encoding='utf-8') as file:
                file.write(log_str + '\n')

            return result

        return wrapper

    return decorator



"""
            # log_data = {
            #     'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            #     'file': __file__,
            #     'function': func.__name__,
            #     'execution_time': execution_time,
            #     'description': description
            # }
"""