from os import path

from setuptools import setup

setup(name='fdkcc',
      version='0.0.1',
      url='https://github.com/taemin410',
      py_modules=['fdkcc'],
      author='Tae Min Ha and Jae Won Choi',
      author_email='taemin410@gmail.com',
      # license=open(path.join(path.abspath(path.dirname(__file__)), 'LICENSE')).read(),
      install_requires=[x.strip() for x in
                        open(path.join(path.abspath(path.dirname(__file__)), 'requirements.txt')).readlines()],
      python_requires='>=3.5',
      )

