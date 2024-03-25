Create file in this directory to add more plugins.

## Basic Imports
```python
from . import client
from telethon import events

@client.on(events.NewMessage(pattern='{pattern_here}'))
async def _(event):
    ...
```

After this add `import` statement in `plugins/__init__.py`
