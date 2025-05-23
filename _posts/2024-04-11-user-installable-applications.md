---
layout: post
title: "User Installable Applications"
date: 2024-04-11 12:00:00 +0100
categories: discord.py
---
Hello! This post is all about User Installable Applications and how to set them up.

Let's get into the hows and whats, as well as limitations.

## Additions/edits to existing methods to accomodate this.

Discord.py always like to be convenient for it's userbase, and as such we've correctly modified the following items:-

#### Edits/Changes
- [`@app_commands.dm_only()`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.dm_only)
  - Applies the `dms=True` to the command allowed contexts.
- [`@app_commands.guild_only()`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.guild_only)
  - Applies the `guilds=True` to the command allowed contexts.

#### Added
- [`@app_commands.private_channel_only()`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.private_channel_only)
  - Applies the `private_channels=True` to allowed contexts.
- [`@app_commands.guild_install()`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.guild_install)
  - Specifies that this command will be a guild installable application command.
- [`@app_commands.user_install()`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.user_install)
  - Specifies that this command will be a user installable application command.
- [`@allowed_installs()`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.allowed_installs)
  - Controls the allowed installation methods.
- [`@allowed_contexts()`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.allowed_contexts)
  - Controls the allowed installation contexts.
- [`Interaction.is_user_integration()`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.Interaction.is_user_integration)
  - Determines if the interaction came from a user installed command.
- [`Interaction.is_guild_integration()`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.Interaction.is_guild_integration)
  - Determines if the interaction came from a guild installed command.

## Install locations {#user-apps-locations}

There are limited places where you can "install" these commands. These are:-

- Per User (you)
- Per Guild (which you manage)

"Per User" means that you can install an application to your user profile, which you - and only you - can use.
You can use this in any guild, any channel, any DM, so long as it [allowed in the context]({% post_url 2024-04-11-user-installable-applications %}#user-apps-contexts).

"Per Guild" means you can install an application within a guild which you have the Manage Guild permission in. Anyone in this guild can use this application command, so long as:-
- It is in the allowed context.
- They have permission to execute these commands as per the usual Application Command permissions.

## Allowed contexts {#user-apps-contexts}

Contexts are where installed apps are allowed to be used. In essence, the developer can specify where their commands are allowed to be used. Currently this is limited to:-

- Guilds
- DMs
- Private Channels (Group DMs/chats)

For some added clarity, let's imagine the below scenarios and how they work:-

> Developer creates a user-installable application with allowed contexts of guilds and dms.

This means that a general user can install this application to their account for their personal use, but they cannot use this application within a group chat or group dm. Only within guilds and DMs.

> Developer creates a user-installable application with allowed context of private channels.

This means that a general user can install this application to their account for their personal use, but they can *only* use this application within a group chat/dm.

> Developer creates a guild and user installable application with the allowed context of guilds.

This means that a Guild manager *or* general user can install this command -  Guild managers require the Manage Guild permission to install applications - and general users can install it to their account for usage.
This application can *only* be used within guilds.

## Creating installable commands

*Note*: I will be using explicit definitions in decorators to show all options, but you as a user can allow the defaults.

### Globally setting installation and contexts {#global-install-context}

If you are making an application in which all commands/menus will be user installable, instead of setting the decorator(s) on each callback, you can set it globally:-

If you're using `discord.Client`:-
{% highlight python %}
import discord

client = discord.Client(...)
tree = app_commands.CommandTree(
  allowed_contexts=discord.app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
  allowed_installs=discord.app_commands.AppInstallationType(guild=True, user=True)
)

client.tree = tree
{% endhighlight %}

Or if you're using `commands.Bot`:-
{% highlight python %}
import discord
from discord.ext import commands

bot = commands.Bot(
  ...,
  allowed_contexts=discord.app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
  allowed_installs=discord.app_commands.AppInstallationType(guild=True, user=True),
)
{% endhighlight %}

You can view the documentation on the `AppInstallationType` [here](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.AppInstallationType) and the `AppCommandContext` [here](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.AppCommandContext).

### Slash - user installable, executable anywhere. {#slash-user-unlocked}

Let's define a command that says hello to the executing user, and make it user installable, but executable anywhere.

{% highlight python %}
import discord
from discord import app_commands

my_client = discord.Client(intents=discord.Intents.none())
tree = app_commands.CommandTree(my_client)

@tree.command()
@app_commands.allowed_installs(guilds=False, users=True) # users only, no guilds for install
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # all allowed
async def hello(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")

...
{% endhighlight %}

You can see that using the decorators above is how we define the restrictions on user installable apps.
Once your command is defined you'd [sync it as normal]({% post_url 2023-01-30-app-command-basics %}#syncing) to make the changes live.

### Slash - guild installable, executable only in guilds. {#slash-guild-locked}

Now we'll define a command that can be installed to, and only used within a guild.
Something like a member info command:-

{% highlight python %}
# let's assume we use the client and tree like above

@tree.command(name="member-info")
@app_commands.allowed_installs(guilds=True, users=False) # guilds only this time
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False) # only guilds, again
async def member_info(interaction: discord.Interaction, member: discord.Member) -> None:
    await interaction.response.send_message(f"Here's what I have on {member.name}...")
    await _member_info(interaction, member) # this is boilerplate code, not real
{% endhighlight %}

### ContextMenu - user, non-cog, user installable, executable in dms and private channels {#ctx-nc-user-dms}

What a title...
Anyway, let's get to it.

{% highlight python %}
# Again, reusing the client and tree from the first codeblock

@tree.context_menu(name="Generate funny meme")
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=False, users=True, private_channels=True)
async def meme_generator_extreme(interaction: discord.Interaction, user: discord.User) -> None:
    # This is where we'd define our code here
{% endhighlight %}

This is a lazy example, sorry, but you can see the decorators in use here as expected.

### ContextMenu - cog, user installable, all contexts {#ctx-c-user-unlocked}

These titles are getting crazy.
This example is gonna be way more wordy, purely because of the Bot + Cog boilerplate code. But the example will be relevant.

{% highlight python %}
from discord import app_commands
from discord.ext import commands

my_bot = commands.Bot(intents=discord.Intents.none()) # we dont need intents here.

class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot, /) -> None:
        self.bot: commands.Bot = bot
        self.meme_context_menu = app_commands.ContextMenu(
            name="Generate funny meme",
            callback=self.meme_callback,
            allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
            allowed_installs=app_commands.AppInstallationType(guild=False, user=True)
        )
        self.bot.tree.add_command(self.meme_context_menu)

    async def meme_callback(self, interaction: discord.Interaction, user: discord.User) -> None:
        ...
{% endhighlight %}

This example is very wordy, but it was to show the `allowed_contexts` and `allowed_installs` kwargs in the `ContextMenu` constructor. This is how you'd do this, in this specific context.

Here's the relevant documentation for all 3 items:-

- [`ContextMenu`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.ContextMenu)
- [`AppCommandContext`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.AppCommandContext)
- [`AppInstallationType`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.AppInstallationType)

## Things to keep in mind.

### Permissions
If an application is installed *both* to your user **and** the current guild you're using it in, then guild permissions may override your ability to use your user installed commands from the application.

### Available information
When using processing a user installed command, the only information available to you is what's contained on the interaction itself. You will *not* receive any extra information that you may be used to having such as guild members, guild roles, etc.

### Final notes

As always, don't forget to [sync]({% post_url 2023-01-30-app-command-basics %}#syncing) as normal to make your apps installable after code changes, and don't forget to join [discord.py](https://discord.gg/dpy) if you need more help.
