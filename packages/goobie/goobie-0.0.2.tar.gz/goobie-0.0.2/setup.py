from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.2'
DESCRIPTION = ''
KEYWORDS = ['test']


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
]

# Setting up
setup(
    name="goobie",
    version=VERSION,
    author="Erasmus A. Junior",
    author_email="eirasmx@pm.me",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    licence='GNU LGPLv3',
    packages=['goobie/stubs'],
    package_data={'goobie/stubs': ['__init__.pyi', 'core.pyi', 'handler.pyi']},
    python_requires='>=3.7',
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    py_modules=['goobie'],
)

