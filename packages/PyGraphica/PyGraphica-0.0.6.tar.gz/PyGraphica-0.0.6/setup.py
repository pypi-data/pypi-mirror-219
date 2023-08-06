from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='PyGraphica',
    version='0.0.6',
    license='MIT',
    author="Luke Campbell",
    author_email='LukeCampbell5853@gmail.com',
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'':['*.ttf']},
    url='https://github.com/LukeCampbell5853/PyGraphica',
    keywords='gui',
    install_requires=[
          'pysdl2',
          'pysdl2-dll',
          'pillow'
      ],
)