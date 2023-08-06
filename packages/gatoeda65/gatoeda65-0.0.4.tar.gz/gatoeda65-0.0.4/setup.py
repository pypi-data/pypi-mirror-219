
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Functions for exploratory data analysis'
LONG_DESCRIPTION = 'A set of functions that help to clean and analyse data builded on top of pandas, numpy, matplot.pyplot, seaborn, statsmodels, and scipy.'

# Setting up
setup(
    name='gatoeda65',
    version=VERSION,
    author='GatoMario (Mario Hevia Cavieres)',
    author_email="mario.hevia@gmail.com",
    description=DESCRIPTION,
    long_description_content_type='text',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['scipy', 'statsmodels', 'pandas', 'numpy', 'matplotlib', 'seaborn'],
    keywords=['python', 'EDA', 'exploratory data analysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

