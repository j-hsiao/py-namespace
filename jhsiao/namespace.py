__all__ = ['make_ns']

import sys
import os
import re

pattern = re.compile(
    br'\s*__path__\s*=.*\.extend_path\(\s*__path__\s*,\s*__name__\s*\)')
OFLAGS = os.O_RDWR
if sys.version_info < (3,3):
    OFLAGS |= os.O_CREAT
def make_ns(*dirs, **kwargs):
    """Make the directories a namespace package.

    Add an extend_path call if not found and __init__.py exists.
    If version < 3.3, always add __init__.py even if it doesn't exist.
    Default namespace packages is only added at 3.3
    """
    basedir = kwargs.get('dir', None)
    for dirname in dirs:
        if basedir is not None:
            fname = os.path.join(basedir, dirname, '__init__.py')
        else:
            fname = os.path.join(dirname, '__init__.py')
        try:
            fd = os.open(fname, OFLAGS)
        except FileNotFoundError:
            continue
        with os.fdopen(fd, 'rb+') as f:
            if not any(map(pattern.match, f)):
                end = f.tell()
                if end != 0:
                    f.seek(end-1, os.SEEK_SET)
                    if f.read(1) != b'\n':
                        f.write(b'\n')
                f.write(
                    b"__path__ = __import__('pkgutil')"
                    b'.extend_path(__path__, __name__)\n')


def fdir(fname=None, *modifiers):
    """Convenience function to return directory of filename.

    If fname is None, use inspect to find the filename of caller.
    """
    if fname is None:
        import inspect
        fname = inspect.currentframe().f_back.f_code.co_filename
    return os.path.abspath(os.path.join(os.path.dirname(fname), *modifiers))
