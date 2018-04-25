

class IgnoreError(object):
    def __init__(self, print_error=False):
        self.__print_error = print_error

    def __enter__(self, *args):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and self.__print_error:
            print("An error happend! e: %s" % exc_type)
        return True
