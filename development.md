# Development Manual
Developers can refer here when they need documentation on how to develop new commands and features for the isobot project.

## Slash Command Development
### Core Syntax
This starting syntax for slash commands is always required for developing new commands, or can be referenced when editing existing commands.

```py
@client.slash_command(
    name=<the general name for the command (alphanumerical characters, no spaces, only underscores)>
    description=<a description that fits best for the command's purpose>
)
```

This defines the Python command as a slash command, so that the PyCord library will understand and parse it correctly to the Discord API.

The actual Python command syntax requires `async` as PyCord is an asynchronous library.

```py
async def <command name>(ctx: ApplicationContext):
    <command source to be executed>
```

Assigning the command parameter `ctx` is important as it provides the base for all of the command's interactions (like sending a message response or getting author/guild/channel info, etc.)
Defining `ctx` as `ApplicationContext` is also equally as important as it helps Python to correctly parse the context data.

### Options
Options for a slash command are just like adding arguments to a Python command... except here you are actually doing exactly that.

To add an option, this decorator must be added after the core syntax.

```py
@option(
    name=<option name>,
    description=<short description on what the option does>,
    type=<str, int, bool, etc.>,
    default=<optional argument><preset value for the option, use None if option is optional>,
    choices=[
        <optional argument><a list of available options that user can choose from>
    ]
)
```

If an option is added to a slash command, that option also needs to be added to the actual Python command so that the parameter can be used with Python code.

For example, if I make a slash command `/hello` with an option to show the name of a person, it should be written like this:

```py
@client.slash_command(
    name="hello",
    description="Says hello to somebody!"
)
@option(name="name", description="The name of the person.", type=str)
async def hello(ctx: ApplicationContext, name: str):
    await ctx.respond(f"Hello {name}!")
```

## Auth Library Usage
The auth library is an important library, used to authorize the isobot client itself with Discord, as well as being used to authorize other libraries, clients, and API tools. It can also be used to provide essential client information, along with startup and runtime configuration to the bot client.

To start using the auth library, add this line of code to the source code:

```py
from api import auth
```

This will prepare the client to use the auth library and its properties.

From here, various things can be done with the library, which will be further documented here.




<!--
code_tips.txt

#you should use "not" in statements
#no need to declare variables unless they are random and you use it more than once
#if a == b: function()
#return await ctx.send
#declaring variable types is completely useless
#python isnt javascript, you dont have to use () in statements or loops
#an if statement doesnt need a corresponding else statement
#[a, b, c, d, ...] in 1 line
#import a, b, c, ... in 1 line
#when you are opening a file that is a subdirectory of the cwd you dont need to type full path... unix logic
-->
