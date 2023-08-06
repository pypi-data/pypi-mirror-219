from setuptools import setup
import os

# read requirements.txt file
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()


setup(name='raster_basics',
      version='1.3.14',
      description='Basic GeoTIFF Processing',
      packages=['raster_basics'],
      install_requires=install_requires,
      author_email='awwells@andrew.cmu.edu',
      url='https://github.com/albinwwells/Raster-Basics',
      zip_safe=False)

# navigate to directory
# python setup.py sdist
# twine upload dist/* 
# awwells, Awells98

# sudo pip install raster_basics --upgrade