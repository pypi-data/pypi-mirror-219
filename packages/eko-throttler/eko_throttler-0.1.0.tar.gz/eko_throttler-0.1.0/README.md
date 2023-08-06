# eko_throttler
Async implementation of a rate-limited lock object for Python 3.11.x

## Info
Author: Drix Holway
Version: 0.1.0
Revision Date: 2023-07-18

## Usage

```python
from eko_throttler import Throttler

async def main():
	throttler = Throttler(10, 1)
	async with throttler:
		# do something
```

## Installation

```bash
pip install eko_throttler
```

## License
Licensed under the [MIT](LICENSE) license.

## Credits
Copyright (c) 2023 Ekoteq

Author: Drix Holway
