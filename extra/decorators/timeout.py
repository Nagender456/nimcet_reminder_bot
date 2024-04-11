import signal
import functools

class TimeoutError(Exception):
    pass

def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def handle_timeout(signum, frame):
                raise TimeoutError("Function timed out")

            # Set the signal handler and alarm
            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(seconds)  # Set the alarm for 'seconds' seconds

            try:
                result = func(*args, **kwargs)
            finally:
                # Reset the alarm
                signal.alarm(0)

            return result

        return wrapper

    return decorator
