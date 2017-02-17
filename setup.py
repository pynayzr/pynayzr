from setuptools import setup
from setuptools import find_packages


setup(name='pynayzr',
      version='0.0.1',
      description='Taiwan News Analyzer for Python',
      author='Louie Lu',
      author_email='me@louie.lu',
      url='https://louie.lu',
      license='MIT',
      install_requires=['pyocr', 'pillow', 'google-api-python-client'],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': ['pynayzr=pynayzr.cli:main'],
      },
      packages=find_packages())
