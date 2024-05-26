---
layout: post
title: "Application Command definition examples"
date: 2023-01-30 13:00:00 +0100
categories: discord.py
---

Discord.py allows for several ways to create/define application commands within it's codebases.
In this page we'll go through several of these.

The mandatory preamble is that you should check out the [basics]({% post_url 2023-01-30-app-command-basics %}) before reading this.

## Within a Cog class

### Free-standing commands {#cog-free}
This means commands with no parent group, e.g. `/hello` or `/get-inventory`

A small working example is the following:-

{% highlight python %}
import discord
from discord import app_commands
from discord.ext import commands

class MyCog(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name="command-1")
  async def my_command(self, interaction: discord.Interaction) -> None:
    """ /command-1 """
    await interaction.response.send_message("Hello from command 1!", ephemeral=True)

  @app_commands.command(name="command-2")
  @app_commands.guilds(discord.Object(id=...), ...)
  async def my_private_command(self, interaction: discord.Interaction) -> None:
    """ /command-2 """
    await interaction.response.send_message("Hello from private command!", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog(bot))
{% endhighlight %}

Nothing too special, you can see that it defines those commands, and the discord.py mechanics for adding cogs (which is done when we load this extension in the `setup` method) will automatically add application commands to the [CommandTree][command-tree].

### Cog being a Parent group {#group-cog}
This means our Cog class name will be taken as the parent, e.g. `/parent command-1` and `/balance send`.

{% highlight python %}
import discord
from discord import app_commands
from discord.ext import commands

class MyCog(commands.GroupCog, name="parent"):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name="sub-1")
  async def my_sub_command_1(self, interaction: discord.Interaction) -> None:
    """ /parent sub-1 """
    await interaction.response.send_message("Hello from sub command 1", ephemeral=True)

  @app_commands.command(name="sub-2")
  async def my_sub_command_2(self, interaction: discord.Interaction) -> None:
    """ /parent sub-2 """
    await interaction.response.send_message("Hello from sub command 2", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog(bot))
  # or if you want guild/guilds only...
  await bot.add_cog(MyCog(bot), guilds=[discord.Object(id=...)])
{% endhighlight %}

For simplicity, the above commands are all global. You can add `guild=` or `guilds=` to `Bot.add_cog` in `setup` to add them to a guild, or use the `@app_commands.guilds()` decorator.

### Cog with optional parent group {#cog-opt}
This means that we can define commands within the Cog class that you can have as [free commands]({% post_url 2023-01-30-app-command-examples %}#cog-free) as well as having commands with a parent group, however it will be a tad different than the previous example:-

{% highlight python %}
import discord
from discord import app_commands
from discord.ext import commands

class MyCog(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  group = app_commands.Group(name="parent", description="...")
  # Above, we declare a command Group, in discord terms this is a parent command
  # We define it within the class scope (not an instance scope) so we can use it as a decorator.
  # This does have namespace caveats but i don't believe they're worth outlining in our needs.

  @app_commands.command(name="top-command")
  async def my_top_command(self, interaction: discord.Interaction) -> None:
    """ /top-command """
    await interaction.response.send_message("Hello from top level command!", ephemeral=True)

  @group.command(name="sub-command") # we use the declared group to make a command.
  async def my_sub_command(self, interaction: discord.Interaction) -> None:
    """ /parent sub-command """
    await interaction.response.send_message("Hello from the sub command!", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog(bot))
{% endhighlight %}

## Free-form definition of commands

We can also define commands without the extensions or Cog lifecycle, I refer to these as 'free-form' commands, and an example of them is as follows:-

{% highlight python %}
import asyncio

from discord.ext import commands
from discord import app_commands

# define Bot with **needed** parameters
bot = commands.Bot(command_prefix="some_prefix", intents=some_intents_definition)

# You can now use `@bot.tree.command()` as a decorator:
@bot.tree.command()
async def my_command(interaction: discord.Interaction) -> None:
  await interaction.response.send_message("Hello from my command!")
### NOTE: the above is a global command, see the `main()` func below:

# we can even use Groups
group = app_commands.Group(name="some-parent", description="description")

@group.command()
async def my_subcommand(interaction: discord.Interaction) -> None:
  await interaction.response.send_message("hello from the subcommand!")

bot.tree.add_command(group, guild=discord.Object(id=...))

async def main():
  async with bot:
    # do you setup stuff if you need it here, then:
    bot.tree.copy_global_to(guild=discord.Object(id=...))  # we copy the global commands we have to a guild, this is optional
    await bot.start(MY_TOKEN)

# We still need to sync this tree somehow, but you can make a command as discussed already.
{% endhighlight %}

## Hybrid Commands

Hybrid commands are a cool addition to discord.py which allows a command defintion to function as a prefix command AND an application command, e.g. `?hello` and `/hello`.

{% highlight python %}
# discord.py recently added full hybrid commands. They work as follows:
## Note: as I don't see a reason not to, I will present an example using a commands.Cog.

## IMPORTANT: hybrid commands only work if the signature is compatible with app commands.
# this means that all parameters must have a type annotation, even if it is just `str`.
# this also means that you must use `Transformers` not `Coverters` in these cases.


import discord
from discord.ext import commands

class MyCog(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot: commands.Bot = bot

  @commands.hybrid_command(name="ping")
  async def ping_command(self, ctx: commands.Context) -> None:
    """
    This command is actually used as an app command AND a message command.
    This means it is invoked with `?ping` and `/ping` (once synced, of course).
    """

    await ctx.send("Hello!")
    # we use ctx.send and this will handle both the message command and app command of sending.
    # added note: you can check if this command is invoked as an app command by checking the `ctx.interaction` attribute.


  @commands.hybrid_group(name="parent")
  async def parent_command(self, ctx: commands.Context) -> None:
    """
    We even have the use of parents. This will work as usual for ext.commands but will be un-invokable for app commands.
    This is a discord limitation as groups are un-invokable.
    """
    ...   # nothing we want to do in here, I guess!

  @parent_command.command(name="sub")
  async def sub_command(self, ctx: commands.Context, argument: str) -> None:
    """
    This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
    """

    await ctx.send(f"Hello, you sent {argument}!")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog(bot))
{% endhighlight %}

## Subclassing app_commands.Group

We can also subclass Group to add our commands within there:-

{% highlight python %}
# you can nest these down a few levels, like so:-

# /group subcommand (up to 25)
# /group subcommand group
# /group subcommand group subcommand (up to 25).

import discord
from discord import app_commands

# the discord-side check decorators (app_commands.guild_only, app_commands.allowed_installs, etc) can be used on the class like so:-
@app_commands.guild_only()
# these will apply to ALL subcommands (and groups), subcommands cannot have invidual perms!
class Group(app_commands.Group):

  # subcommand of Group (/group my_subcommand)
  @app_commands.command()
  async def my_subcommand(self, interaction: discord.Interaction) -> None:
    await interaction.response.send_message("hello from the subcommand!")

  # nested group command
  group2 = app_commands.Group(name="group2", description="This a nested group!")

  # subcommand of group2 (/group group2 my_second_group_command)
  @group2.command()
  async def my_second_group_command(self, interaction: discord.Interaction) -> None:
    await interaction.response.send_message("hello from the second subcommand!")

# unlike commands.GroupCog, you need to add this class to your tree yourself.
tree.add_command(Group())
{% endhighlight %}

[command-tree]: https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.CommandTree
