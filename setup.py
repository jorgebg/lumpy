from setuptools import setup
from sys import version_info as pythonversion

import lumpy

requires = []
if pythonversion[0] is 3:
    requires.append("dnspython3")
else:
    requires.append("dnspython")


setup(
  name = 'Lumpy',
  description = lumpy.__doc__,
  version = lumpy.__version__,
  packages = ['lumpy'],
  scripts = ['scripts/lumpy'],
  install_requires = requires,
  url = 'https://github.com/jorgebg/lumpy',
  author = lumpy.__author__,
  author_email = lumpy.__author_email__,
  license = lumpy.__license__,
  keywords = ['mta', 'mua', 'mail', 'smtp', 'mx']
)
