# Configure 🎁 Your 🤗 Python 🐍 Logging 📝

[![PyPI](https://img.shields.io/pypi/v/pydantic-loggings)](https://pypi.org/project/pydantic-loggings/)

## Installation

```shell
pip install pydantic-loggings
```

## Usage

- [examples](./examples)

### out of the box

```py
from pydantic_loggings.base import Logging


logger = Logging().get_logger(configure=True)

logger.debug('debug')
logger.info('info')
logger.warning('warning')

# 01-01 00:00:00 DEBUG   debug
# 01-01 00:00:00 INFO    info
# 01-01 00:00:00 WARNING warning
```

### Default Logging

```py
from pydantic_loggings.not_set import Logging


logger = Logging().get_logger(configure=True)

logger.debug('debug')
logger.info('info')
logger.warning('warning')

# warning
```

### Configure from Environment

```py
from pathlib import Path

from pydantic_loggings.not_set import Logging


env_file = Path(__file__).parent / '.env'
logger = Logging(_env_file=env_file).get_logger(configure=True)

logger.debug('debug')
logger.info('info')
logger.warning('warning')

# 01-01 00:00:00 [root]   DEBUG (main.py:11) debug
# 01-01 00:00:00 [root]    INFO (main.py:12) info
# 01-01 00:00:00 [root] WARNING (main.py:13) warning
```

```shell
# .env
log__formatters__my_formatter__datefmt='%m-%d %H:%M:%S'
log__formatters__my_formatter__format='{asctime} [{name}] {levelname:>7} ({filename}:{lineno}) {message}'
log__formatters__my_formatter__style='{'

log__handlers__my_handler__class_='logging.StreamHandler'
log__handlers__my_handler__formatter='my_formatter'

log__loggers__root__level='DEBUG'
log__loggers__root__handlers='["my_handler"]'

# is equivalent to:

# log__formatters__my_formatter='{"datefmt":"%m-%d %H:%M:%S","format":"{asctime} [{name}] {levelname:>7} ({filename}:{lineno}) {message}","style":"{"}'
# log__handlers__my_handler='{"class_":"logging.StreamHandler","formatter":"my_formatter"}'
# log__loggers__root='{"level":"DEBUG","handlers":["my_handler"]}'

# and/or:

# log__formatters='{"my_formatter":{"datefmt":"%m-%d %H:%M:%S","format":"{asctime} [{name}] {levelname:>7} ({filename}:{lineno}) {message}","style":"{"}}'
# log__handlers='{"my_handler":{"class_":"logging.StreamHandler","formatter":"my_formatter"}}'
# log__loggers='{"root":{"level":"DEBUG","handlers":["my_handler"]}}'
```

### Loggings

- not_set
- base
- rich
