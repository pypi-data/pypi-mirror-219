import setuptools
from setuptools import setup

setup(name='serra_cli',
      version='0.1.1',
      description='Simplified Data Pipelines',
      url='http://github.com',
      author='Albert Stanley',
      author_email='albert@serra.io',
      license='tbd',
      packages=setuptools.find_packages(),
      install_requires=[
         "click","requests", "tqdm"
      ],
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'serra=serra_cli.cli:main'
        ]
    })