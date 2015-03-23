from setuptools import setup

import lumpy

setup(
<<<<<<< HEAD
  name = 'Lumpy',
  description = lumpy.__doc__,
  version = lumpy.__version__,
  packages = ['lumpy'],
  scripts = ['scripts/lumpy'],
  install_requires = [
    'dnspython',
=======
  name='Lumpy',
  version=VERSION,
  description='Sends an email to a single recipient straight to his MTA',
  py_modules=['lumpy'],
  scripts=['scripts/lumpy'],
  install_requires=[
      'dnspython',
>>>>>>> 7fe915a2e695ec071e46fea9c7f4ca1412db0208
  ],
  url = 'https://github.com/jorgebg/lumpy',
  author = lumpy.__author__,
  author_email = lumpy.__author_email__,
  license = lumpy.__license__,
  keywords = ['mta', 'mua', 'mail', 'smtp', 'mx']
)
