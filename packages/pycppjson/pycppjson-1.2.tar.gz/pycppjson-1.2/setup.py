from os import listdir
from setuptools import setup, Extension

setup(
      name='pycppjson',
      version='1.2',
      description='Load JSON in Python from C++!',
      packages=['pycppjson'],
      author_email='g6h6m238929@gmail.com',
      zip_safe=False,
      ext_modules=[Extension(file.split('.')[0], [file]) for file in listdir('pycppjson') if file.endswith('.cxx')]
)