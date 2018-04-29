import os.path

__all__ = [
    "__title__", "__summary__", "__uri__", "__version__",
    "__author__", "__email__", "__license__", "__copyright__",
]


try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None


__title__ = "warehouse"
__summary__ = "Next Generation Python Package Repository"
__uri__ = "https://pypi.org/"

__version__ = "15.0.dev0"

if base_dir is not None and os.path.exists(os.path.join(base_dir, ".commit")):
    with open(os.path.join(base_dir, ".commit")) as fp:
        __commit__ = fp.read().strip()
else:
    __commit__ = None

__author__ = "The Python Packaging Authority"
__email__ = "admin@mail.pypi.org"

__license__ = "Apache License, Version 2.0"
__copyright__ = "2018 %s" % __author__
