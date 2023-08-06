from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='PyGraphica',
    version='0.1.1',
    license='MIT',
    author="Luke Campbell",
    author_email='LukeCampbell5853@gmail.com',
    description="PyGraphica is an easy-to-learn GUI module designed for Python, built on the Python bindings (pysdl2) for SDL-2.",
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