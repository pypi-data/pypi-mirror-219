from setuptools import setup, find_packages

setup(
    name='PyGraphica',
    version='0.0.5',
    license='MIT',
    author="Luke Campbell",
    author_email='LukeCampbell5853@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/LukeCampbell5853/PyGraphica',
    keywords='gui',
    install_requires=[
          'pysdl2',
          'pysdl2-dll',
          'pillow'
      ],
    package_data={'':['*.ttf']}
)