from setuptools import setup, find_packages
setup(
  name='pitricks',
  version='0.1.4a2',
  author='pyy',
  url='https://github.com/one-pyy/pitricks',
  packages=find_packages(),
  install_requires=['regex', 'rich', 'nest_asyncio'],
  description='a tool box'
)