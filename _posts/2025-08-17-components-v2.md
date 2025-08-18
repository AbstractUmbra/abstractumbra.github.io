---
layout: post
title: "Components V2"
date: 2025-08-17 12:00:00 +0100
categories: discord.py
---
Discord.py 2.6 brings support for Discord's new components system (known as "Components V2"), which allows you to mix text, media, and interactive components when composing bot messages.

Some important things to know:

- Old components are not going away. They will continue to be supported by both Discord and discord.py.
  - You can continue to use `ui.View` under the old system, even if you have other parts of your bot using the new `ui.LayoutView`.
- You cannot send `content`, `embeds`, `stickers`, or `polls` in a message using the new components. New components provide the functionality of content and embeds.

## LayoutView

The [`ui.LayoutView`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.LayoutView) class replaces `ui.View` as the base class for all of your views. This is required in order to use the new components.

At the time of writing, the limit on total components contained in a LayoutView is 40. This includes nested components.

```py
class Layout(discord.ui.LayoutView):
    # you can add any top-level component here

    text = discord.ui.TextDisplay("Hello, Components V2!")

    action_row = discord.ui.ActionRow()

    @action_row.button(label = "A Button")
    async def a_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Clicked!", ephemeral = True)
```

## Top-level components

These components can be placed directly in a `LayoutView`.
<!-- (placed in order of usefulness, except container which is.. different) -->

### Text display

[`ui.TextDisplay`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.TextDisplay) allows placing regular text content in your layout. Markdown is supported. Note that mentions placed in the text will ping users/roles/everyone even if the text display is within a [container](#container).

## Action row {#action-row}

[`ui.ActionRow`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.ActionRow) is a container for [buttons and select menus](#buttons-selects). It can be subclassed and used with [`@ui.button`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.button)/[`@ui.select`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.select) or directly in a `LayoutView` as shown by the example above.

The [documentation page](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.ActionRow) has examples of both usages.

### Section {#section}

[`ui.Section`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.Section) allows placing text and an accessory side-by-side, where the accessory can be either a [thumbnail](#thumbnail) or [button](#buttons-selects).

```py
section = discord.ui.Section(
    "Text can be directly passed as strings, which will be wrapped in a TextDisplay automatically.",
    discord.ui.TextDisplay("Or you can pass a TextDisplay."),
    accessory = MyCustomButtonSubclass()
)
```

### Separator

[`ui.Separator`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.Separator) adds visual spacing between components. Whether a line is visible, and the amount of space (large or small), can be set.

### Media Gallery

[`discord.ui.MediaGallery`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.MediaGallery) allows displaying images and videos in a gallery. Entries are specified as [`discord.MediaGalleryItem`](https://discordpy.readthedocs.io/en/latest/api.html#discord.MediaGalleryItem)s. The current limit is 1-10 media per gallery.

```py
gallery = discord.ui.MediaGallery(
    discord.MediaGalleryItem("https://some.image/url.png", description = "Alt text"),
    discord.MediaGalleryItem("attachment://secret_message.png", spoiler = True),
)
```

### File

[`discord.ui.File`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.File) allows displaying files in your message. These will not display a preview. Files can also be marked as a spoiler. Note that your [`discord.File`](https://discordpy.readthedocs.io/en/latest/api.html#discord.File) needs to be included when sending the message.

### Container {#container}

[`discord.ui.Container`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.Container) can contain other top-level components. Visually, it displays a border similar to an embed, and can have an accent color. Containers can be marked as a spoiler.

```py
class MyContainer(discord.ui.Container):
    text = discord.ui.TextDisplay("This appears inside a box!")

class MyLayout(discord.ui.LayoutView):
    container = MyContainer(accent_color = 0x7289da)
```

## Non-top-level components

These cannot be placed directly under a LayoutView or Container.

### Buttons and select menus {#buttons-selects}

These have not changed from old components. However, you must manually place them in an [action row](#action-row) to include them in LayoutViews.

You might be interested in reading more about [the different types of select menus]({% post_url 2023-09-25-selects %}).

### Thumbnail {#thumbnail}

[`discord.ui.Thumbnail`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.Thumbnail) represents an image displayed on the right of a [section](#section). They can be marked as a spoiler.

```py
section = discord.ui.Section(
    "Text content",
    accessory = discord.ui.Thumbnail("attachment://thumb.png")
)
```

## Using with webhooks

Non-bot webhooks can now send non-interactive components by adding `?with_components=true` to the end of the webhook url.

## Component ids

All components now have a numerical `id` property. This is different from the `custom_id` property of interactive components. Manually setting the `id` and using [`LayoutView.find_item`](https://discordpy.readthedocs.io/en/latest/interactions/api.html#discord.ui.LayoutView.find_item) can help with managing deeply nested items.

```py
import discord
from discord import ui

COUNT_TRACKER_ID = 100027

class CounterButton(ui.Button):
    async def callback(self, i: discord.Interaction):
        self.view.count += 1

        text_display = self.view.find_item(COUNT_TRACKER_ID)
        text_display.content = f"The current count is {self.view.count}."

        await i.response.edit_message(view = self.view)

class MyCounterLayout(discord.ui.LayoutView):
    count = 0

    container = discord.ui.Container(
        discord.ui.Section(
            discord.ui.TextDisplay(
                f"The current count is {count}.",
                id = COUNT_TRACKER_ID,
            ),
            accessory = CounterButton(label = "+1"),
        )
    )
```

## Migrating persistent views

If the same buttons/select menus with the same `custom_id`s are present in a LayoutView, migrating from a persistent View to a persistent LayoutView should work as you expect. In fact, Discord allows you to edit messages that did not use new components to use new components, as long as you clear `content`/`embeds` by setting it to None in your edit. However, you cannot edit a message back to using old components.


This page was written by pipythonmc.
