from setuptools import setup
import os

# read requirements.txt file
current_directory = os.path.abspath(os.path.dirname(__file__))
requirements_file = os.path.join(current_directory, 'requirements.txt')
with open(requirements_file) as f:
    required_packages = f.read().splitlines()


setup(name='raster_basics',
      version='1.3.16',
      description='Basic GeoTIFF Processing',
      packages=['raster_basics'],
      install_requires=required_packages,
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