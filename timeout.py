import errno
import os
import signal
import functools

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator


import re
@timeout()
def match_pattern():
    match = re.findall(r'A(B|C+)+D', "ACCCCCCCCCCCCCCCCCCCCCCCCCCABD")
    if match:
        print("Match found:", match.group())
    else:
        print("No match found")

def main():
    match_pattern()

if __name__ == "__main__":
    main()