from functools import wraps

def cleanup_tmp_files(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        finally:
            self = args[0]
            self._delete_tmp_files(self.vectorstore_path)
    return wrapper
