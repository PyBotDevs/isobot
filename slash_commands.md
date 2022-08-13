# Discord Slash Commands
### `create_option()` and Command Types

## `create_option()` Syntax
```python
create_option(name="something", description="Something else", option_type=3, required=True)
```

In this snippet, an example option `something` is provided here for reference.

* name: The option's name
* description: What the use of the option is, or what it does. Make sure it is understandable by all users
* option_type: Can only be defined as an `int`. The argument type, whether it is a string, integer, user mention, channel, role, etc.
* required: Whether the option has to be inputted by the user or not

## What is Discord Slash Command types?
Discord slash command types define what kind of argument is expected in a slash command.
For example, if I wanted to restrict integers to an argument `number`, I would write the command like this:

```python
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
client = discord.Client()
slash = SlashCommand(client)
@slash.slash(
    name="some_command",
    description="Does something",
    options=[
        create_option(name="number", description="Place to input a number", option_type=4, required=True)
    ]
)
async def some_command(ctx, number):
    await ctx.send(number + 1)
```

Here, see line 10. You can see in `create_option()` that the `option_type` argument was passed as a `4`. This is because 4 refers to an integer in the discord_slash library.

However, you can also directly define it in the method itself.

```python
import discord
from discord_slash import SlashCommand
client = discord.Client()
slash = SlashCommand(client)
@slash.slash(
    name="some_command",
    description="Does something"
)
async def some_command(ctx, number:int):
    await ctx.send(number + 1)
```

In this snippet, see line 9. In this example, the argument type was directly defined in the command itself. The discord_slash library reads this and automatically sets that as the slash command `option_type`. However, to avoid confusion, it is best to just define it in `create_option()`.

## Some Option Types
Not all option types are provided here, just the ones that will be used the most.

* sub-command: 1
* sub-command group: 2
* string: 3
* int: 4
* bool: 5
* user: 6
* channel: 7
* role: 8

<h6>NKA 2022 | Py | Discord | discord_slash | Discord library documentation</h6>