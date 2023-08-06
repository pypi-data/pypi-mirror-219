from setuptools import setup
from pathlib import Path

# read requirements.txt file
def get_install_requires():
    """Returns requirements.txt parsed to a list"""
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setup(name='raster_basics',
      version='1.3.17',
      description='Basic GeoTIFF Processing',
      packages=['raster_basics'],
      install_requires=get_install_requires(),
      author_email='awwells@andrew.cmu.edu',
      url='https://github.com/albinwwells/Raster-Basics',
      zip_safe=False)

# navigate to directory
# python setup.py sdist
# twine upload dist/* 
# awwells, Awells98

# sudo pip install raster_basics --upgrade

# generate requirements.txt: navigate to directory, then:
# pipreqs raster_basics