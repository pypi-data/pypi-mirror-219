# GustavSelfBot

My self bot!
Current implementation of GustavSelfBot includes chat logs and commands.
<br>
TODO: make custom command and hooks possible

## Install

To install this module, simply run:

```commandline
python -m pip install GustavSelfBot
```

## Config

The required Config structure looks like this and is accessed from the root of your project. (config.json)

```json
{
  "token": "PUT_DISCORD_USER_TOKEN_HERE"
}
```

## Example

```python
import discord

from GustavSelfBot import log, Config, bot

if __name__ == "__main__":
    try:
        bot.run(token=Config["token"], log_handler=None)
    except discord.errors.LoginFailure as e:
        log.error(e)
        raise Exception(e)
```