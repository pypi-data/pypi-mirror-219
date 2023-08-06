# eko_throttler
<p>Async implementation of a rate-limited lock object for Python 3.11.x</p>

## Info
<p><strong>Author:</strong> Drix Holway<br><strong>Version:</strong> 0.2.0<br><strong>Revision Date:</strong> 2023-07-18</p>

## Usage
<p>The Throttler class requires a request limit <code>int</code> value, and an interval <code>timedelta</code> value on initialisation. These values dictate how the rate limiting will occur when a lock is acquired.</p>

```python
from datetime import timedelta
from eko_throttler import Throttler

async def main():
	throttler = Throttler(
		10,
		timedelta(seconds=1),
	)

	async with throttler:
		# do something
```

## Installation
<p>Installation of <code>eko_throttler</code> may be done using <code>pip</code>.</p>

```bash
pip install eko_throttler
```

## License
<p>Licensed under the <strong>[MIT](LICENSE)</strong> license.</p>

## Credits
<p>Copyright (c) 2023 Ekoteq</p>
<p><strong>Author:</strong> Drix Holway</p>
