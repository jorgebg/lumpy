# Lumpy

[![Pypy](https://img.shields.io/pypi/v/Lumpy.svg)](https://pypi.python.org/pypi/Lumpy)
[![Requirements Status](https://requires.io/github/jorgebg/lumpy/requirements.svg?branch=master)](https://requires.io/github/jorgebg/lumpy/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/jorgebg/lumpy/badge.svg)](https://coveralls.io/r/jorgebg/lumpy)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/jorgebg/lumpy/blob/master/LICENSE)

[![Stories in Ready](https://badge.waffle.io/jorgebg/lumpy.svg)](http://waffle.io/jorgebg/lumpy)

Sends an email to a **single recipient** straight to his MTA.
Looks up for the MX DNS records of the recipient SMTP server and attempts the delivery through them.

## Requirements
* Python 2.4+

## Install
```
sudo pip install lumpy
```

## Usage
```
usage: lumpy [-h] [--from [SENDER]] [--subject [SUBJECT]] [--body [BODY]] [--verbose] recipient

positional arguments:
  recipient

optional arguments:
  -h, --help            show this help message and exit
  --from [SENDER], -f [SENDER]
  --subject [SUBJECT], -s [SUBJECT]
  --body [BODY], -b [BODY]
  --verbose, -v
```

### Examples
```
lumpy finn@ooo.land
lumpy finn@ooo.land -s "Sir! My sir!"
lumpy jake@ooo.land -s "Sir! My sir!" -f queen@lumpy.space
lumpy jake@ooo.land -s "Sir! My sir!" -m "A message from their majesty."
```

### Programmatically

Use `lumpy.Mail(self, recipient, sender, subject, body)`

```python
from lumpy import Mail
m = Mail('finn@ooo.land')
m.send()
```
