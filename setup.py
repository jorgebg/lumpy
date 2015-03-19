from setuptools import setup

VERSION = '0.1.0'

setup(
  name='Lumpy',
  version=VERSION,
  description='Sends an email to a single recipient straight to his MTA',
  py_modules=['lumpy'],
  scripts=['scripts/lumpy'],
  install_requires=[
      'dnspython',
  ],
  author = 'Jorge Barata',
  url = 'https://github.com/jorgebg/lumpy',
  download_url = 'https://github.com/jorgebg/lumpy/tarball/0.1.0',
  license = 'MIT',
  keywords = ['mta', 'mua', 'mail', 'smtp', 'mx']
)
