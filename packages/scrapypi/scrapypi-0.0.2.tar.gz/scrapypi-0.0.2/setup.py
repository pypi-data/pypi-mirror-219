from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as readme:
    with codecs.open(os.path.join(here, "CHANGELOG.md"), encoding="utf-8") as changelog:
        LONG_DESCRIPTION = readme.read() + '\n\n\n' + changelog.read()


VERSION = '0.0.2'
DESCRIPTION = 'Get PyPi Package information.'
KEYWORDS = ['pypi', 'information', 'package', 'module', 'stats', 'info', 'scrape']


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License', 
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
]

setup(
    name="scrapypi",
    version=VERSION,
    author="Erasmus A. Junior",
    author_email="eirasmx@pm.me",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    licence='MIT',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=['wget'],
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    py_modules=['scrapypi'],
    entry_points = {'console_scripts':['scrapypi = scrapypi:main']},
)
