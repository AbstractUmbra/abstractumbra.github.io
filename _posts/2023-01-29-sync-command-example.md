---
layout: post
title: "Umbra's Sync Command"
date: 2023-01-29 12:00:00 +0100
categories: d.py discord.py
---
I curated and created a pretty full-featured command for [syncing]({% post_url 2023-01-30-app-command-basics %}#syncing) your CommandTree, you can see it here:

{% highlight python %}
from typing import Literal, Optional

import discord
from discord.ext import commands

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
{% endhighlight %}

The code above is freely given by me, and licensed with [The Unlicense](https://unlicense.org/). Do what you will with it, I only ask if you make improvements then you share it with the rest of us!

Editor's note:-
Please feel free to switch out the type annotations for `commands.Context` to your `Context` subclass if you have one. The rest of the annotations actually do things at runtime within d.py!

## Breakdown of the command

So the codeblock can be pretty overwhelming so let's break it down into pieces.

### Annotations

The annotations of the command parameters actually do have effect at runtime, so they exist for a reason!
Let's see them out:-

- `ctx: commands.Context`
  - This one is interesting. It doesn't do _too much_ at runtime, but it helps annotate the `ctx` object for you. You can switch `commands.Context` for your own context subclass if you have one, this is fine.
- `guilds: commands.Greedy[discord.Object]`
  - This one is interesting on it's own. We use two of the d.py converters here, which I'll explain backwards to make it easier. `discord.Object` takes an argument and attempts to parse it as if it were a discord ID. E.g. your user id. So this accepts any integer value, but we want it to act like a Guild, so only pass guild ids here please!
  - `commands.Greedy` is a really neat ext.commands converter, what this does is takes the entire argument string, and splits it on a whitespace. It then takes all split items and attempts to convert to the inner one (`discord.Object` here) until it fails, in which case it will allow the remaning split pieces to be parse by the remainder of the command arguments.
- `spec: Optional[Literal["~", "*", "^"]]`
  - This looks confusing but it's pretty simple to read. `Optional` means that passing a value here is... optional. The `= None` will make this parameter equal to `None` if no argument is passed.
  - `Literal["~", "*", "^"]` is the real converter. This means it accepts ONLY one of these 3 values (or None/no value, as above covered). Each of these 3 values does something unique within the command body, and yes, discord.py does respect `Literal` and will raise an error if you pass something erroneus.
    - ... However, since we have it wrapped in `Optional`, it allows no value to be passed. So no value, or one of the 3 within.

### Command body

So now that we convered the above, we can cover just what the command does...

I'll provide some execution examples, and then explain what is covered! Oh and for these examples `!` is the prefix.

- `!sync`
  - This takes all **global** commands within the CommandTree and sends them to Discord. (see [CommandTree]({% post_url 2023-01-30-app-command-basics %}#cmd-tree) for more info.)
- `!sync ~`
  - This will sync all guild commands for the current context's guild.
- `!sync *`
  - This command copies all global commands to the current guild (within the CommandTree) and syncs.
- `!sync ^`
  - This command will remove all guild commands from the CommandTree and syncs, which effectively removes all commands from the guild.
- `!sync 123 456 789`
  - This command will sync the 3 guild ids we passed: 123, 456 and 789. Only their guilds and guild-bound commands.
