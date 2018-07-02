# setup.py
from distutils.core import setup
import py2exe

setup(
    console=['main.py'],
    options={
        "py2exe": {
            "includes": ['lxml.etree', 'lxml._elementpath', 'gzip'],
            "skip_archive": True,
            "unbuffered": True,
            "optimize": 2
        }
    }
)
