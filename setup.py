from setuptools import setup

import lumpy

setup(
  name = 'Lumpy',
  description = lumpy.__doc__,
  version = lumpy.__version__,
  packages = ['lumpy'],
  scripts = ['scripts/lumpy'],
  install_requires = [
    'dnspython',
  ],
  url = 'https://github.com/jorgebg/lumpy',
  author = lumpy.__author__,
  author_email = lumpy.__author_email__,
  license = lumpy.__license__,
  keywords = ['mta', 'mua', 'mail', 'smtp', 'mx']
)
