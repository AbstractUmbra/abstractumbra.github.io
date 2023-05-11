---
layout: post
title: "Umbra's Sync Command"
date: 2023-01-29 12:00:00 +0100
categories: d.py discord.py
---
I curated and created a pretty full-featured command for [syncing][syncing] your CommandTree, you can see it here:

{% highlight python %}
from typing import Literal, Optional

import discord
from discord.ext import commands

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
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

The code above is freely given by me, and entirely unlicensed. Do what you will with it, I only ask if you make improvements then you share it with the rest of us!
