import logging
import time
from stringcolor import bold



def timer_decorator(logger: logging.Logger):
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()  # get current time before function execution
            result = func(*args, **kwargs)  # function execution
            end_time = time.perf_counter()  # get current time after function execution
            run_time = end_time - start_time  # calculate execution time
            run_time = f"{run_time:.4f}"
            func_name = bold(func.__name__).cs("blue")
            run_time = bold(run_time).cs("green")

            logger.info(f"Finished {func_name} in {run_time} seconds")
            return result

        return wrapper
    return actual_decorator


def timer_decorator_async(logger: logging.Logger):
    def actual_decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()  # get current time after function execution
            run_time = end_time - start_time  # calculate execution time
            run_time = f"{run_time:.4f}"
            func_name = bold(func.__name__).cs("blue")
            run_time = bold(run_time).cs("green")

            logger.info(f"Finished {func_name} in {run_time} seconds")
            return result

        return wrapper
    return actual_decorator
