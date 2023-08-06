from setuptools import setup, find_packages
setup(
   name='covert-ots',
   version='1.0.2',
   packages=find_packages(),
   install_requires=[
      'typer',
      'rich',
      'inquirer',
      'pycryptodome'
   ]
)