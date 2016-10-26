from setuptools import setup

setup(name='grok',
      version='1.0',
      description='A python command-line tool to get information from wikis',
      license='MIT',
      install_requires=['requests'],
      scripts=['grok.py'])

