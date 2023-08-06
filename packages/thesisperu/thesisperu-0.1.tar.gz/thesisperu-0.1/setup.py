from setuptools import setup, find_packages
from thesisperu.version import version

setup(
    name='thesisperu',
    version=version,
    description='Descarga la metada de las tesis',
    url='https://github.com/TJhon/tesis_peru',
    author='Jhon',
    author_email='fr.jhonk@gmail.com',
    packages=find_packages(),
	install_requires=[
        'pandas',
        'numpy<=1.24.3',
        'bs4',
        'tqdm',
  ]
)
