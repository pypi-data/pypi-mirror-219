from setuptools import setup, find_packages
setup(
   name='covert-ots',
   version='1.0.4',
   packages=find_packages(),
   install_requires=[
      'typer',
      'rich',
      'inquirer',
      'pycryptodome'
   ],
   entry_points='''
      [console_scripts]
      covert-ots=covert.covert:app
      ''',
)