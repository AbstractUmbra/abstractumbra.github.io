---
layout: post
title: "Application command basics"
date: 2023-01-30 12:00:00 +0100
categories: d.py discord.py
---

Hey there, welcome to the examples and explanations of the discord.py application (or 'slash') command system.

In these pages we'll cover everything from regular ol' slash commands all the way to Modals and the other component goodies. But for now we'll just cover the very basics.

## CommandTree {#cmd-tree}

The [CommandTree][command-tree] will be your "controller" of your application commands.
This object controls your "local" copy of the commands, versus what Discord has.

The slash command system requires that Discord has a copy of your commands.
This does **not** include the Command body, e.g:-
{% highlight python %}
async def command(interaction: discord.Interaction) -> None:
    # Discord has no idea what anything in here is.
{% endhighlight %}

What discord.py [will send][syncing] is:-
- The command name.
- The command description.
- The parameters names and descriptions.
- Parameter type information.
- The command permissions (default_permissions)
- The guilds it is limited to, if any.

So until this information is sent, these commands technically don't exist.

## Syncing the tree {#syncing}

To make discord aware of our changes, we need to sync the command tree.
This essentially sends the required informations taken from our written and registered code and sends it to Discord with the guilds/permissions and whatever else we require.

There is a method on the [CommandTree][command-tree] named [`sync`][sync] which does exactly that.

### Caveats

Now, as fantastic and well-handled as dpy does this, there are some common pitfalls the average user seems to hit when using these without guidance for the first time.
They may seem obvious after you read about them, which I hope is the case!

1. Don't auto-sync your CommandTree.
I see a lot of users syncing their tree within the `on_ready` event, or as part of the `setup_hook` entrypoint. Whilst the latter is definitely meant for "pre-launch" tasks, syncing your tree here is definitely not a good idea.
Why?
- Ratelimits.
  There are ratelimits on the app command creation endpoint. Discord don't announce these but I know they can be harsh (with 24h lockouts!). So don't sync until you're ready to, y'know?
- A lot of folks tend to sync before loading their extensions... which means their commands aren't loaded into their CommandTree yet. This may seem obvious to you, but not to everyone!

It's mostly point #1, but 2 is perfectly valid.

[syncing]: #syncing
[command-tree]: https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.CommandTree
[sync]: https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.CommandTree.sync
