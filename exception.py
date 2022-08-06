import linecache
import sys


class DetailException:

    @staticmethod
    def get_exception_details():
        try:
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
        except AttributeError:
            return 'No EXCEPTION detected!'

    @staticmethod
    def print():
        print(DetailException.get_exception_details())